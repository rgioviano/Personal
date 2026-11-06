#!/usr/bin/env python3
"""promise_scan.py: find promises Ryne made in sent messages that look unfulfilled and are due. Exceptions only.

The bot gathers raw items with its connectors (Gmail, Quo, Slack, Otter) and saves them as JSON; this script
does the filtering. Read-only: it never calls an API or writes anything except stdout (and --out if given).

Inputs
  --sent FILE       messages Ryne sent: a JSON list, or {"messages": [...]}. Each item:
                    {"source": "gmail|quo|slack|otter", "id": "...", "thread_id": "...", "to": "Name <a@example.com>",
                     "date": "2026-10-22T14:07:35Z", "text": "...", "subject": "..."(optional)}
                    (threadId, body and snippet are accepted as aliases.)
  --activity FILE   later activity per thread or contact: a JSON list (or {"messages"/"activity": [...]}, or a dict
                    {thread_id: [items]}). Each item: {"thread_id", "date", "direction": "in|out", "from", "to"}.
                    direction may be left out when "from" is one of Ryne's addresses (MY_ADDRESSES) or labelIds has SENT.
                    The --sent messages also count as outbound activity.
  --gmail-thread F  raw Gmail get_thread output (repeatable, globs ok). Ryne's messages since --since go to sent,
                    every message goes to activity. Can be mixed with --sent/--activity.
Options
  --today YYYY-MM-DD   --now ISO      (default: now, America/Chicago)
  --since YYYY-MM-DD   only scan sent messages on/after this date (default: no limit)
  --grace-days N       a promise with no date is due N days after it was sent (default 1)
  --skip-file PATH     extra skip entries (default chief/promise_skip.txt next to this script)
  --show-dropped       also list dropped and not-yet-due promises
  --allow-empty        an empty --sent export is not an error
  --unanswered-hours N also list inbound messages with no later outbound in that thread/contact after N hours
                       (counts toward exit 1). Only as complete as the activity the bot exported.
Output: JSON with counts {messages_scanned, flagged, dropped_done, dropped_skip, dropped_waiting, not_due_yet,
remaining} and
the remaining overdue or due-today promises. Exit 0 none remaining, 1 remaining, 2 script error
(including an empty or unreadable export: empty is not zero).
"""
import argparse, datetime as dt, glob, json, os, re, sys
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

CT = ZoneInfo("America/Chicago")
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- editable lists -------------------------------------------------------------------------------------
# Action verbs that make "I'll / I will / we'll / I'm going to ..." a promise ("we'll test his movement" is not).
PROMISE_VERBS = ("send|email|text|call|get|set|have|follow|reach|check|look|find|ask|talk|put|add|update|book|"
                 "schedule|let you know|share|forward|write|make|sort|fix|take care|pause|hold|cancel|switch|"
                 "change|confirm|upload|review|figure|reply|respond|circle back|touch base|give|post|create|build|"
                 "draft|finish|loop|connect|work on|move|reschedule|refund|credit|charge|adjust|program")
PROMISE_PHRASES = [
    r"\bI(?:'ll| will| am going to|'m going to)\s+(?:\w+\s+){0,2}?(?:" + PROMISE_VERBS + r")\b",
    r"\bwe(?:'ll| will| are going to|'re going to)\s+(?:\w+\s+){0,2}?(?:" + PROMISE_VERBS + r")\b",
    r"\byes,? (?:I|we) can (?:certainly |definitely )?(?:" + PROMISE_VERBS + r"|put|add|pause|do)\b",
    r"\bwill get back\b", r"\bget back to you\b", r"\blet me (?:check|look|see|find|ask|confirm|double.check)\b",
    r"\bsend you the link\b", r"\bsend (?:it|that|them) over\b", r"\bI can send\b",
    r"\bby tomorrow\b", r"\bby (?:the )?end of (?:the )?(?:day|week)\b", r"\bby EOD\b", r"\bby tonight\b",
]
# A promise that waits on them first ("Once you do that, we'll send ..."): dropped as waiting on them
# unless they wrote back after it.
CONDITIONAL = [r"^\s*(?:if|once|when|after|as soon as)\b", r"\b(?:if|once|when|after|as soon as) (?:you|they|he|she)\b"]
# sentences that match a promise phrase but are not promises
NOT_PROMISE = [
    r"\bI'?ll see you\b", r"\bwe'?ll see you\b", r"\bsee you (?:then|there|soon|on|at|next|this|tomorrow)\b",
    r"\bI'?ll be (?:out|away|traveling|travelling|off|there|honest)\b", r"\bI will be (?:out|away|traveling|off|there)\b",
    r"\bwe'?ll (?:miss|be closed)\b", r"\bif (?:you|they|he|she) will\b", r"\bwill you\b", r"\bI wish\b",
]
# built-in skip list (Ryne, 2026-10-23): student observation requests.
# Named people are not stored in this file.
SKIP = ["North Central observation"]
SKIP_REGEX = [r"north\s+central.{0,80}observ", r"observ.{0,80}north\s+central"]
# Only addresses brain_lint already allows. Do not add a personal mailbox here.
MY_ADDRESSES = ["ryne@achievesportsperformance.com",
                "contact@achievesportsperformance.com", "contact@achieve-personaltraining.com"]
# ----------------------------------------------------------------------------------------------------------

PROMISE_RX = [re.compile(p, re.I) for p in PROMISE_PHRASES]
NOT_RX = [re.compile(p, re.I) for p in NOT_PROMISE]
COND_RX = [re.compile(p, re.I) for p in CONDITIONAL]
SKIP_RX = [re.compile(p, re.I | re.S) for p in SKIP_REGEX]
WD = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
EMAIL = re.compile(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+")
QUOTE_START = [re.compile(p, re.M | re.I) for p in [
    r"^\s*On\s[^\n]{0,200}?(?:\n[^\n]{0,200}?)?wrote:\s*$", r"^\s*-{2,}\s*Original Message\s*-{2,}",
    r"^\s*_{10,}\s*$", r"^\s*From:\s.*\n\s*(?:Sent|Date):\s", r"^\s*-{2,}\s*Forwarded message\s*-{2,}"]]
SIG = re.compile(r"^--\s*$", re.M)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def parse_date(v):
    if v is None or v == "":
        raise ValueError("missing date")
    if isinstance(v, (int, float)) or (isinstance(v, str) and v.isdigit()):
        n = float(v)
        return dt.datetime.fromtimestamp(n / 1000 if n > 1e11 else n, tz=dt.timezone.utc).astimezone(CT)
    s = str(v).strip()
    try:
        d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        d = parsedate_to_datetime(s)
    if d.tzinfo is None:
        d = d.replace(tzinfo=CT)
    return d.astimezone(CT)


def load_json(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if not raw.strip():
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:  # connector output saved with a wrapper around the JSON
        a, b = raw.find("{"), raw.rfind("}")
        a2, b2 = raw.find("["), raw.rfind("]")
        if a2 != -1 and (a == -1 or a2 < a):
            a, b = a2, b2
        return json.loads(raw[a:b + 1])


def as_list(d, keys=("messages", "activity", "items")):
    if d is None:
        return []
    if isinstance(d, list):
        return d
    for k in keys:
        if isinstance(d.get(k), list):
            return d[k]
    if all(isinstance(v, list) for v in d.values()):  # {thread_id: [items]}
        out = []
        for tid, items in d.items():
            for it in items:
                out.append({"thread_id": tid, **it})
        return out
    raise ValueError("unrecognised JSON layout (want a list or {'messages': [...]})")


def is_me(addr_field):
    a = (addr_field or "").lower()
    return any(m in a for m in MY_ADDRESSES)


def contacts(item):
    """Keys for 'same contact': emails, phone digits, else the normalised name."""
    keys = set()
    for f in ("to", "from", "contact", "participant", "phone"):
        v = item.get(f)
        if isinstance(v, list):
            v = ", ".join(map(str, v))
        if not v:
            continue
        for e in EMAIL.findall(str(v)):
            if not is_me(e):
                keys.add(e.lower())
        for p in re.findall(r"\+?\d[\d\s().-]{8,}\d", str(v)):
            digits = re.sub(r"\D", "", p)[-10:]
            if len(digits) == 10:
                keys.add(digits)
        if f in ("contact", "participant") and not EMAIL.search(str(v)):
            keys.add(norm(v))
    return {k for k in keys if k}


def body_of(m):
    return m.get("text") or m.get("body") or m.get("snippet") or ""


def strip_quoted(text):
    t = text.replace("\r\n", "\n").replace("\u2019", "'").replace("\u2018", "'")
    cut = len(t)
    for rx in QUOTE_START:
        m = rx.search(t)
        if m:
            cut = min(cut, m.start())
    s = SIG.search(t)
    if s:
        cut = min(cut, s.start())
    t = t[:cut]
    return "\n".join(l for l in t.split("\n") if not l.lstrip().startswith(">"))


def sentences(text):
    out = []
    for para in re.split(r"\n\s*\n", text):
        para = re.sub(r"\s+", " ", para).strip()
        if para:
            out.extend(s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", para) if s.strip())
    return out


def find_promise(sentence):
    if any(rx.search(sentence) for rx in NOT_RX) and not re.search(
            r"\b(send|get back|check|follow up|look into|find out|let you know)\b", sentence, re.I):
        return None
    if re.search(r"\?\s*$", sentence) and not re.search(r"\b(I'?ll|I will)\b", sentence, re.I):
        return None
    for rx in PROMISE_RX:
        m = rx.search(sentence)
        if m:
            return m.group(0)
    return None


def next_weekday(d, wd, skip_week=False):
    delta = (wd - d.weekday()) % 7
    if skip_week:
        delta += 7 if delta else 7
    return d + dt.timedelta(days=delta)


def due_date(sentence, sent_day, grace):
    s = sentence.lower()
    if re.search(r"\b(today|tonight|this (?:morning|afternoon|evening)|end of (?:the )?day|eod|later today)\b", s):
        return sent_day, "today"
    if re.search(r"\btomorrow\b", s):
        return sent_day + dt.timedelta(days=1), "tomorrow"
    m = re.search(r"\bin (\d+|a couple(?: of)?|a few) days\b", s)
    if m:
        n = {"a couple": 2, "a couple of": 2, "a few": 3}.get(m.group(1)) or int(m.group(1))
        return sent_day + dt.timedelta(days=n), m.group(0)
    m = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", s)
    if m:
        mo, da = int(m.group(1)), int(m.group(2))
        yr = int(m.group(3)) if m.group(3) else sent_day.year
        yr += 2000 if yr < 100 else 0
        try:
            d = dt.date(yr, mo, da)
            if not m.group(3) and (sent_day - d).days > 180:
                d = d.replace(year=yr + 1)
            return d, m.group(0)
        except ValueError:
            pass
    m = re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.? (\d{1,2})(?:st|nd|rd|th)?\b", s)
    if m:
        try:
            d = dt.date(sent_day.year, MONTHS[m.group(1)], int(m.group(2)))
            if (sent_day - d).days > 180:
                d = d.replace(year=d.year + 1)
            return d, m.group(0)
        except ValueError:
            pass
    m = re.search(r"\b(next|this)? ?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", s)
    if m:
        return next_weekday(sent_day, WD.index(m.group(2)), m.group(1) == "next"), m.group(0).strip()
    if re.search(r"\bthis weekend\b", s):
        return next_weekday(sent_day, 6), "this weekend"
    if re.search(r"\b(this week|end of (?:the )?week)\b", s):
        return next_weekday(sent_day, 4), "this week"
    if re.search(r"\bnext week\b", s):
        return next_weekday(sent_day, 4, True), "next week"
    if re.search(r"\bend of (?:the )?month\b", s):
        nm = (sent_day.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        return nm - dt.timedelta(days=1), "end of month"
    return sent_day + dt.timedelta(days=grace), f"no date (sent + {grace} day)"


def load_skip(path):
    entries, rx = list(SKIP), list(SKIP_RX)
    if path and os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower().startswith("re:"):
                rx.append(re.compile(line[3:].strip(), re.I | re.S))
            else:
                entries.append(line)
    return [norm(e) for e in entries if norm(e)], rx


def skip_hit(m, skip):
    entries, rx = skip
    hay = " ".join(str(m.get(k, "")) for k in ("to", "contact", "subject")) + " " + body_of(m)
    n = norm(hay)
    for e in entries:
        if e in n:
            return e
    for r in rx:
        if r.search(hay):
            return r.pattern
    return None


def from_gmail_threads(paths, since):
    sent, act = [], []
    for p in paths:
        d = load_json(p)
        if d is None:
            raise ValueError(f"empty Gmail thread export: {p}")
        for m in as_list(d):
            out = is_me(m.get("from")) or "SENT" in (m.get("labelIds") or [])
            item = {"source": "gmail", "id": m.get("id"), "thread_id": m.get("threadId") or d.get("id"),
                    "to": m.get("to", ""), "from": m.get("from", ""), "date": m.get("date"),
                    "subject": m.get("subject", ""), "text": body_of(m), "direction": "out" if out else "in"}
            if "DRAFT" in (m.get("labelIds") or []):
                continue
            act.append(item)
            if out and (not since or parse_date(item["date"]).date() >= since):
                sent.append(item)
    return sent, act


def direction(a):
    d = (a.get("direction") or "").lower()
    if d in ("out", "outbound", "outgoing", "sent"):
        return "out"
    if d in ("in", "inbound", "incoming", "received"):
        return "in"
    if is_me(a.get("from")) or "SENT" in (a.get("labelIds") or []):
        return "out"
    return "in"


def scan(sent, activity, now, grace=1, skip=None, since=None):
    skip = skip or load_skip(None)
    today = now.date()
    acts = []
    for a in list(activity) + [dict(s, direction="out") for s in sent]:
        try:
            acts.append((parse_date(a.get("date")), direction(a), a.get("thread_id") or a.get("threadId"),
                         contacts(a), a.get("id")))
        except Exception:
            continue
    counts = dict(messages_scanned=0, flagged=0, dropped_done=0, dropped_skip=0, dropped_waiting=0, not_due_yet=0, remaining=0)
    remaining, dropped = [], []
    seen_ids = set()
    for m in sent:
        if m.get("id") and m["id"] in seen_ids:
            continue
        seen_ids.add(m.get("id"))
        when = parse_date(m.get("date"))
        if since and when.date() < since:
            continue
        counts["messages_scanned"] += 1
        tid = m.get("thread_id") or m.get("threadId")
        keys = contacts(m)
        hit = skip_hit(m, skip)
        for sent_text in sentences(strip_quoted(body_of(m))):
            phrase = find_promise(sent_text)
            if not phrase:
                continue
            counts["flagged"] += 1
            due, basis = due_date(sent_text, when.date(), grace)
            rec = {"source": m.get("source", ""), "id": m.get("id"), "thread_id": tid, "to": m.get("to", ""),
                   "subject": m.get("subject", ""), "sent": when.strftime("%Y-%m-%d %H:%M CT"),
                   "promise": sent_text[:300], "phrase": phrase, "due": due.isoformat(), "due_basis": basis}
            if hit:
                counts["dropped_skip"] += 1
                dropped.append(dict(rec, reason=f"skip list ({hit})"))
                continue
            later_out = [x for x in acts if x[1] == "out" and x[0] > when and x[4] != m.get("id")
                         and ((tid and x[2] == tid) or (keys & x[3]))]
            if later_out:
                counts["dropped_done"] += 1
                first = min(later_out, key=lambda x: x[0])
                dropped.append(dict(rec, reason="later outbound " + first[0].strftime("%Y-%m-%d %H:%M CT")))
                continue
            if due > today:
                counts["not_due_yet"] += 1
                dropped.append(dict(rec, reason="not due yet"))
                continue
            later_in = [x for x in acts if x[1] == "in" and x[0] > when and ((tid and x[2] == tid) or (keys & x[3]))]
            if not later_in and any(rx.search(sent_text) for rx in COND_RX):
                counts["dropped_waiting"] += 1
                dropped.append(dict(rec, reason="conditional, waiting on them (no reply since)"))
                continue
            rec["status"] = "due today" if due == today else "overdue"
            rec["days_overdue"] = (today - due).days
            rec["they_replied_after"] = (min(later_in, key=lambda x: x[0])[0].strftime("%Y-%m-%d %H:%M CT")
                                         if later_in else None)
            remaining.append(rec)
    counts["remaining"] = len(remaining)
    remaining.sort(key=lambda r: (r["due"], r["sent"]))
    return counts, remaining, dropped


def unanswered(activity, sent, now, hours, skip):
    """Inbound messages with no later outbound in the same thread or to the same contact, older than `hours`."""
    rows = []
    for a in list(activity) + [dict(x, direction="out") for x in sent]:
        try:
            rows.append((parse_date(a.get("date")), direction(a), a.get("thread_id") or a.get("threadId"), contacts(a), a))
        except Exception:
            continue
    out, seen = [], set()
    for when, d, tid, keys, a in rows:
        if d != "in" or (now - when).total_seconds() < hours * 3600:
            continue
        if skip_hit(a, skip):
            continue
        if any(x[1] == "out" and x[0] > when and ((tid and x[2] == tid) or (keys & x[3])) for x in rows):
            continue
        k = tid or a.get("id")
        if k in seen:
            continue
        seen.add(k)
        later = [x for x in rows if x[1] == "in" and x[0] > when and tid and x[2] == tid]
        last = max([when] + [x[0] for x in later])
        out.append({"source": a.get("source", ""), "id": a.get("id"), "thread_id": tid, "from": a.get("from", ""),
                    "subject": a.get("subject", ""), "received": last.strftime("%Y-%m-%d %H:%M CT"),
                    "hours_waiting": int((now - last).total_seconds() // 3600),
                    "snippet": re.sub(r"\s+", " ", strip_quoted(body_of(a)))[:200]})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sent", action="append", default=[])
    ap.add_argument("--activity", action="append", default=[])
    ap.add_argument("--gmail-thread", action="append", default=[])
    ap.add_argument("--today")
    ap.add_argument("--now")
    ap.add_argument("--since")
    ap.add_argument("--grace-days", type=int, default=1)
    ap.add_argument("--skip-file", default=os.path.join(HERE, "promise_skip.txt"))
    ap.add_argument("--show-dropped", action="store_true")
    ap.add_argument("--allow-empty", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--unanswered-hours", type=float)
    a = ap.parse_args(argv)
    if a.now:
        now = parse_date(a.now)
    elif a.today:
        now = dt.datetime.combine(dt.date.fromisoformat(a.today), dt.time(23, 59), CT)
    else:
        now = dt.datetime.now(CT)
    since = dt.date.fromisoformat(a.since) if a.since else None
    sent, activity = [], []
    for p in a.sent:
        d = load_json(p)
        if d is None:
            raise ValueError(f"empty sent export: {p}")
        sent += as_list(d)
    for p in a.activity:
        d = load_json(p)
        if d is None:
            raise ValueError(f"empty activity export: {p}")
        activity += as_list(d)
    paths = [f for g in a.gmail_thread for f in (sorted(glob.glob(g)) or [g])]
    if paths:
        s2, a2 = from_gmail_threads(paths, since)
        sent += s2
        activity += a2
    if not sent and not a.allow_empty:
        raise ValueError("no sent messages in the export (empty is not zero; use --allow-empty if the window was truly quiet)")
    counts, remaining, dropped = scan(sent, activity, now, a.grace_days, load_skip(a.skip_file), since)
    res = {"now": now.strftime("%Y-%m-%d %H:%M CT"), "since": a.since, "counts": counts, "remaining": remaining}
    found = bool(remaining)
    if a.unanswered_hours is not None:
        ua = unanswered(activity, sent, now, a.unanswered_hours, load_skip(a.skip_file))
        res["counts"]["unanswered_inbound"] = len(ua)
        res["unanswered_inbound"] = ua
        found = found or bool(ua)
    if a.show_dropped:
        res["dropped"] = dropped
    txt = json.dumps(res, indent=2, ensure_ascii=False)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(txt + "\n")
    print(txt)
    return 1 if found else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"promise_scan error: {e}", file=sys.stderr)
        sys.exit(2)
