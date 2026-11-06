#!/usr/bin/env python3
"""fleet_lint.py: check every bot on disk against Chief's fleet rules.

Prints exceptions only. Prints "0 exceptions" when clean.
Read-only. Never reads secrets/ folders or store.db files.

Usage:
  python3 fleet_lint.py                # human list + JSON file
  python3 fleet_lint.py --json         # JSON only on stdout
  python3 fleet_lint.py --out FILE     # where to write JSON (default /workspace/routine-scripts/fleet_lint.latest.json)
Exit code: 0 clean, 1 exceptions found, 2 script error.
"""
import argparse, glob, json, os, re, sys
from collections import defaultdict

ROOT = "/home/box/agent-data"
AGENTS = os.path.join(ROOT, "agents")
CHIEF_ID = "ad6690d7-be33-4540-ac42-68eb3059c181"
TEAM_MD = os.path.join(AGENTS, CHIEF_ID, "memory", "TEAM.md")
IDS_MD = "/workspace/fleet/IDS.md"
FLEET_MD = "/workspace/fleet/FLEET.md"
DELETED_JSON = os.path.join(ROOT, "deleted-agents.json")
DEFAULT_OUT = "/workspace/routine-scripts/fleet_lint.latest.json"

EM = "\u2014"
UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

# A mention of a retired name is OK when nearby words show the text is warning about it.
NEG_BEFORE = re.compile(r"\b(not|never|no longer|don't|do not|old|retired|former(?:ly)?|stale|deleted|without|instead of)\b", re.I)
NEG_AFTER = re.compile(r"retired|stale|\bgone\b|deleted|merged|now Penny|now Tally|\u2192|->|\(now|are stale|is retired", re.I)


def negated(s, m):
    return bool(NEG_BEFORE.search(s[max(0, m.start() - 45):m.start()]) or NEG_AFTER.search(s[m.end():m.end() + 80]))


# (rule_id, regex, description). Flagged only when the sentence has no NEGATION word.
RETIRED_TERMS = [
    ("retired-crm-watch", re.compile(r"\bCRM Watch\b", re.I), "names retired bot CRM Watch"),
    ("retired-pa-8b769a17", re.compile(r"8b769a17"), "names retired Personal Assistant 8b769a17"),
    ("retired-personal-assistant", re.compile(r"\bPersonal Assistant\b(?! for)"), "names old Personal Assistant bot (now Penny)"),
    ("retired-pa-schedules", re.compile(r"\bPA Schedules\b"), "names merged PA Schedules bot (now Penny)"),
    ("retired-ledger", re.compile(r"\bLedger\b"), "names Ledger (CRM bot is Tally)"),
    ("retired-morgan", re.compile(r"\bMorgan\b"), "names Morgan (retired name)"),
    ("scdd-watch-active", re.compile(r"SCDD Instant Form watch|Instant Form watch", re.I), "treats SCDD Instant Form watch as active"),
    ("retired-bot-name", re.compile(r"\b(Lingxi|AI Expert|Herald|Bolt|Warden|Cipher|Bottleneck|CoS Ops)\b"), "names a retired bot"),
]
NUMA_PREFERRED = re.compile(
    r"prefer(?:red|s)?\s+Numa|Numa\s+(?:is\s+)?(?:preferred|first|default)|use Numa for new|"
    r"Numa over Quo", re.I)
AURORA_AD = re.compile(r"\bAurora\b", re.I)
AD_WORDS = re.compile(r"\b(ads?|campaigns?|target(?:ing|ed)?|geo|radius|audience|Meta|Google Ads|boost)\b", re.I)
SELF_FIX = re.compile(r"self[- ]fix", re.I)
WEEKEND = {0, 6}
QUIET_START, QUIET_END = 21, 7  # 9pm to 7am CT


def short_name(name):
    """Short name before " · " (e.g. "Penny · admin" -> "Penny"). Bots were renamed to "Name · role" ~2026-10-26."""
    return (name or "").split(" \u00b7 ", 1)[0].strip()


def name_keys(name):
    """Every form a doc may use for this bot: full profile name and short name."""
    return {k for k in ((name or "").strip(), short_name(name)) if k}


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?\n])\s+", text or "") if s.strip()]


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def scan_terms(text, where, add, bot):
    """Retired-name, Numa and Aurora checks on one block of text."""
    for s in sentences(text):
        for rid, rx, why in RETIRED_TERMS:
            for m in rx.finditer(s):
                if not negated(s, m):
                    add(bot, rid, f"{where}: {why}", snippet(s, rx))
                    break
        if NUMA_PREFERRED.search(s):
            add(bot, "numa-preferred", f"{where}: says Numa is preferred for phone work (Quo is preferred)", snippet(s, NUMA_PREFERRED))
        if AURORA_AD.search(s) and AD_WORDS.search(s) and not re.search(r"\b(exclude|not|never|no)\b", s, re.I):
            add(bot, "aurora-ad-target", f"{where}: references Aurora in an ad or targeting context", snippet(s, AURORA_AD))


def snippet(s, rx, width=70):
    m = rx.search(s)
    if not m:
        return s[:width * 2].replace("\n", " ")
    a, b = max(0, m.start() - width), min(len(s), m.end() + width)
    return ("..." if a else "") + s[a:b].replace("\n", " ") + ("..." if b < len(s) else "")


# ---------- cron ----------
def expand(field, lo, hi):
    out = set()
    for part in field.split(","):
        step = 1
        if "/" in part:
            part, st = part.split("/", 1)
            step = int(st)
        if part in ("*", "?"):
            a, b = lo, hi
        elif "-" in part:
            a, b = (int(x) for x in part.split("-", 1))
        else:
            a = b = int(part)
            if step != 1:
                b = hi
        out.update(range(a, b + 1, step))
    return out


def cron_flags(expr):
    """Return list of human reasons a cron fires on a weekend or in quiet hours (CT)."""
    tz = "America/Chicago"
    e = expr.strip()
    m = re.match(r"(?:CRON_)?TZ=(\S+)\s+(.*)", e)
    if m:
        tz, e = m.group(1), m.group(2)
    f = e.split()
    if len(f) != 5:
        return [f"unparsed schedule '{expr}'"]
    try:
        hours = expand(f[1], 0, 23)
        dows = {d % 7 for d in expand(f[4], 0, 6 if f[4] in ("*", "?") else 7)}
    except ValueError:
        return [f"unparsed schedule '{expr}'"]
    reasons = []
    if tz not in ("America/Chicago", "US/Central"):
        reasons.append(f"timezone {tz} (not CT), times below may be off")
    wk = sorted(dows & WEEKEND)
    if wk and f[2] == "*":
        reasons.append("fires on " + "/".join("Sun" if d == 0 else "Sat" for d in wk))
    elif f[2] != "*" and f[4] == "*":
        reasons.append("day-of-month schedule, can land on a weekend")
    quiet = sorted(h for h in hours if h >= QUIET_START or h < QUIET_END)
    if quiet:
        reasons.append("fires in quiet hours (9pm to 7am CT) at hour " + ",".join(str(h) for h in quiet))
    return reasons


# ---------- docs ----------
def parse_ids_md():
    """Return dict id -> {name, status, section} from IDS.md bot and room tables."""
    rows = {}
    if not os.path.exists(IDS_MD):
        return rows
    section = None
    for line in open(IDS_MD, encoding="utf-8"):
        if line.startswith("### Active bots"):
            section = "active"
        elif line.startswith("### Retired bots"):
            section = "retired"
        elif line.startswith("## 2. Group rooms"):
            section = "room"
        elif line.startswith("## 3"):
            section = None
        if section and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            ids = UUID_RE.findall(line)
            if ids and len(cells) > 1:
                rows[ids[0]] = {"name": cells[0], "status": section}
    return rows


def parse_fleet_md():
    """Return (active_names, retired_names) from FLEET.md summary table."""
    act, ret = set(), set()
    if not os.path.exists(FLEET_MD):
        return act, ret
    for line in open(FLEET_MD, encoding="utf-8"):
        if line.startswith("| ") and not line.startswith("| Bot ") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 6 and cells[-1].strip("*").lower() in ("active", "retired"):
                (ret if "retired" in cells[-1].lower() else act).add(cells[0])
    return act, ret


def parse_team_md():
    ids, names = set(), set()
    if not os.path.exists(TEAM_MD):
        return ids, names
    text = open(TEAM_MD, encoding="utf-8").read()
    ids = set(UUID_RE.findall(text))
    m = re.search(r"## Current names.*?\n(.*?)\n## ", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 2 and cells[1] and not cells[1].startswith("---") and cells[1] != "Current bot":
                names.add(re.sub(r"\s*\(.*", "", cells[1]))
    return ids, names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="print JSON only")
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    exc = []
    notes = []

    def add(bot, rule, msg, snip=None):
        exc.append({"bot": bot, "rule": rule, "message": msg, **({"snippet": snip} if snip else {})})

    deleted = set()
    if os.path.exists(DELETED_JSON):
        try:
            deleted = set(load_json(DELETED_JSON).get("agents", {}).keys())
        except Exception as e:
            notes.append(f"could not read deleted-agents.json: {e}")

    bots, rooms = {}, {}
    for d in sorted(glob.glob(os.path.join(AGENTS, "*/"))):
        aid = os.path.basename(d.rstrip("/"))
        pf = os.path.join(d, "profile.json")
        if not os.path.exists(pf):
            continue
        label = aid[:8]
        try:
            prof = load_json(pf)
        except Exception as e:
            add(label, "profile-unreadable", f"profile.json does not parse: {e}")
            continue
        name = (prof.get("name") or "").strip()
        label = f"{name or '(no name)'} ({aid[:8]})"
        is_room = os.path.exists(os.path.join(d, "group.json"))
        (rooms if is_room else bots)[aid] = {"name": name, "label": label, "prof": prof, "dir": d}
        desc = prof.get("description") or ""

        sf = os.path.join(d, "settings.json")
        if not os.path.exists(sf):
            add(label, "settings-missing", "settings.json missing")
        else:
            try:
                load_json(sf)
            except Exception as e:
                add(label, "settings-unreadable", f"settings.json does not parse: {e}")

        if not name:
            add(label, "name-empty", "profile name is empty")
        for fld in ("name", "title", "description"):
            v = prof.get(fld) or ""
            if EM in v:
                add(label, "em-dash", f"{fld} contains {v.count(EM)} em dash(es)")
        if is_room:
            try:
                g = load_json(os.path.join(d, "group.json"))
                members = set(UUID_RE.findall(json.dumps(g)))
                for mid in members:
                    if mid in deleted:
                        add(label, "room-member-deleted", f"room lists deleted agent {mid[:8]}")
                    elif not os.path.isdir(os.path.join(AGENTS, mid)):
                        add(label, "room-member-missing", f"room lists agent {mid[:8]} with no folder on disk")
            except Exception as e:
                add(label, "group-unreadable", f"group.json does not parse: {e}")
        else:
            if not desc.strip():
                add(label, "description-empty", "description is empty")
            elif not SELF_FIX.search(desc):
                add(label, "self-fix-missing", "description has no Self-fix line")
        scan_terms(desc, "description", add, label)
        for ref in set(UUID_RE.findall(desc)):
            if ref in deleted:
                add(label, "references-deleted-id", f"description references deleted agent/room {ref[:8]}")

        # on-disk automations (may be stale copies)
        for af in sorted(glob.glob(os.path.join(d, "automations", "*", "automation.json"))):
            rname = os.path.basename(os.path.dirname(af))
            try:
                a = load_json(af)
            except Exception as e:
                add(label, "automation-unreadable", f"{rname}: automation.json does not parse: {e}")
                continue
            if a.get("enabled") is False:
                continue
            trig = (a.get("triggerPresentation") or {}).get("trigger") or {}
            sched = a.get("schedule") or trig.get("schedule")
            disp = a.get("name") or rname
            if sched and (trig.get("type") in (None, "cron")):
                rs = cron_flags(sched)
                if rs:
                    add(label, "schedule-off-hours", f"routine '{disp}' ({sched}) " + "; ".join(rs) + " [on-disk copy, may be stale]")
            elif trig.get("type") not in (None, "cron"):
                notes.append(f"{label}: routine '{disp}' has trigger type {trig.get('type')}, not checked")
            prompt = a.get("prompt") or ""
            scan_terms(prompt, f"routine '{disp}' prompt [on-disk copy, may be stale]", add, label)
            for ref in set(UUID_RE.findall(prompt)):
                if ref in deleted:
                    add(label, "references-deleted-id", f"routine '{disp}' prompt references deleted agent/room {ref[:8]} [on-disk copy, may be stale]")

    # duplicate names
    by_name = defaultdict(list)
    for aid, b in {**bots, **rooms}.items():
        if b["name"]:
            by_name[b["name"].lower()].append(aid)
    for n, ids in by_name.items():
        if len(ids) > 1:
            add(n, "duplicate-name", "name used by " + ", ".join(i[:8] for i in ids))

    # cross-check docs
    on_disk = {**bots, **rooms}
    ids_rows = parse_ids_md()
    if not ids_rows:
        notes.append(f"{IDS_MD} missing or unparsed")
    for aid, r in ids_rows.items():
        if r["status"] in ("active", "room"):
            if aid not in on_disk:
                add(r["name"], "ids-md-missing-on-disk", f"IDS.md lists {r['status']} {aid[:8]} but no folder on disk")
            elif r["name"] not in name_keys(on_disk[aid]["name"]):
                add(on_disk[aid]["label"], "ids-md-name-mismatch", f"IDS.md calls it '{r['name']}', profile says '{on_disk[aid]['name']}'")
        elif r["status"] == "retired" and aid in on_disk:
            add(on_disk[aid]["label"], "retired-still-on-disk", "IDS.md marks this bot retired but its folder is still on disk (pending sidebar delete)")
    for aid, b in on_disk.items():
        if ids_rows and aid not in ids_rows:
            add(b["label"], "missing-from-ids-md", "on disk but not listed in IDS.md")

    f_act, f_ret = parse_fleet_md()
    if not f_act:
        notes.append(f"{FLEET_MD} missing or unparsed")
    disk_bot_names = {k for b in bots.values() for k in name_keys(b["name"])}
    for n in sorted(f_act - disk_bot_names):
        add(n, "fleet-md-missing-on-disk", "FLEET.md lists this active bot but no bot with that name is on disk")
    if f_act:
        for aid, b in bots.items():
            keys = name_keys(b["name"])
            if not (keys & f_act) and not (keys & f_ret):
                add(b["label"], "missing-from-fleet-md", "on disk but not in FLEET.md summary table")
            elif keys & f_ret:
                add(b["label"], "retired-still-on-disk", "FLEET.md marks this bot retired but it is still on disk")

    # Live routine folders with no on-disk copy (confirmed live 2026-10-21)
    KNOWN_LIVE_ROUTINE_IDS = {"5a9f4a41-dbcf-5bdb-bcdf-f3cf132a4689", "2da06ad7-fb78-5ee3-a15a-91219eb5b712"}
    t_ids, t_names = parse_team_md()
    auto_dirs = {os.path.basename(x.rstrip("/")) for x in glob.glob(os.path.join(AGENTS, "*", "automations", "*/"))}
    team_text = open(TEAM_MD, encoding="utf-8").read() if os.path.exists(TEAM_MD) else ""
    # Page (canvas) and store IDs are not agents: skip IDs inside cursor.com/canvas links
    # and in any "## ... Page ..." section (project Page table). Added 2026-11-01.
    page_ids = set()
    for url in re.findall(r"cursor\.com/canvas/\S+", team_text):
        page_ids.update(UUID_RE.findall(url))
    for sec in re.findall(r"^## [^\n]*\bPage\b[^\n]*\n(.*?)(?=^## |\Z)", team_text, re.S | re.M):
        page_ids.update(UUID_RE.findall(sec))
    for tid in sorted(t_ids - page_ids):
        line = next((l for l in team_text.splitlines() if tid in l), "")
        if re.search(r"\* \*|routine|folder", line, re.I) and tid not in on_disk:
            if tid not in auto_dirs and not any(tid.startswith(k) or k.startswith(tid) for k in KNOWN_LIVE_ROUTINE_IDS):
                add("TEAM.md", "team-md-routine-folder-missing", f"TEAM.md routine folder {tid[:8]} not found in any on-disk automations folder (on-disk copies may be stale)")
            continue
        if tid not in on_disk:
            add("TEAM.md", "team-md-missing-on-disk", f"TEAM.md references {tid[:8]}, no folder on disk" + (" (in deleted-agents.json)" if tid in deleted else ""))
    for n in sorted(t_names - disk_bot_names):
        add("TEAM.md", "team-md-name-not-on-disk", f"TEAM.md current-names table lists '{n}', no bot with that name on disk")
    missing_team = sorted(b["name"] for aid, b in bots.items()
                          if t_ids and aid not in t_ids and not (name_keys(b["name"]) & t_names)
                          and not any(re.search(r"\b" + re.escape(k) + r"\b", team_text) for k in name_keys(b["name"])))
    if missing_team:
        add("TEAM.md", "missing-from-team-md", f"{len(missing_team)} bots on disk not named anywhere in TEAM.md: " + ", ".join(missing_team))

    # de-dupe identical lines
    seen, uniq = set(), []
    for e in exc:
        k = (e["bot"], e["rule"], e["message"])
        if k not in seen:
            seen.add(k)
            uniq.append(e)
    exc = uniq

    result = {
        "checked": {"bots": len(bots), "rooms": len(rooms)},
        "exception_count": len(exc),
        "exceptions": exc,
        "notes": notes,
        "sources": {"agents": AGENTS, "ids_md": IDS_MD, "fleet_md": FLEET_MD, "team_md": TEAM_MD},
    }
    try:
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
    except OSError as e:
        notes.append(f"could not write {args.out}: {e}")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if not exc:
            print("0 exceptions")
        else:
            print(f"{len(exc)} exceptions ({len(bots)} bots, {len(rooms)} rooms checked)")
            by_rule = defaultdict(list)
            for e in exc:
                by_rule[e["rule"]].append(e)
            for rule in sorted(by_rule):
                print(f"\n[{rule}] {len(by_rule[rule])}")
                for e in by_rule[rule]:
                    print(f"- {e['bot']}: {e['message']}")
        for n in notes:
            print(f"note: {n}")
        print(f"JSON: {args.out}")
    return 1 if exc else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # never crash silently in a routine
        print(f"fleet_lint error: {e}", file=sys.stderr)
        sys.exit(2)
