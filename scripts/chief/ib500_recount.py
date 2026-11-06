#!/usr/bin/env python3
"""ib500_recount.py: IB 500 nightly recount. Slack count messages vs the Sheet's Daily log.

The bot exports the day's #ironblueprint messages and the Daily log tab with its own
connectors. This script never calls Slack or Sheets. It applies the rules Ryne approved 10/18:

  Counted (explicit increment): "Add 5", "Add 5 more", "5 more", "5 done", "5 programs done",
                                "5 programs added", "Added 5 more", "2 more added".
  AMBIGUOUS, not counted, ask:  a number that could be a total: "so far", "total", "to now",
                                "from Saturday", "since", "up to", "overall", "in all", "we're at".
  Skipped:                      the nightly pace post (anything with "N of 500", "N/500" or "_213 / 500_";
                                markdown _ * ~ ` is stripped first), messages with no count words (bug
                                reports, feedback), and notes of 4+ lines unless a line is an explicit add.
  Never a count:                the goal number 500 or "the 500 programs" ("once we have the 500 programs done").
                                Spelled-out numbers ("three programs in a row") count only next to an add verb
                                ("added five", "five done"); digits next to a count word still do.
  UNCLEAR, not counted, ask:    a number right next to a count word ("7 programs", "add 7")
                                that fits no pattern above, or two different counts in one message.
  Skipped:                      messages that start with "Bug:".
  NOTE (exit code unchanged):   a Sheet cell holding text, e.g. "Platform Down", counted as 0.
Then per date and person: Slack sum vs the Sheet cell. Any difference is listed.
On the requested date(s) it also checks the Day total and Running total cells against the person cells.

Inputs:
  --slack  JSON list of messages: ts (Slack ts), user (id) and/or user_name, text
           (a Slack conversations.history export {"messages": [...]} also works)
  --sheet  Daily log as CSV (Date, one column per person, optional Day total, Running total),
           or Sheets values JSON {"values": [[header...], [row...]]}
  --people "U0HPMS8MU=Ryne,U62EKBP1Q=Nick,..." maps Slack ids to Sheet columns (defaults built in)

Usage:
  python3 ib500_recount.py --slack day.json --sheet daily-log.csv --date 2026-10-21
  python3 ib500_recount.py --slack all.json --sheet daily-log.csv          # every date in the Slack file
  options: --json, --skip-ts TS[,TS...] (messages already resolved by hand)
Exit code: 0 everything matches, 1 differences or messages to ask about, 2 script error.
"""
import argparse, csv, datetime as dt, json, re, sys
from collections import defaultdict
from zoneinfo import ZoneInfo

CHI = ZoneInfo("America/Chicago")
DEFAULT_PEOPLE = {"U0HPMS8MU": "Ryne", "U62EKBP1Q": "Nick", "U09AYPV9F3Q": "Blake",
                  "U085X5K1874": "Santos", "U0AJXGFCMR6": "Scott"}
WORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve "
                                     "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
NUM = r"(\d{1,3}|" + "|".join(WORDS) + r")"   # digits or a spelled-out number (only next to an add verb)
DIG = r"(\d{1,3})"                               # digits only
PACE = re.compile(r"\b\d{1,3}\s*(?:/|of)\s*500\b", re.I)
AMBIG = re.compile(r"\b(so far|in total|total|to now|till now|until now|up to now|from (?:this past |last )?"
                   r"(?:mon|tue|wed|thu|fri|sat|sun)\w*|since|overall|in all|we'?re at|i'?m at|i have|i'?ve done|brings? (?:me|us) to)\b", re.I)
VERB_AFTER = r"(?:done|added|finished|completed?|made|logged)"
VERB_BEFORE = r"(?:add|added|did|made|logged|finished|completed)"
NOT_PROGRAMS = r"(?:reps?|sets?|rounds?|weeks?|days?|exercises?|minutes?|mins?|seconds?|secs?|lbs?|pounds?)"
# A number is a possible count only right next to a count word. Digits: "7 programs", "7 more", "add 7", "7 done".
# Spelled-out numbers only next to an explicit add verb: "added five", "five done" (not "three programs in a row").
ADJACENT = re.compile(rf"\b{DIG}\s+(?:more\b(?!\s+{NOT_PROGRAMS}\b)|(?:programs?|done|added|finished|completed?|made|logged)\b)"
                      rf"|\b{NUM}\s+(?:more\s+)?(?:programs?\s+)?{VERB_AFTER}\b"
                      rf"|\b{VERB_BEFORE}\s+{NUM}\b(?!\s*-)", re.I)
INCREMENT = [
    re.compile(rf"\badd(?:ed)?\s+(?:another\s+)?{NUM}\b(?:\s+more)?(?:\s+programs?)?", re.I),
    re.compile(rf"\b{NUM}\s+(?:more\s+)?(?:programs?\s+)?(?:more\s+)?{VERB_AFTER}\b", re.I),
    re.compile(rf"\b{DIG}\s+more\b(?!\s+{NOT_PROGRAMS}\b)", re.I),
]
MARKDOWN = re.compile(r"[_*~`]")
GOAL = re.compile(r"\b(?:the|our|all|ib)?\s*500\b(?:\s+(?:total\s+)?programs?)?", re.I)
LONG_LINES = 4   # a message with this many non-empty lines is notes/feedback unless a line is an explicit add


def num(s):
    s = s.lower()
    return int(s) if s.isdigit() else WORDS[s]


def classify(text):
    """Return (kind, count). kind: count | ambiguous | unclear | pace | none."""
    t = re.sub(r"<[^>]+>", " ", text or "")
    t = MARKDOWN.sub(" ", t)                     # "_213 / 500_" -> " 213 / 500 "
    if PACE.search(t):
        return "pace", None
    if re.match(r"\s*bug\s*:", t, re.I):
        return "none", None
    t = GOAL.sub(" ", t)                         # the goal (500, "the 500 programs") is never an increment
    lines = [ln for ln in t.splitlines() if ln.strip()]
    if len(lines) >= LONG_LINES:
        adds = [ln for ln in lines if any(rx.search(ln) for rx in INCREMENT)]
        if not adds:
            return "none", None                  # meeting notes, feedback lists
        t = "\n".join(adds)
    found = []
    for rx in INCREMENT:
        for m in rx.finditer(t):
            found.append((m.start(), num(m.group(1))))
    values = {v for _, v in found}
    # for the ASK rule a spelled-out number still counts as "a number" ("they include the one's from Saturday")
    has_number = re.search(rf"\b{NUM}\b", t, re.I) is not None
    if AMBIG.search(t) and (found or has_number):
        return "ambiguous", (max(values) if values else None)
    if len(values) == 1:
        return "count", values.pop()
    if len(values) > 1:
        return "unclear", None
    if ADJACENT.search(t):
        return "unclear", None
    return "none", None


def load_slack(path):
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("messages") or data.get("data") or []
    return data


def day_of(ts):
    return dt.datetime.fromtimestamp(float(ts), CHI).date().isoformat()


def norm_date(v):
    v = str(v).strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", v)
    if m:
        return f"{m[1]}-{m[2]}-{m[3]}"
    m = re.match(r"(?:\w+,?\s+)?(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", v)
    if m:
        y = int(m[3]) if m[3] else dt.date.today().year
        y = y + 2000 if y < 100 else y
        return dt.date(y, int(m[1]), int(m[2])).isoformat()
    m = re.match(r"(?:\w+,?\s+)?([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:,?\s+(\d{4}))?", v)
    if m:
        y = int(m[3]) if m[3] else dt.date.today().year
        return dt.datetime.strptime(f"{m[1][:3]} {m[2]} {y}", "%b %d %Y").date().isoformat()
    return None


def load_sheet(path):
    if path.lower().endswith(".json"):
        d = json.load(open(path, encoding="utf-8"))
        rows = d.get("values") if isinstance(d, dict) else d
    else:
        rows = list(csv.reader(open(path, newline="", encoding="utf-8-sig")))
    header = [h.strip() for h in rows[0]]
    out = {}
    for r in rows[1:]:
        if not r:
            continue
        r = list(r) + [""] * (len(header) - len(r))
        d = norm_date(r[0])
        if d:
            out[d] = {header[i]: str(r[i]).strip() for i in range(1, len(header))}
    return header, out


NOTES = {}  # (date, column) -> text of a cell that is not a number


def cell_int(v, where=None):
    """Number in a Sheet cell. Blank, "-" or any text (e.g. "Platform Down") counts as 0;
    text is recorded once as a NOTE and never changes the exit code."""
    raw = str(v or "").strip()
    t = raw.replace(",", "")
    if t in ("", "-"):
        return 0
    try:
        return int(float(t))
    except ValueError:
        if where is not None:
            NOTES.setdefault(where, raw)
        return 0


def main():
    ap = argparse.ArgumentParser(description="IB 500 recount: Slack count messages vs the Sheet Daily log (exported files in, no API calls).")
    ap.add_argument("--slack", required=True); ap.add_argument("--sheet", required=True)
    ap.add_argument("--date", help="YYYY-MM-DD (CT). Default: every date in the Slack file")
    ap.add_argument("--people", help="Slack id=Sheet column pairs, comma separated")
    ap.add_argument("--skip-ts", default="", help="ts values already resolved by hand")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    people = dict(DEFAULT_PEOPLE)
    if a.people:
        people = dict(p.split("=", 1) for p in a.people.split(","))
    skip = {s.strip() for s in a.skip_ts.split(",") if s.strip()}
    header, sheet = load_sheet(a.sheet)
    person_cols = [h for h in header[1:] if h.lower() not in ("day total", "running total", "target running total", "ahead/behind")]
    msgs = load_slack(a.slack)
    if not msgs:
        print("EMPTY_EXPORT: the Slack export has 0 messages. Empty is not zero; check the pull.", file=sys.stderr)
        return 2
    counts = defaultdict(int)
    asks, counted, unknown_people = [], [], set()
    dates = set()
    for m in msgs:
        ts = str(m.get("ts", ""))
        if not ts or ts in skip:
            continue
        d = day_of(ts)
        if a.date and d != a.date:
            continue
        dates.add(d)
        who = people.get(m.get("user", "")) or m.get("user_name") or m.get("user", "?")
        kind, n = classify(m.get("text", ""))
        if kind in ("ambiguous", "unclear"):
            asks.append({"date": d, "person": who, "ts": ts, "kind": kind, "text": m.get("text", "")[:200]})
        elif kind == "count":
            if who not in person_cols:
                unknown_people.add(who)
            counts[(d, who)] += n
            counted.append({"date": d, "person": who, "ts": ts, "count": n})
    if a.date:
        dates.add(a.date)
    diffs, total_issues = [], []
    running = 0
    for d in sorted(sheet):
        row = sheet[d]
        day_sum = sum(cell_int(row.get(p), (d, p)) for p in person_cols)
        running += day_sum
        if d not in dates:
            continue  # totals are only checked on the requested date(s); the running sum still covers every row
        if "Day total" in row and row["Day total"] != "" and cell_int(row["Day total"], (d, "Day total")) != day_sum:
            total_issues.append({"date": d, "cell": "Day total", "sheet": row["Day total"], "sum_of_people": day_sum})
        if "Running total" in row and row["Running total"] != "" and cell_int(row["Running total"], (d, "Running total")) != running:
            total_issues.append({"date": d, "cell": "Running total", "sheet": row["Running total"], "sum_of_people": running})
        for p in person_cols:
            s, c = cell_int(row.get(p), (d, p)), counts.get((d, p), 0)
            if s != c:
                why = [x for x in asks if x["date"] == d and x["person"] == p]
                diffs.append({"date": d, "person": p, "slack": c, "sheet": s,
                              "note": "has a message to ask about" if why else ""})
    for d in sorted(dates):
        if d not in sheet:
            if any(k[0] == d for k in counts):
                diffs.append({"date": d, "person": "*", "slack": sum(v for k, v in counts.items() if k[0] == d),
                              "sheet": None, "note": "no Sheet row for this date"})
    res = {"dates": sorted(dates), "counted_messages": len(counted), "differences": diffs,
           "ask_about": asks, "total_cell_issues": total_issues, "unknown_people": sorted(unknown_people),
           "notes": [{"date": d, "cell": c, "text": t} for (d, c), t in sorted(NOTES.items())],
           "slack_totals": {f"{d} {p}": v for (d, p), v in sorted(counts.items())}}
    n = len(diffs) + len(asks) + len(total_issues) + len(unknown_people)
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        for (d, c), t in sorted(NOTES.items()):
            print(f"NOTE {d} {c}: \"{t}\" is not a number, counted as 0")
    if a.json:
        pass
    elif n == 0:
        print(f"0 differences ({len(counted)} count messages, {len(res['dates'])} day(s)); Slack and the Sheet match")
    else:
        for x in diffs:
            print(f"DIFF {x['date']} {x['person']}: Slack {x['slack']} vs Sheet {x['sheet']} {('(' + x['note'] + ')') if x['note'] else ''}")
        for x in asks:
            print(f"ASK  {x['date']} {x['person']} ts {x['ts']} {x['kind']}: \"{x['text']}\"")
        for x in total_issues:
            print(f"TOTAL {x['date']} {x['cell']}: Sheet {x['sheet']} vs sum of person cells {x['sum_of_people']}")
        for p in sorted(unknown_people):
            print(f"PERSON {p}: counted in Slack but has no Sheet column")
        print(f"{n} exceptions")
    return 1 if n else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:
        print(f"ib500_recount error: {e}", file=sys.stderr)
        sys.exit(2)
