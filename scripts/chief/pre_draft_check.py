#!/usr/bin/env python3
"""pre_draft_check.py: the mechanical half of the Pre-draft check skill. READY or HELD + reasons.

Run it on a draft before it is shown to Ryne. The bot exports the data with its own connectors.
This script calls no API and sends nothing. Judgment (tone, facts, coaching hours, whether a
touch means drop or rewrite) stays with the bot.

HOLD (exit 1) on:
  recipient   name plus phone, or name plus email, does not match exactly one contact row
  touches     a real Gmail/Quo message to or from them in the last 48h, or since the draft was written
  times       every offered time, including each time in a list ("Wed 10/28 4pm or 6pm",
              "4, 5 or 6pm", "4pm/6pm"), must not have passed; a weekday next to a date uses that date,
              a weekday alone means its next occurrence on or after today; a weekday that does not match its date, also in
              parentheses ("Tuesday (10/21)"); a slot that overlaps a busy block (blocks whose title has
              the recipient's last name are their own booking and are ignored, in every mode)
  parent      "your son/daughter/child" when nothing confirms a parent (see below)
  price       a $ amount with no --price-source; with --first-touch, anything other than a single
              "Pricing starts at $X/mo" line backed by --price-source (Ryne 2026-10-23)
  age         draft written more than 48 hours ago
  style       draft_lint rules: em dash, "thanks for checking in", "reach out anytime"
  aurora      --kind ad: any Aurora that is not an exclusion. email/text: Aurora in ad or targeting
              wording only (same sentence rule as fleet_lint). An address line is fine.
  email end   (since 2026-10-23: the Gmail connector's create_draft does NOT add Ryne's signature, so a
              saved email draft must end with "Thanks,", a blank line, then the exact block below)
                Ryne Gioviano, MSEd, CSCS
                Owner, Achieve Sports Performance & Personal Training
                www.achievesportsperformance.com

                For scheduling or account questions:
                Contact@achieve-personaltraining.com | Text: 630.340.4114
              The full block PASSES (blank lines, extra spaces, &amp;/&nbsp; and htmlBody-derived text are
              tolerated). A partial or wrong block (name only, a missing line, a different phone/email/URL,
              extra lines after it) HOLDS and names the missing or wrong lines. Email only; texts never carry it.
              --no-signature: old rule for bodies checked without the signature: any typed signature
              (name, CSCS, Achieve block, URL) after the closing HOLDS.
  missing     a check whose export was not given is NOT CHECKED and holds (use --skip only when the
              bot did that check another way)
WARN (exit code unchanged):
  a time with no day or no am/pm ("See you at 5!") is NOT CHECKED (in --mode confirm a bare "at 5" counts
  as checked when 5am/5pm with its day is already in the draft); no Drafted time (the 48-hour check is
  approximate or not done); an offered slot later today
  (offer mode); Aurora as a town call-out in an email/text; a closing line that is not "Thanks,"
  (house style: the line just before the signature, or the last line when there is none; "Thanks!" or
  "See you at 5!" is allowed); an email with NO signature: "connector drafts need the full signature
  typed in" (not with --no-signature, never for texts); a confirm-mode time with no matching booking
  on the calendar.
A body given as HTML (a Gmail-style htmlBody: <div>...</div><div><br></div>) is turned into plain text first.
Every run prints the checks that passed.

Household contact: a To person not on the Sheet whose last name matches a row (that row's own email/phone empty or
different) and whose email/phone is on no other row is a WARN "household contact, confirm relation", not a hold.
An email/phone that belongs to a different row still HOLDS.

Parent is confirmed by any of: --parent-confirmed; a parent/guardian column on the row; the row's
Comments/Notes saying "Parent X." (how the 2026 tab records it) where X is the draft's To first name
("Parent Lisa." on a draft to Anthony HOLDS with that reason; an unnamed "parent" note still counts);
the lead's own message in --touches saying "my son/daughter/child/kid" (up to 4 words between, e.g.
"my high school freshman son"), including a WordPress Lead Form whose body names their email or phone.

DRAFT FILE: optional header lines, a blank line, then the body:
  To: Jordan Sample <jordan.sample@example.com>
  Phone: 555-01-0001
  Channel: email            (or text)
  Drafted: 2026-10-19 18:05 (CT)   a date with no time counts as end of that day
  Subject: ...
Command-line --name/--email/--phone/--channel/--drafted-at override the header.

--contacts  reading stops at the first row with a cell saying AVERAGES (the 2026 tab's summary
            table, row 287) and a note says where. The Sheet row(s): CSV, JSON list of objects, or Sheets values {"values": [[header], [row]]}.
            Name = First Name + Last Name (or a Name column); phone/email = any column with that word;
            Comments/Notes are read for the parent rule.
--touches   one or more files (repeat the flag or list several paths). A file with content but no
            readable message is ERROR, exit 2 (NOT CHECKED, never a pass); "No messages found" and an
            empty JSON list are 0 touches.
            JSON list (or {"messages": [...]}) of SENT or RECEIVED messages only:
              {"timestamp": "2026-10-20T19:42:00-05:00", "channel": "Gmail" | "Quo SMS",
               "direction": "in" | "out", "from": "...", "to": "...", "subject": "...", "text": "..."}
            timestamp may be ISO with offset, "YYYY-MM-DD HH:MM" (CT) or epoch seconds.
            Do NOT include unsent Gmail drafts (entries with "draft": true or a DRAFT label are dropped).
            WordPress Lead Form notifications ("Lead Form - Form Submission Notification", from
            wordpress@) are the inquiry itself, not a touch: they are ignored for the 48h rule but read
            for the parent rule.
            Gmail entries with "snippet" and no "text" are read from the snippet.
            Quo/Sona call or voicemail alert emails (from quo.com, e.g. "Sona handled a call from
            555-01-0001") are inbound touches from the caller: "they called <time> (Quo alert email)".
            Numa notification emails (from no-reply@example.com, subject "New conversation: ..." or
            "New message: ...", body ending "Sent by <name or phone> to Achieve ...") are inbound texts from
            that person, matched by phone or by full name in any order: "they texted <time> (Numa
            notification)". "Still waiting: ..." reminders are a note, not a touch. Gmail exports may use
            "sender" instead of "from".
            Quo: a plain-text .txt export is accepted. Each message line has a timestamp and a direction
            (in/out/incoming/outgoing) among | fields; these layouts are read:
              AC... | +16305550102 | incoming | 2026-10-20T19:42:00Z    (message text on the next line)
              AC... | incoming | 2026-10-20T19:42:00Z | message text   (under a "+1630... (conversation CN...)" line)
              2026-10-20 19:42 | in | +16305550102 | +16303404114 | message text
            "No messages found" is 0 touches. To use Quo JSON,
            map each message to the object above: createdAt -> timestamp, direction incoming/outgoing
            -> in/out, from, to, text.
--busy      one or more files (repeat the flag or list several paths), e.g. one per calendar.
            An event list where no event has a start/end is ERROR, exit 2.
            JSON list (or {"items": [...]} / {"events": [...]}) of calendar events:
              {"summary": "Eval - Chacon", "start": "2026-10-21T17:00:00-05:00", "end": "..."}
            start/end may also be Google's {"dateTime": ...} objects. Export ALL of Ryne's calendars
            for the days offered: Achieve (evals live here), Personal and Work.
--mode      offer (default), confirm or reply. reply (or --reply-to <message id>): the draft answers their
            newest inbound message (or the one with that id); that message and earlier ones in the thread are not
            touches, but any message after it still holds.
            offer (default) or confirm. confirm: the draft confirms a booked time, so no same-day warning,
            and it warns if no calendar block with the recipient's last name sits at that time.
--kind      email (default), text or ad. Controls the Aurora rule.
--workdir   folder that relative input paths are read from. Use a fresh per-run subfolder such as
            /workspace/predraft-test/<bot>-<person>-<timestamp>/ so bots never overwrite each other's files.

Usage:
  python3 pre_draft_check.py draft.txt --contacts row.csv --touches touches.json --busy busy.json
  options: --now "2026-10-21 09:00", --first-touch, --price-source "Penny's locked price sheet",
           --parent-confirmed, --slot-minutes 60, --skip touches,times,calendar,recipient, --json,
           --no-signature (body checked without Ryne's signature: old "Gmail adds it" rule)
Exit code: 0 READY (warnings allowed), 1 HELD, 2 script error.
"""
import argparse, csv, datetime as dt, html, importlib.util, json, os, re, sys
from zoneinfo import ZoneInfo

CHI = ZoneInfo("America/Chicago")
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("draft_lint", os.path.join(HERE, "draft_lint.py"))
draft_lint = importlib.util.module_from_spec(spec); spec.loader.exec_module(draft_lint)
STYLE_RULES = [r for r in draft_lint.RULES if r[0] not in ("price", "aurora")]
PRICE_RX = dict((r[0], r[1]) for r in draft_lint.RULES)["price"]

AURORA_RX = re.compile(r"\bAurora\b", re.I)
AD_WORDS = re.compile(r"\b(ads?|campaigns?|target(?:ing|ed)?|geo|radius|audience|Meta|Google Ads|boost)\b", re.I)
NEGATION = re.compile(r"\b(exclude[sd]?|excluding|not|never|no)\b", re.I)
ADDRESS_RX = re.compile(r"\b\d{2,6}\s+[A-Z][\w.]*(?:\s+[A-Z][\w.]*)*\s+(?:Drive|Dr|Road|Rd|Street|St|Avenue|Ave|Boulevard|Blvd|Lane|Ln|Way|Court|Ct|Parkway|Pkwy|Highway|Hwy|Place|Pl|Circle)\b"
                        r"|\bAurora,?\s+(?:IL|Illinois)\b|\b60[56]\d\d\b")
WD_FULL = "monday tuesday wednesday thursday friday saturday sunday".split()
WD_ABBR = {"Mon": 0, "Tue": 1, "Tues": 1, "Wed": 2, "Thu": 3, "Thur": 3, "Thurs": 3, "Fri": 4, "Sat": 5, "Sun": 6}
MONTHS = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}
ANCHOR = re.compile(
    r"(?:(?P<wdf>(?i:monday|tuesday|wednesday|thursday|friday|saturday|sunday))|(?P<wda>\b(?:Mon|Tues|Tue|Wed|Thurs|Thur|Thu|Fri|Sat|Sun)\b)\.?)?"
    r"(?:,?\s*\(?\s*(?:the\s+)?)?"
    r"(?:(?P<md>\b(?P<m>1[0-2]|0?[1-9])/(?P<d>3[01]|[12]\d|0?[1-9])(?:/(?P<y>\d{4}|\d{2}))?\b(?!/))"
    r"|(?P<mon>\b(?i:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?)\s+(?P<md2>3[01]|[12]\d|0?[1-9])(?:st|nd|rd|th)?\b(?:,?\s+(?P<y2>\d{4}))?)?"
    r"(?:\s*\))?"
    r"|(?P<rel>\b(?i:today|tonight|tomorrow)\b)")
TIME = re.compile(r"\b(?P<h>1[0-2]|0?[1-9])(?::(?P<mi>[0-5]\d))?\s*(?:-\s*(?:1[0-2]|0?[1-9])(?::[0-5]\d)?\s*)?(?P<ap>(?i:am|pm|a\.m\.|p\.m\.))|\b(?P<noon>(?i:noon))\b")
BARE_TIME = re.compile(r"\b(?:at|by|around|from)\s+(?:1[0-2]|0?[1-9])(?::[0-5]\d)?\b(?!\s*(?:am|pm|a\.m|p\.m|%|/|-?\s*(?:minutes?|mins?|weeks?|days?|hours?|x\b)))", re.I)
OFFER_WORDS = re.compile(r"\b(open|available|availability|works?|work for|how about|would|could|can you|slot|spot|either|or|book|come in|schedule)\b|\?", re.I)
PARENT_RX = re.compile(r"\b(your\s+(?:son|daughter|child|children|kid|kids|athlete|swimmer|player|boy|girl)s?|as\s+(?:a|his|her)\s+parent|you\s+and\s+your\s+(?:son|daughter|child|kid))\b", re.I)
PARENT_NAMED_RX = re.compile(r"\b(?i:(parent|mom|dad|mother|father|guardian))\s+([A-Z][a-z]+)")
PARENT_NOTE_RX = re.compile(r"(?<!not a )(?<!not )(?<!no )\b(parent|mom|dad|mother|father|guardian)\b", re.I)
MY_CHILD_RX = re.compile(r"\bmy\s+(?:\d+\s*(?:yo|year[- ]old)\s+)?(?:[A-Za-z0-9-]+\s+){0,4}?(?:son|daughter|child|children|kid|kids|boy|girl|swimmer|athlete)s?\b", re.I)
CLOSING_RX = re.compile(r"^\s*(?:thanks|thank you|thanks so much|thanks again|best|cheers|regards|talk soon|see you\b.*|looking forward\b.*|-\s*ryne)\s*[,!.]*\s*$", re.I)
SIG_RX = re.compile(r"(Ryne\s+Gioviano|\bRyne\b\s*$|\bCSCS\b|\bMSEd\b|Achieve\s+Sports\s+Performance|\bOwner\b|Head\s+(?:Strength\s+)?Coach|630[\s.-]?340[\s.-]?4114|achievesportsperformance\.com|www\.|^\s*-{2,}\s*$|Sent from my)", re.I | re.M)
# Ryne's email signature (since 2026-10-23 connector drafts must carry it typed in), compared line by line
SIGNATURE_LINES = [
    "Ryne Gioviano, MSEd, CSCS",
    "Owner, Achieve Sports Performance & Personal Training",
    "www.achievesportsperformance.com",
    "For scheduling or account questions:",
    "Contact@achieve-personaltraining.com | Text: 630.340.4114",
]
HTML_RX = re.compile(r"<\s*(?:div|br|p|span|html|body)\b[^>]*>", re.I)


def html_to_text(text):
    """Gmail-style htmlBody (one div per paragraph, <div><br></div> spacers) to plain text lines."""
    t = re.sub(r"(?is)<(script|style)\b.*?</\1\s*>", "", text)
    t = re.sub(r"(?i)<br\s*/?>", "\n", t)
    t = re.sub(r"(?i)</\s*(?:div|p|li|tr|h[1-6])\s*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t).replace("\xa0", " ")
    return re.sub(r"\n{3,}", "\n\n", t).strip("\n")


def sig_norm(line):
    t = html.unescape(line).replace("\xa0", " ").replace("\u2009", " ")
    t = re.sub(r"\s*\|\s*", " | ", t)
    t = re.sub(r"\s*,\s*", ", ", t)
    return re.sub(r"\s+", " ", t).strip().casefold()


SIG_NORM = [sig_norm(l) for l in SIGNATURE_LINES]


def check_signature(lines):
    """lines: body lines. Returns (status, closing_line, detail). status: full, partial, none, after (text after closing)."""
    nb = [l.strip() for l in lines if l.strip()]
    nn = [sig_norm(l) for l in nb]
    k = len(SIG_NORM)
    if len(nn) >= k and nn[-k:] == SIG_NORM:
        return "full", (nb[-k - 1] if len(nb) > k else ""), ""
    idx = max((i for i, l in enumerate(nb) if CLOSING_RX.match(l)), default=None)
    if idx is not None:
        after = nb[idx + 1:]
        if not after:
            return "none", nb[idx], ""
        if not SIG_RX.search("\n".join(after)):
            return "after", nb[idx], ""
        closing = nb[idx]
    else:
        tail_start = max(0, len(nb) - 8)
        start = next((i for i in range(tail_start, len(nb)) if len(nb[i]) < 80 and SIG_RX.search(nb[i])), None)
        if start is None:
            return "none", (nb[-1] if nb else ""), ""
        after, closing = nb[start:], (nb[start - 1] if start else "")
    got = [sig_norm(l) for l in after]
    missing = [SIGNATURE_LINES[i] for i, w in enumerate(SIG_NORM) if w not in got]
    wrong = [a for a, g in zip(after, got) if g not in SIG_NORM]
    parts = []
    if missing:
        parts.append("missing " + "; ".join(f'"{m}"' for m in missing))
    if wrong:
        parts.append("not in the signature " + "; ".join(f'"{w[:60]}"' for w in wrong))
    if not parts:
        parts.append("lines out of order or repeated")
    return "partial", closing, ", ".join(parts)


QUO_ALERT_FROM_RX = re.compile(r"@(?:[\w-]+\.)*(?:quo\.com|openphone\.(?:com|co))\b|\bThe Quo Team\b|\bSona\b", re.I)
QUO_ALERT_SUBJ_RX = re.compile(r"\b(?:handled a call|missed (?:a )?call|call from|called you|voicemail|new call)\b", re.I)
NUMA_FROM_RX = re.compile(r"@(?:[\w-]+\.)*(?:getnuma\.com|numa\.com)\b", re.I)
NUMA_NEW_RX = re.compile(r"^\s*New (?:conversation|message)\b", re.I)
NUMA_WAIT_RX = re.compile(r"^\s*Still waiting\b", re.I)
NUMA_SENT_BY_RX = re.compile(r"Sent by\s+(.+?)(?:\s+to\s+Achieve\b|\s+You can find\b|\s*$)", re.I)


def numa_sender(text):
    """Numa notification body/snippet ends 'Sent by <name or 555-01-0001> to Achieve ...'.
    Returns (name, phone10); 'Sent by you.' (Ryne's own message) returns (None, None)."""
    m = NUMA_SENT_BY_RX.search(re.sub(r"\s+", " ", text))
    if not m or re.match(r"you\b", m.group(1), re.I):
        return None, None
    who = m.group(1).strip().rstrip(".")
    ph = digits10(who) if re.fullmatch(r"[\d\s()+.-]{10,}", who) else ""
    return (None if ph else who), (ph or None)


LEAD_FORM_RX = re.compile(r"wordpress@|Lead Form\s*-|Form Submission Notification", re.I)


def parse_dt(s, end_of_day=False):
    """Returns (datetime, had_time)."""
    s = str(s).strip()
    if re.fullmatch(r"\d{9,11}(\.\d+)?", s):
        return dt.datetime.fromtimestamp(float(s), CHI), True
    s2 = re.sub(r"\(?\bCT\b\)?", "", s.replace("Z", "+00:00")).strip()
    for fmt in (None, "%Y-%m-%d %H:%M", "%Y-%m-%d %I:%M%p", "%Y-%m-%d %I:%M %p", "%m/%d/%Y %H:%M", "%m/%d/%Y %I:%M %p", "%m/%d/%y %H:%M"):
        try:
            d = dt.datetime.fromisoformat(s2) if fmt is None else dt.datetime.strptime(s2, fmt)
        except ValueError:
            continue
        if fmt is None and re.fullmatch(r"\d{4}-\d{2}-\d{2}", s2):
            break
        return (d.replace(tzinfo=CHI) if d.tzinfo is None else d.astimezone(CHI)), True
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            d = dt.datetime.strptime(s2, fmt)
        except ValueError:
            continue
        d = d.replace(hour=23, minute=59) if end_of_day else d
        return d.replace(tzinfo=CHI), False
    raise ValueError(f"unreadable date/time {s!r}")


def when(s):
    return parse_dt(s)[0]


def digits10(v):
    d = re.sub(r"\D", "", re.sub(r"\.0+$", "", str(v or "")))
    return d[-10:] if len(d) >= 10 else ""


def nname(v):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s'-]", " ", str(v or "")).strip()).casefold()


QUO_TS = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{1,2}:\d{2}")
QUO_DIR = re.compile(r"(?:in|out|incoming|outgoing|inbound|outbound|received|sent)", re.I)
QUO_PHONE = re.compile(r"\+?\d[\d\s().-]{8,}\d")
QUO_EMPTY = re.compile(r"no messages found|\b0 messages\b|no conversations found", re.I)


class ExportError(Exception):
    pass


def parse_quo_txt(text):
    """Quo plain text. Each message line has a timestamp and a direction among | fields, in any order:
      2026-10-20 19:42 | in | +16305550102 | +16303404114 | text        (timestamp | dir | from | to | text)
      AC123... | incoming | 2026-10-20T19:42:00Z | text                  (list-messages: id | dir | ts | text)
      AC123... | +16305550102 | incoming | 2026-10-20T19:42:00Z           (id | participant | dir | ts),
        message text on the next line(s)
    A "+1630... (conversation CN...)" header line names the participant for the lines under it."""
    rows, conv, pending = [], "", None
    for line in text.splitlines():
        st = line.strip()
        if not st or (st.startswith("<") and st.endswith(">")):
            pending = None if not st else pending
            continue
        if "|" not in st:
            hm = re.fullmatch(r"(\+?\d[\d\s().-]{8,}\d)\s*(?:\(conversation[^)]*\))?:?", st)
            if hm:
                conv, pending = hm.group(1), None
            elif pending is not None and not pending["text"]:
                pending["text"] = st
            elif pending is not None and pending.get("_cont"):
                pending["text"] += " " + st
            continue
        parts = [x.strip() for x in st.split("|")]
        ts_i = next((i for i, x in enumerate(parts) if QUO_TS.match(x)), None)
        dir_i = next((i for i, x in enumerate(parts) if QUO_DIR.fullmatch(x)), None)
        if ts_i is None or dir_i is None:
            continue
        phones = [x for i, x in enumerate(parts) if i not in (ts_i, dir_i) and QUO_PHONE.fullmatch(x)]
        rest = [x for i, x in enumerate(parts) if i > max(ts_i, dir_i) and x not in phones]
        d = parts[dir_i].lower()
        inbound = d in ("in", "incoming", "inbound", "received")
        mid = next((x for i, x in enumerate(parts) if i not in (ts_i, dir_i) and re.fullmatch(r"[A-Z]{2}[0-9a-f]{16,}", x)), None)
        r = {"timestamp": parts[ts_i], "direction": "in" if inbound else "out", "id": mid,
             "participant": " ".join(phones) or conv, "text": " | ".join(rest), "channel": "Quo SMS"}
        if len(phones) >= 2:
            r["from"], r["to"] = phones[0], phones[1]
        r["_cont"] = not r["text"]
        rows.append(r)
        pending = r
    for r in rows:
        r.pop("_cont", None)
    return rows


def load_rows(path):
    if path.lower().endswith(".txt"):
        return parse_quo_txt(open(path, encoding="utf-8").read())
    if path.lower().endswith(".json"):
        d = json.load(open(path, encoding="utf-8"))
        if isinstance(d, dict) and "values" in d:
            v = d["values"]; h = [str(x) for x in v[0]]
            return [dict(zip(h, list(r) + [""] * (len(h) - len(r)))) for r in v[1:]]
        if isinstance(d, dict):
            for k in ("rows", "data", "items", "messages", "events"):
                if isinstance(d.get(k), list):
                    return d[k]
            return [d]
        return d
    return list(csv.DictReader(open(path, newline="", encoding="utf-8-sig")))


def stop_at_averages(rows):
    """Contact rows end at the first row with a cell saying AVERAGES (the 2026 tab's summary table).
    Returns (rows, sheet_row_number_or_None); sheet row = list index + 2 (row 1 is the header)."""
    for i, r in enumerate(rows):
        vals = r.values() if isinstance(r, dict) else r
        if any(str(v).strip().upper() == "AVERAGES" for v in vals if v is not None):
            return rows[:i], i + 2
    return rows, None


def contact_view(r):
    keys = {k.lower().strip(): k for k in r if k}
    names, parents, last = set(), set(), ""
    fn = next((keys[k] for k in keys if k in ("first name", "first", "firstname")), None)
    ln = next((keys[k] for k in keys if k in ("last name", "last", "lastname")), None)
    if fn and ln and (r.get(fn) or r.get(ln)):
        names.add(nname(f"{r.get(fn, '')} {r.get(ln, '')}"))
        last = nname(r.get(ln, ""))
    for k, orig in keys.items():
        if ("name" in k and "first" not in k and "last" not in k and "user" not in k) or k in ("full name", "client", "athlete"):
            if any(p in k for p in ("parent", "guardian", "mom", "dad")):
                if r.get(orig): parents.add(nname(r[orig]))
            elif r.get(orig):
                names.add(nname(r[orig]))
    phones = {digits10(r[o]) for k, o in keys.items() if "phone" in k or k in ("mobile", "cell")} - {""}
    emails = {str(r[o]).strip().lower() for k, o in keys.items() if "email" in k and r.get(o)}
    rel = " ".join(str(r[o]) for k, o in keys.items() if any(p in k for p in ("parent", "guardian", "relationship")) and r.get(o))
    notes = " ".join(str(r[o]) for k, o in keys.items() if k in ("comments", "comment", "notes", "note") and r.get(o))
    return {"names": names, "parents": parents, "phones": phones, "emails": emails, "last": last,
            "parent_field": rel.strip(), "comments": notes}


def check_recipient(name, email, phone, contacts, warns_out=None):
    """Returns (holds, passed_text, record). A household contact (same last name, not on the Sheet,
    email/phone on no other row) is a WARN in warns_out, not a hold."""
    warns_out = [] if warns_out is None else warns_out
    if not name:
        return ["recipient: no name on the draft to match"], None, None
    if not (email or phone):
        return ["recipient: draft has a name but no phone or email to match on a second field"], None, None
    nn, em, ph = nname(name), (email or "").lower(), digits10(phone)
    views = [contact_view(r) for r in contacts]
    name_hits = [v for v in views if nn in v["names"] or nn in v["parents"]]
    full = [v for v in name_hits if (em and em in v["emails"]) or (ph and ph in v["phones"])]
    if len(full) == 1:
        rec, holds, used, skipped = full[0], [], [], []
        for label, mine, theirs, norm in (("email", em, rec["emails"], em), ("phone", ph, rec["phones"], ph)):
            if mine and theirs:
                if norm in theirs:
                    used.append(label)
                else:
                    holds.append(f"recipient: {label} does not match sheet")
            elif theirs and not mine:
                skipped.append(f"{label} check skipped: draft has no {label}, Sheet has one")
            elif mine and not theirs:
                skipped.append(f"{label} not on the Sheet row")
        text = f"recipient: name + {' + '.join(used)} match one Sheet row" + (f" ({'; '.join(skipped)})" if skipped else "")
        return holds, (None if holds else text), rec
    if len(full) > 1:
        return [f"recipient: {len(full)} records match {name}; possible duplicate, do not present"], None, None
    if name_hits:
        bits = [b for b, v in (("phone", ph), ("email", em)) if v]
        return [f"recipient: only the name matches; {' and '.join(bits)} do not match sheet"], None, None
    other = [v for v in views if (em and em in v["emails"]) or (ph and ph in v["phones"])]
    if other:
        return [f"recipient: phone/email belongs to a record named {sorted(other[0]['names'] or other[0]['parents'])[0].title()}, not {name}"], None, None
    last = nn.split(" ")[-1] if " " in nn else ""
    house = [v for v in views if last and v["last"] == last
             and not ((em and em in v["emails"]) or (ph and ph in v["phones"]))]
    if house:
        who = ", ".join(sorted(n.title() for v in house for n in sorted(v["names"])[:1]))
        warns_out.append(f"recipient: household contact, confirm relation: {name} is not on the Sheet; same last name as {who}"
                         f" (that row's email/phone is empty or different, and this {'email' if em else 'phone'} is on no other row)")
        return [], None, (house[0] if len(house) == 1 else None)
    first = nn.split(" ")[0]
    part = [v for v in views if any(n.split(" ")[0] == first for n in v["names"] | v["parents"])]
    return ["recipient: name only partly matches the sheet" if part else f"recipient: {name} not found in the contact export"], None, None


TS_KEYS = ("timestamp", "date", "time", "sent", "created", "createdat", "created_at", "ts", "internaldate")


def load_touch_files(paths):
    """All --touches files. A file with content but no readable message is an ExportError (exit 2)."""
    rows = []
    for path in paths:
        raw = open(path, encoding="utf-8").read()
        got = load_rows(path)
        good = [r for r in got if isinstance(r, dict) and any(str(k).lower() in TS_KEYS and r[k] for k in r)]
        body = "\n".join(l for l in raw.splitlines() if l.strip() and not (l.strip().startswith("<") and l.strip().endswith(">")))
        json_empty = path.lower().endswith(".json") and got in ([], [{}])
        if not good and body.strip() and not QUO_EMPTY.search(body) and not json_empty:
            raise ExportError(f"touches: NOT CHECKED, {os.path.basename(path)} has content but no message could be read "
                              "(layout not recognized). Fix the export; this is never a pass.")
        rows += good
    return rows


def touch_matches(r, em, ph, nn):
    kl = {k.lower(): k for k in r}
    who = " ".join(str(r[kl[k]]) for k in kl if k in ("from", "to", "contact", "participant", "participants", "name", "phone", "email", "with", "subject"))
    return bool((em and em in who.lower()) or (ph and ph in re.sub(r"\D", "", who)) or (nn and nn in nname(who))), kl


def row_id(r):
    for k in ("id", "message_id", "messageid", "msg_id"):
        for kk in r:
            if str(kk).lower() == k and r[kk]:
                return str(r[kk])
    return None


def check_touches(rows, email, phone, name, drafted, now, warns_out=None, reply_to=None, reply_mode=False):
    """Returns (holds, notes, parent_evidence); first-name-only Numa matches go to warns_out."""
    holds, notes, parent_ev = [], [], None
    warns_out = [] if warns_out is None else warns_out
    events = []  # (when, inbound, id, label if after the draft, label if in the last 48h)
    em, ph, nn = (email or "").lower(), digits10(phone), nname(name)
    skipped_forms = skipped_drafts = 0
    for r in rows:
        if not isinstance(r, dict):
            continue
        hit, kl = touch_matches(r, em, ph, nn)
        get = lambda k: str(r.get(kl.get(k, ""), "") or "")
        text = get("text") or get("body") or get("snippet")
        blob = get("subject") + " " + text
        frm = get("from") or get("sender")
        numa_new = bool(NUMA_FROM_RX.search(frm)) and bool(NUMA_NEW_RX.match(get("subject")))
        numa_wait = bool(NUMA_FROM_RX.search(frm)) and bool(NUMA_WAIT_RX.match(get("subject")))
        if numa_new or numa_wait:
            # Numa notification email: a text from the person named after "Sent by" (match by phone or full name)
            s_name, s_ph = numa_sender(text)
            toks = set(nn.split())
            them = bool((ph and s_ph == ph) or (s_name and len(toks) >= 2 and toks <= set(nname(s_name).split())))
            maybe = bool(not them and s_name and toks and len(nname(s_name).split()) == 1 and nname(s_name) == nn.split()[0])
            if not them and not maybe:
                continue
            ts = next((r[kl[k]] for k in TS_KEYS if k in kl and r[kl[k]]), None)
            if not ts:
                continue
            w = when(ts)
            stamp = f"{w.strftime('%-m/%-d %-I:%M%p').lower()} CT"
            if maybe:
                warns_out.append(f"touches: Numa notification {stamp} is from \"{s_name}\" (first name only, no phone); "
                                 "it may be them, read the Numa thread")
                continue
            if numa_wait:
                notes.append(f"touches: Numa 'Still waiting' reminder {stamp} says they are waiting on a reply "
                             "(a reminder, not a new text; read the Numa thread)")
                continue
            if MY_CHILD_RX.search(text) and not parent_ev:
                parent_ev = f"their own Numa text says \"{MY_CHILD_RX.search(text).group(0)}\""
            events.append((w, True, row_id(r), f"they texted {stamp} (Numa notification)", f"they texted {stamp} (Numa notification)"))
            continue
        form_names_them = bool(LEAD_FORM_RX.search(frm + " " + get("subject"))) and bool(
            (em and em in text.lower()) or (ph and ph in re.sub(r"\D", "", text)))
        if not hit and not form_names_them:
            continue
        direction = get("direction").lower()
        is_call_alert = bool(QUO_ALERT_FROM_RX.search(frm)) and bool(QUO_ALERT_SUBJ_RX.search(get("subject") + " " + text[:200]))
        inbound = is_call_alert or direction in ("in", "inbound", "incoming", "received") or bool(frm and ((em and em in frm.lower()) or (ph and ph in re.sub(r"\D", "", frm))))
        is_form = bool(LEAD_FORM_RX.search(frm + " " + get("subject")))
        if (inbound or is_form) and MY_CHILD_RX.search(blob) and not parent_ev:
            parent_ev = f"their own {'Lead Form' if is_form else 'message'} says \"{MY_CHILD_RX.search(blob).group(0)}\""
            if is_form:
                notes.append("touches: Lead Form names their email/phone, so its wording counts as their own words "
                             "for the parent check (still not a touch)")
        labels = str(r.get(kl.get("labels", ""), "") or "") + " " + str(r.get(kl.get("labelids", ""), "") or "")
        if r.get(kl.get("draft", "")) is True or "DRAFT" in labels.upper() or direction == "draft":
            skipped_drafts += 1
            continue
        if is_form:
            skipped_forms += 1
            continue
        ts = next((r[kl[k]] for k in TS_KEYS if k in kl and r[kl[k]]), None)
        if not ts:
            continue
        w = when(ts)
        stamp = f"{w.strftime('%-m/%-d %-I:%M%p').lower()} CT"
        if is_call_alert:
            # a Quo/Sona call or voicemail alert email is the caller reaching out, not an outbound email
            events.append((w, True, row_id(r), f"they called {stamp} (Quo alert email)", f"they called {stamp} (Quo alert email)"))
            continue
        label = f"{stamp} via {get('channel') or ('Gmail' if ('threadid' in kl or 'labelids' in kl) else 'message')}"
        events.append((w, inbound, row_id(r), f"{'they replied' if inbound else 'already contacted'} {label}",
                       f"{'message from them' if inbound else 'already contacted'} {label}"))
    # --mode reply / --reply-to: the message being answered is not a touch; anything after it still holds
    answered = None
    if reply_to:
        answered = next((e for e in events if e[2] == reply_to), None)
        if answered is None:
            holds.append(f"touches: --reply-to {reply_to} is not in the touches export (check the message id)")
    elif reply_mode:
        answered = max((e for e in events if e[1]), key=lambda e: e[0], default=None)
        if answered is None:
            notes.append("touches: --mode reply but no inbound message from them was found to answer")
    earlier = 0
    for e in events:
        w = e[0]
        if answered is not None and (e is answered or w <= answered[0]):
            earlier += e is not answered
            continue
        if drafted and w > drafted:
            holds.append(f"touches: {e[3]}, after the draft was written")
        elif now - w <= dt.timedelta(hours=48) and w <= now:
            holds.append(f"touches: {e[4]} (last 48 hours)")
    if answered is not None:
        notes.append(f"touches: replying to their {answered[0].strftime('%-m/%-d %-I:%M%p').lower()} CT message "
                     f"(the message being answered is not a touch)" + (f"; {earlier} earlier message(s) in the thread ignored" if earlier else ""))
    if skipped_forms:
        notes.append(f"touches: {skipped_forms} WordPress Lead Form notification(s) ignored (the inquiry, not a touch)")
    if skipped_drafts:
        notes.append(f"touches: {skipped_drafts} unsent draft(s) ignored; leave drafts out of --touches")
    return holds, notes, parent_ev


def resolve_year(m, d, y, ref):
    if y:
        y = int(y); return y + 2000 if y < 100 else y
    cand = dt.date(ref.year, m, d)
    return ref.year + 1 if (ref.date() - cand).days > 180 else ref.year


_ITEM = r"(?:1[0-2]|0?[1-9])(?::[0-5]\d)?(?:\s*-\s*(?:1[0-2]|0?[1-9])(?::[0-5]\d)?)?(?:\s*(?:am|pm|a\.m\.|p\.m\.))?"
TIME_LIST = re.compile(rf"(?<![\w/:.]){_ITEM}(?:\s*(?:,\s*or|,|/|\bor\b|\band\b|&)\s*{_ITEM})*(?![\w/:])", re.I)
NOON = re.compile(r"\bnoon\b", re.I)


def iter_times(line):
    """Yield (start, end, [(h24, minute, label), ...]) for each time or time list on the line.
    "4pm or 6pm", "4, 5 or 6pm", "4pm/6pm", "4 or 6pm": every time is returned; a time with no
    am/pm takes it from the nearest one after it (else before it). Lists with no am/pm at all are skipped."""
    for m in TIME_LIST.finditer(line):
        parts = [x.strip() for x in re.split(r"\s*(?:,\s*or|,|/|\bor\b|\band\b|&)\s*", m.group(0), flags=re.I) if x.strip()]
        parsed = []
        for x in parts:
            pm = re.match(r"(1[0-2]|0?[1-9])(?::([0-5]\d))?(?:\s*-\s*(?:1[0-2]|0?[1-9])(?::[0-5]\d)?)?\s*(am|pm|a\.m\.|p\.m\.)?$", x, re.I)
            if not pm:
                parsed = []
                break
            parsed.append([int(pm.group(1)), int(pm.group(2) or 0), (pm.group(3) or "").lower()[:1], x])
        if not parsed or not any(p[2] for p in parsed):
            continue
        for k, p in enumerate(parsed):
            if not p[2]:
                nxt = next((q[2] for q in parsed[k + 1:] if q[2]), None)
                p[2] = nxt or next(q[2] for q in reversed(parsed[:k]) if q[2])
        out = [((h % 12) + (12 if ap == "p" else 0), mi, lab if re.search(r"[ap]\.?m", lab, re.I) else f"{lab}{ap}m")
               for h, mi, ap, lab in parsed]
        yield m.start(), m.end(), out
    for m in NOON.finditer(line):
        yield m.start(), m.end(), [(12, 0, "noon")]


def make_day(a, ref, today):
    issues, day, wd = [], None, None
    if a.group("wdf"):
        wd = WD_FULL.index(a.group("wdf").lower())
    elif a.group("wda"):
        wd = WD_ABBR[a.group("wda")]
    if a.group("md"):
        m, d = int(a.group("m")), int(a.group("d"))
        day = dt.date(resolve_year(m, d, a.group("y"), ref), m, d)
    elif a.group("mon"):
        m, d = MONTHS[a.group("mon").lower()[:3]], int(a.group("md2"))
        day = dt.date(resolve_year(m, d, a.group("y2"), ref), m, d)
    elif a.group("rel"):
        day = ref.date() + dt.timedelta(days=1 if a.group("rel").lower() == "tomorrow" else 0)
    elif wd is not None:
        # weekday with no date: the next occurrence on or after today
        day = today + dt.timedelta(days=(wd - today.weekday()) % 7)
    if day and wd is not None and (a.group("md") or a.group("mon")) and day.weekday() != wd:
        issues.append(f"{day.strftime('%-m/%-d')} is a {day.strftime('%A')}, not a {WD_FULL[wd].title()}")
    return day, issues, re.sub(r"\s+", " ", a.group(0)).strip()


def make_slot(a, t, ref, today):
    day, issues, text = make_day(a, ref, today)
    w = None
    if t is not None:
        h, mi, lab = t
        w = dt.datetime(day.year, day.month, day.day, h, mi, tzinfo=CHI)
        text = f"{text} {lab}"
    return {"text": text, "date": day.isoformat() if day else None, "when": w, "issues": list(issues)}


def find_slots(body, ref, confirm, today=None):
    today = today or ref.date()
    slots, unchecked, bare = [], [], []
    for line in body.splitlines():
        anchors = [a for a in ANCHOR.finditer(line) if any(a.group(g) for g in ("wdf", "wda", "md", "mon", "rel"))]
        used, paired_spans = set(), []
        for ts, te, times in iter_times(line):
            best = None
            for i, a in enumerate(anchors):
                gap = line[a.end():ts]
                if 0 <= ts - a.end() <= 25 and not re.search(r"[.!?;]|\bor\b|\band\b|/", gap.replace("at", "")):
                    best = i
                elif best is None and 0 <= a.start() - te <= 15 and re.fullmatch(r"\s*(on\s+|this\s+|next\s+)?", line[te:a.start()]):
                    best = i
            if best is None:
                unchecked.append(f"time with no day: \"{line[ts:te].strip()}\"")
                continue
            used.add(best)
            paired_spans.append((ts, te))
            for t in times:
                sl = make_slot(anchors[best], t, ref, today)
                sl["offer"] = confirm or bool(OFFER_WORDS.search(line))
                slots.append(sl)
        for m in BARE_TIME.finditer(line):
            if not any(s <= m.end() and m.start() <= e for s, e in paired_spans):
                bare.append((int(re.search(r"\d+", m.group(0)).group(0)), m.group(0).strip()))
        for i, a in enumerate(anchors):
            if i in used:
                continue
            if any(s <= a.start() < e for s, e in paired_spans):
                continue
            if OFFER_WORDS.search(line) or (a.group("md") or a.group("mon")) and (a.group("wdf") or a.group("wda")):
                sl = make_slot(a, None, ref, today)
                sl["offer"] = bool(OFFER_WORDS.search(line))
                slots.append(sl)
    # confirm mode: a bare "at 5" is the same time when 5am/5pm already appears with its day
    for h, txt in bare:
        if confirm and any(sl.get("when") and sl["when"].hour % 12 == h % 12 for sl in slots):
            continue
        unchecked.append(f"time with no am/pm or day: \"{txt}\"")
    return slots, unchecked


def load_busy(path):
    out = []
    for r in load_rows(path):
        s, e = r.get("start"), r.get("end")
        if isinstance(s, dict):
            s = s.get("dateTime") or s.get("date")
        if isinstance(e, dict):
            e = e.get("dateTime") or e.get("date")
        if s and e:
            out.append((when(s), when(e), str(r.get("summary") or r.get("title") or "busy")))
    return out


def split_draft(text):
    hdr, lines, i = {}, text.splitlines(), 0
    while i < len(lines) and re.match(r"^(To|Phone|Email|Channel|Drafted|Subject|Name)\s*:", lines[i], re.I):
        k, v = lines[i].split(":", 1)
        hdr[k.strip().lower()] = v.strip()
        i += 1
    if hdr and i < len(lines) and not lines[i].strip():
        i += 1
    return hdr, ("\n".join(lines[i:]) if hdr else text)


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+|\n", text) if s.strip()]


def export_error(a, msg):
    if a.json:
        print(json.dumps({"verdict": "ERROR", "reasons": [msg], "warnings": [], "passed": [], "notes": []}, indent=2))
    else:
        print("ERROR: " + msg)
    return 2


def main():
    ap = argparse.ArgumentParser(description="Pre-draft check: mechanical checks on a draft before Ryne sees it (exported files in, no API calls).",
                                 epilog=__doc__.split("DRAFT FILE:", 1)[1], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", nargs="?", help="draft text file (default stdin)")
    ap.add_argument("--name"); ap.add_argument("--email"); ap.add_argument("--phone")
    ap.add_argument("--channel", choices=["email", "text"])
    ap.add_argument("--kind", choices=["email", "text", "ad"], default=None, help="default: the channel, else email")
    ap.add_argument("--mode", choices=["offer", "confirm", "reply"], default="offer",
                    help="reply: answering their newest inbound message, which is then not a touch")
    ap.add_argument("--reply-to", help="id of the message being answered (Gmail/Quo id in --touches); implies --mode reply")
    ap.add_argument("--drafted-at"); ap.add_argument("--now")
    ap.add_argument("--contacts"); ap.add_argument("--touches", nargs="+", action="extend", help="one or more files; repeat the flag or list several paths")
    ap.add_argument("--busy", nargs="+", action="extend", help="one or more files (Achieve, Personal, Work); repeat or list several")
    ap.add_argument("--workdir", help="read relative input paths from here; use a per-run subfolder like /workspace/predraft-test/<bot>-<person>-<timestamp>/")
    ap.add_argument("--slot-minutes", type=int, default=60)
    ap.add_argument("--first-touch", action="store_true"); ap.add_argument("--price-source")
    ap.add_argument("--parent-confirmed", action="store_true")
    ap.add_argument("--skip", default="", help="checks done another way: recipient,touches,times,calendar")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-signature", action="store_true",
                    help="the body is checked without Ryne's signature (old rule: any typed signature after the closing HOLDS)")
    a = ap.parse_args()
    P = lambda p: p if (not p or not a.workdir or os.path.isabs(p)) else os.path.join(a.workdir, p)
    raw = open(P(a.draft), encoding="utf-8").read() if a.draft and a.draft != "-" else sys.stdin.read()
    hdr, body = split_draft(raw)
    if HTML_RX.search(body):
        body = html_to_text(body)
    to = hdr.get("to", "")
    m = re.match(r"\s*(.*?)\s*<([^>]+)>", to)
    name = a.name or hdr.get("name") or (m.group(1) if m else (to if "@" not in to else ""))
    email = a.email or hdr.get("email") or (m.group(2) if m else (to if "@" in to else ""))
    phone = a.phone or hdr.get("phone")
    channel = a.channel or (hdr.get("channel", "").lower() or ("email" if email and not phone else "text"))
    kind = a.kind or ("text" if channel == "text" else "email")
    now = parse_dt(a.now)[0] if a.now else dt.datetime.now(CHI)
    held, warns, passed, notes = [], [], [], []
    drafted = None
    if a.drafted_at or hdr.get("drafted"):
        drafted, had_time = parse_dt(a.drafted_at or hdr["drafted"], end_of_day=True)
        if not had_time:
            warns.append(f"age: Drafted has a date but no time, so the 48-hour check is approximate (treated as end of day {drafted.strftime('%-m/%-d')} 11:59pm)")
    skip = {s.strip() for s in a.skip.split(",") if s.strip()}
    rec = None
    # 1 recipient
    if "recipient" in skip:
        notes.append("recipient: skipped by the bot (--skip)")
    elif a.contacts:
        crow, stop = stop_at_averages(load_rows(P(a.contacts)))
        if stop:
            notes.append(f"contacts: stopped at sheet row {stop} (\"AVERAGES\" summary table); {len(crow)} contact rows read")
        h, ptxt, rec = check_recipient(name, email, phone, crow, warns)
        held += h
        if ptxt: passed.append(ptxt)
    else:
        held.append("recipient: NOT CHECKED (no contact export given)")
    # 2 touches
    parent_ev = None
    if "touches" in skip:
        notes.append("touches: skipped by the bot (--skip)")
    elif a.touches:
        try:
            trows = load_touch_files([P(x) for x in a.touches])
        except ExportError as e:
            return export_error(a, str(e))
        h, n, parent_ev = check_touches(trows, email, phone, name, drafted, now, warns,
                                        reply_to=a.reply_to, reply_mode=(a.mode == "reply" or bool(a.reply_to)))
        held += h; notes += n
        if not h: passed.append("touches: no Gmail/Quo touch in the last 48h or since the draft")
    else:
        held.append("touches: NOT CHECKED (no Gmail/Quo touch export given)")
    # 3 times
    slots, unchecked = find_slots(body, drafted or now, a.mode == "confirm", now.date())
    for u in unchecked:
        warns.append(f"times: NOT CHECKED, {u}")
    busy = None
    if a.busy:
        busy = []
        for bf in a.busy:
            got = load_busy(P(bf))
            if not got and load_rows(P(bf)) not in ([], [{}]):
                return export_error(a, f"calendar: NOT CHECKED, {os.path.basename(bf)} has events but none could be read (no start/end)")
            busy += got
    lasts = {x for x in ({nname(name).split(" ")[-1]} if name and " " in nname(name) else set()) | ({rec["last"]} if rec and rec["last"] else set()) if len(x) >= 3}
    own = lambda title: any(re.search(rf"\b{re.escape(l)}\b", nname(title)) for l in lasts)
    time_holds = 0
    for s in slots:
        for i in s["issues"]:
            held.append(f"times: {s['text']}: {i}"); time_holds += 1
        if "times" in skip:
            continue
        if s["when"] is not None:
            if s["when"] <= now:
                if s.get("offer"):
                    held.append(f"times: offered time passed: {s['text']}"); time_holds += 1
                else:
                    notes.append(f"times: past time mentioned (not in an offer sentence, bot to judge): {s['text']}")
                continue
            if s["when"].date() == now.date() and a.mode in ("offer", "reply") and s.get("offer"):
                warns.append(f"times: {s['text']} is later today (same-day offer)")
            if busy is not None and "calendar" not in skip:
                end = s["when"] + dt.timedelta(minutes=a.slot_minutes)
                over = [b for b in busy if b[0] < end and b[1] > s["when"]]
                mine = [b for b in over if own(b[2])]
                clash = [b for b in over if not own(b[2])]
                if clash:
                    held.append(f"times: {s['text']} is no longer open (calendar: {clash[0][2]})"); time_holds += 1
                if mine:
                    notes.append(f"times: {s['text']} overlaps their own booking \"{mine[0][2]}\" (ignored)")
                if a.mode == "confirm" and not any(b[0] == s["when"] or (b[0] <= s["when"] < b[1]) for b in mine):
                    warns.append(f"times: confirm mode, no calendar block with their last name at {s['text']}")
        elif s["date"] and dt.date.fromisoformat(s["date"]) < now.date() and s.get("offer"):
            held.append(f"times: offered day passed: {s['text']}"); time_holds += 1
    timed = [s for s in slots if s["when"]]
    if timed and busy is None and not ({"calendar", "times"} & skip):
        held.append("times: calendar NOT CHECKED (no busy-times export given)")
    elif timed and not time_holds and "times" not in skip:
        passed.append(f"times: {len(timed)} time(s) in the future" + ("" if "calendar" in skip else ", weekday/date agree, no calendar clash"))
    elif not slots:
        passed.append("times: no offered day or time found")
    # 4 parent
    pm = PARENT_RX.search(body)
    if pm:
        why = None
        if a.parent_confirmed: why = "--parent-confirmed"
        elif rec and (rec["parent_field"] or rec["parents"]): why = "parent column on the Sheet row"
        named_bad = None
        if not why and rec and PARENT_NOTE_RX.search(rec["comments"]):
            named = [(m.group(0), m.group(2)) for m in PARENT_NAMED_RX.finditer(rec["comments"])]
            to_first = nname(name).split(" ")[0] if name else ""
            if named:
                hit = next((t for t, fn in named if nname(fn) == to_first), None)
                if hit: why = f"Sheet Comments say \"{hit}\" (matches the To name)"
                else: named_bad = named[0][0]
            else:
                why = f"Sheet Comments say \"{PARENT_NOTE_RX.search(rec['comments']).group(0)}\""
        if not why and parent_ev: why = parent_ev
        if why:
            passed.append(f"parent: \"{pm.group(0)}\" confirmed by {why}")
        elif named_bad:
            held.append(f"parent: says \"{pm.group(0)}\" but Sheet Comments say \"{named_bad}\", not {(name or '?').split(' ')[0]} (the To name); check who this draft is to")
        else:
            held.append(f"parent: says \"{pm.group(0)}\" but nothing confirms a parent (Sheet row, Comments, or their own message)")
    else:
        passed.append("parent: no son/daughter/parent wording")
    # 5 price
    prices = [x.group(0) for x in PRICE_RX.finditer(body)]
    if prices:
        starts_at = len(prices) == 1 and re.search(r"(?:pricing|prices?|rates?|it)?\s*starts?\s+at\s+" + re.escape(prices[0]), body, re.I)
        if a.first_touch and starts_at and a.price_source:
            passed.append(f"price: one 'starts at' line, read live today from {a.price_source} (Ryne 2026-10-23)")
        elif a.first_touch and starts_at:
            held.append(f"price: 'starts at {prices[0]}' allowed in lead emails, but name the live source (--price-source)")
        elif a.first_touch:
            held.append(f"price: {prices[0]} in a first-touch/inbound reply (only one 'Pricing starts at $X/mo' line is allowed)")
        elif not a.price_source:
            held.append(f"price: {prices[0]} with no live source named (--price-source)")
        else:
            passed.append(f"price: read live today from {a.price_source}")
    else:
        passed.append("price: no $ amounts")
    # 6 age
    if drafted and now - drafted > dt.timedelta(hours=48):
        held.append(f"age: draft is {(now - drafted).days} days old (written {drafted.strftime('%-m/%-d')}); re-check or drop")
    elif drafted:
        passed.append("age: under 48 hours old")
    else:
        warns.append("age: no Drafted time given, so the 48-hour check was not done (add a Drafted: line)")
    # style
    n_style = 0
    for ln, line in enumerate(body.splitlines(), 1):
        for rid, rx, why in STYLE_RULES:
            if rid == "thank-you-for-checking-in" and STYLE_RULES[[r[0] for r in STYLE_RULES].index("thanks-for-checking-in")][1].search(line):
                continue
            if rx.search(line):
                held.append(f"style: line {ln} {rid} ({why})"); n_style += 1
    if not n_style:
        passed.append("style: no em dash or banned phrases")
    # aurora
    n_aur = 0
    for s in sentences(body):
        if not AURORA_RX.search(s) or NEGATION.search(s):
            continue
        n_aur += 1
        if kind == "ad":
            held.append(f"aurora: Aurora in ad copy (marketing targets Naperville): \"{s.strip()[:60]}\"")
        elif AD_WORDS.search(s):
            held.append(f"aurora: Aurora in ad or targeting wording: \"{s.strip()[:60]}\"")
        elif ADDRESS_RX.search(s):
            notes.append("aurora: Aurora in an address line (fine)")
        else:
            warns.append(f"aurora: Aurora used as a town call-out: \"{s.strip()[:60]}\"")
    if not any(h.startswith("aurora") for h in held):
        passed.append("aurora: no Aurora in ad or targeting wording")
    # email ending
    if channel == "email" and a.no_signature:
        lines = body.rstrip().splitlines()
        idx = max((i for i, l in enumerate(lines) if CLOSING_RX.match(l)), default=None)
        after = [l for l in lines[idx + 1:] if l.strip()] if idx is not None else []
        tail = [l for l in lines if l.strip()][-3:]
        if after and SIG_RX.search("\n".join(after)):
            held.append("email end: typed signature after the closing (--no-signature: this body should have none)")
        elif idx is None and any(len(l) < 80 and SIG_RX.search(l) for l in tail):
            held.append("email end: typed signature block at the end (--no-signature: this body should have none)")
        else:
            passed.append("email end: no typed signature (--no-signature)")
            if after:
                warns.append("email end: text after the closing line")
        last = next((l.strip() for l in reversed(lines) if l.strip()), "")
        if last != "Thanks,":
            warns.append(f"email end: ends with \"{last[:40]}\", house style is \"Thanks,\"")
    elif channel == "email":
        status, closing, detail = check_signature(body.rstrip().splitlines())
        if status == "full":
            passed.append("email end: full signature block after the closing")
        elif status == "partial":
            held.append(f"email end: partial or wrong signature ({detail}); connector drafts need the full block typed in")
        else:
            warns.append("email end: no signature; connector drafts need the full signature typed in")
            if status == "after":
                warns.append("email end: text after the closing line")
        if closing != "Thanks,":
            where = "the line before the signature" if status in ("full", "partial") else "ends with"
            shown = closing[:40] if closing else "(nothing)"
            warns.append(f"email end: {where} \"{shown}\", house style is \"Thanks,\"")
    verdict = "HELD" if held else "READY"
    res = {"verdict": verdict, "reasons": held, "warnings": warns, "passed": passed, "notes": notes,
           "recipient": {"name": name, "email": email, "phone": phone, "channel": channel, "kind": kind, "mode": a.mode},
           "offered_times": [{"text": s["text"], "when": s["when"].isoformat() if s["when"] else s["date"]} for s in slots],
           "checked_at": now.isoformat()}
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        if held:
            print("HELD: " + held[0])
            for h in held[1:]:
                print("  also: " + h)
        else:
            print("READY" + (f" ({len(warns)} warning{'s' if len(warns) != 1 else ''})" if warns else ""))
        for w in warns:
            print("  WARN: " + w)
        for p in passed:
            print("  passed: " + p)
        for n in notes:
            print("  note: " + n)
    return 1 if held else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:
        print(f"pre_draft_check error: {e}", file=sys.stderr)
        sys.exit(2)
