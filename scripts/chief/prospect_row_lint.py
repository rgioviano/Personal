#!/usr/bin/env python3
"""prospect_row_lint.py: check Prospect Tracking row format and Contact Date order.

Infers conventions from the existing data rows (name capitalization, date format,
phone format, and the allowed Stage / Referral Source / Service Type / Eval? /
Sign-Up vocabularies) and flags data rows that deviate. Also checks that the
data block is sorted by Contact Date, newest at the top (blank dates stay at
the bottom). Value-only read_range exports cannot see fonts, alignment, or row height.
Comments must be one short coach-facing line (80 chars or less, no Gmail ids,
"via Chief", readback, or other audit-trail notes - those belong in the journal).
Use --format with a grid-data JSON export (Sheets includeGridData, with
userEnteredFormat / effectiveFormat and rowMetadata pixelSize) or an .xlsx
export of the tab to flag per-column style and row-height drift.

This script never calls Sheets. Strip the untrusted wrapper the same way a
read_range export is prepared for sheet_readback.py (first '{' to last '}'),
then parse ranges[0].content as CSV. A bare CSV or a values-list JSON works too.

Usage:
  python3 prospect_row_lint.py SHEET_EXPORT.json
  python3 prospect_row_lint.py --insert ROW.json|.csv SHEET_EXPORT.json
  python3 prospect_row_lint.py --format GRID.json|.xlsx
  options: --json

Exit code: 0 clean, 1 problems found, 2 script error.
"""
from __future__ import annotations

import argparse, csv, io, json, re, sys
from datetime import datetime
from pathlib import Path

STAGES = [
    "New inquiry", "Contacted", "Replied", "Parked", "Eval booked",
    "Eval done", "No-show", "Offer", "Signed", "Lost", "Hold",
]
SERVICES = [
    "Semi-Private", "Swim Dryland Training", "Athletic Development", "Remote", "Hybrid",
]
# Values already on the 2026 tab that are outside the official Service Type list.
LEGACY_SERVICES = ["Remote/Online Training", "14-Day Trial"]
EVAL_SIGNUP = ["Yes", "No"]
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
MONTH_INDEX = {m.lower(): i + 1 for i, m in enumerate(MONTHS)}
REFERRALS = [
    "Website", "Meta Ad", "Client Referral", "Previous Client", "Previous Athlete",
    "Google", "Yelp", "Search", "Phone", "Walk-in", "Instagram",
]
# Historical typo and one-off referral values already on the tab.
LEGACY_REFERRALS = ["Previoius Client", "Su '26 Athlete #1"]

DATE_COLS = ("Contact Date", "Sign-Up Date", "Last Contact", "Next Follow-Up")
HEADER_ALIASES = {
    "last name": "Last Name",
    "first name": "First Name",
    "month": "Month",
    "contact date": "Contact Date",
    "stage": "Stage",
    "contact count": "Contact Count",
    "referral source": "Referral Source",
    "eval?": "Eval?",
    "eval": "Eval?",
    "sign-up": "Sign-Up",
    "signup": "Sign-Up",
    "sign-up date": "Sign-Up Date",
    "email address": "Email Address",
    "email": "Email Address",
    "phone number": "Phone Number",
    "phone": "Phone Number",
    "service type": "Service Type",
    "comments": "Comments",
    "last contact": "Last Contact",
    "next follow-up": "Next Follow-Up",
    "next follow up": "Next Follow-Up",
}


def load_text(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def strip_wrapper(text):
    """First '{' to last '}', same unwrap used for read_range exports."""
    i, j = text.find("{"), text.rfind("}")
    if i >= 0 and j > i:
        try:
            return json.loads(text[i:j + 1], strict=False)
        except json.JSONDecodeError:
            return None
    return None


def rows_from_payload(data):
    if isinstance(data, dict) and data.get("ranges"):
        content = data["ranges"][0].get("content") or ""
        return list(csv.reader(io.StringIO(content)))
    if isinstance(data, dict) and "values" in data:
        return [list(r) for r in data["values"]]
    if isinstance(data, list) and data and isinstance(data[0], (list, tuple)):
        return [list(r) for r in data]
    return None


def load_sheet(path):
    text = load_text(path)
    data = strip_wrapper(text)
    rows = rows_from_payload(data) if data is not None else None
    if rows is None:
        rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise ValueError(f"no rows in {path}")
    return rows


def canon_header(name):
    return HEADER_ALIASES.get((name or "").strip().lower(), (name or "").strip())


def as_dicts(rows):
    header = [canon_header(h) for h in rows[0]]
    out = []
    for i, raw in enumerate(rows[1:], start=2):
        raw = list(raw) + [""] * (len(header) - len(raw))
        d = {header[j]: raw[j] if j < len(raw) else "" for j in range(len(header))}
        d["_row"] = i
        out.append(d)
    return header, out


def stop_at_averages(dicts):
    kept = []
    avg = None
    for d in dicts:
        if any(str(v).strip().upper() == "AVERAGES" for k, v in d.items() if k != "_row"):
            avg = d["_row"]
            break
        kept.append(d)
    return kept, avg


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%m/%d/%y", "%m/%d/%Y", "%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%m-%d-%y", "%m-%d-%Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    # Sheets serial (days since 1899-12-30) if a bare number sneaks in
    if re.fullmatch(r"\d{5}(?:\.\d+)?", s):
        try:
            from datetime import timedelta
            return datetime(1899, 12, 30) + timedelta(days=float(s))
        except Exception:
            return None
    return None


def format_mdyy(dt):
    return f"{dt.month}/{dt.day}/{dt.strftime('%y')}"


def date_pattern(s):
    s = (s or "").strip()
    if not s:
        return "blank"
    if re.fullmatch(r"\d{1,2}/\d{1,2}/\d{2}", s):
        return "M/D/YY"
    if re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", s):
        return "M/D/YYYY"
    return "other"


def digits_phone(s):
    return re.sub(r"\D", "", s or "")


def phone_pattern(s):
    s = (s or "").strip()
    if not s:
        return "blank"
    if re.fullmatch(r"\d{10}", s):
        return "##########"
    if re.fullmatch(r"\d{3}-\d{3}-\d{4}", s):
        return "###-###-####"
    if re.fullmatch(r"\(\d{3}\) \d{3}-\d{4}", s):
        return "(###) ###-####"
    if re.fullmatch(r"\d{3}\.\d{3}\.\d{4}", s):
        return "###.###.####"
    return "other"


def title_name(s):
    s = (s or "").strip()
    if not s:
        return s
    # Keep trailing initial period: "F." "O."
    if re.fullmatch(r"[A-Za-z]\.?", s):
        return s[0].upper() + ("." if s.endswith(".") else "")
    if s in ("?", "??"):
        return s
    parts = re.split(r"([\s\-']+)", s)
    out = []
    for p in parts:
        if not p or re.fullmatch(r"[\s\-']+", p):
            out.append(p)
            continue
        # Preserve internal caps already present (McCool, O'Neill, Szewczykowski is already Title)
        if any(ch.isupper() for ch in p[1:]) and not p.isupper():
            out.append(p[0].upper() + p[1:])
            continue
        low = p.lower()
        if low.startswith("mc") and len(low) > 2:
            out.append("Mc" + low[2:].capitalize())
        elif low.startswith("o'") and len(low) > 2:
            out.append("O'" + low[2:].capitalize())
        else:
            out.append(low.capitalize())
    return "".join(out)


def most_common(counter):
    if not counter:
        return None
    return max(counter, key=counter.get)


def infer(dicts):
    from collections import Counter
    dates, phones, months = Counter(), Counter(), Counter()
    stages, referrals, services, evals, signups = set(), set(), set(), set(), set()
    for d in dicts:
        for col in DATE_COLS:
            p = date_pattern(d.get(col, ""))
            if p != "blank":
                dates[p] += 1
        p = phone_pattern(d.get("Phone Number", ""))
        if p != "blank":
            phones[p] += 1
        m = (d.get("Month") or "").strip()
        if m:
            months[m] += 1
        if (d.get("Stage") or "").strip():
            stages.add(d["Stage"].strip())
        if (d.get("Referral Source") or "").strip():
            referrals.add(d["Referral Source"].strip())
        if (d.get("Service Type") or "").strip():
            services.add(d["Service Type"].strip())
        if (d.get("Eval?") or "").strip():
            evals.add(d["Eval?"].strip())
        if (d.get("Sign-Up") or "").strip():
            signups.add(d["Sign-Up"].strip())
    return {
        "date_format": most_common(dates) or "M/D/YY",
        "phone_format": most_common(phones) or "##########",
        "month_style": "full" if all(m in MONTHS for m in months) else "mixed",
        "stages": sorted(stages),
        "referrals": sorted(referrals),
        "services": sorted(services),
        "evals": sorted(evals),
        "signups": sorted(signups),
        "date_counts": dict(dates),
        "phone_counts": dict(phones),
    }


def allowed_vocab(official, inferred, legacy=None):
    return set(official) | set(inferred) | set(legacy or [])


def lint_rows(dicts, conv):
    problems = []
    date_ok = {"M/D/YY", "M/D/YYYY"}  # YYYY appears once historically; insert mode still emits M/D/YY
    phone_ok = {"##########", "###-###-####", "###.###.####", "(###) ###-####"}
    # A few existing international / leading-1 numbers; don't fail the whole tab for them.
    stage_ok = allowed_vocab(STAGES, conv["stages"])
    service_ok = allowed_vocab(SERVICES, conv["services"], LEGACY_SERVICES)
    referral_ok = allowed_vocab(REFERRALS, conv["referrals"], LEGACY_REFERRALS)
    eval_ok = allowed_vocab(EVAL_SIGNUP, conv["evals"])
    signup_ok = allowed_vocab(EVAL_SIGNUP, conv["signups"])

    for d in dicts:
        row = d["_row"]
        who = f"{d.get('Last Name','')} {d.get('First Name','')}".strip() or "(no name)"
        prefix = f"row {row} {who}"

        for col in DATE_COLS:
            raw = (d.get(col) or "").strip()
            if not raw:
                continue
            pat = date_pattern(raw)
            if pat not in date_ok or parse_date(raw) is None:
                problems.append({
                    "kind": "format", "row": row, "column": col,
                    "value": raw, "expected": conv["date_format"],
                    "msg": f"{prefix}: {col} {raw!r} is not {conv['date_format']}",
                })

        month = (d.get("Month") or "").strip()
        if month and month not in MONTHS:
            problems.append({
                "kind": "format", "row": row, "column": "Month",
                "value": month, "expected": "full month name (e.g. November)",
                "msg": f"{prefix}: Month {month!r} is not a full month name",
            })
        cd = parse_date(d.get("Contact Date", ""))
        if month and cd and MONTH_INDEX.get(month.lower()) and MONTH_INDEX[month.lower()] != cd.month:
            problems.append({
                "kind": "format", "row": row, "column": "Month",
                "value": month, "expected": MONTHS[cd.month - 1],
                "msg": f"{prefix}: Month {month!r} does not match Contact Date {d.get('Contact Date')}",
            })

        phone = (d.get("Phone Number") or "").strip()
        if phone:
            pat = phone_pattern(phone)
            digs = digits_phone(phone)
            if pat not in phone_ok and not (digs.isdigit() and 10 <= len(digs) <= 15):
                problems.append({
                    "kind": "format", "row": row, "column": "Phone Number",
                    "value": phone, "expected": conv["phone_format"],
                    "msg": f"{prefix}: Phone Number {phone!r} is not {conv['phone_format']}",
                })

        checks = [
            ("Stage", stage_ok, "allowed Stage value"),
            ("Referral Source", referral_ok, "allowed Referral Source value"),
            ("Service Type", service_ok, "allowed Service Type value"),
            ("Eval?", eval_ok, "Yes, No, or blank"),
            ("Sign-Up", signup_ok, "Yes, No, or blank"),
        ]
        for col, ok, expected in checks:
            raw = (d.get(col) or "").strip()
            if raw and raw not in ok:
                problems.append({
                    "kind": "format", "row": row, "column": col,
                    "value": raw, "expected": expected,
                    "msg": f"{prefix}: {col} {raw!r} is not an {expected}",
                })

        for issue in comment_issues(d.get("Comments", "")):
            problems.append({
                "kind": "format", "row": row, "column": "Comments",
                "value": d.get("Comments", ""),
                "expected": f"one short line, {COMMENT_MAX_CHARS} chars or less, no audit trail",
                "msg": f"{prefix}: Comments {issue}",
            })

    # Sort: dated rows newest first; blank Contact Date rows belong at the bottom
    dated = [(parse_date(d.get("Contact Date", "")), d) for d in dicts]
    last_dated_idx = None
    for i, (dt, d) in enumerate(dated):
        if dt is None:
            continue
        if last_dated_idx is not None:
            prev_dt, prev = dated[last_dated_idx]
            if dt > prev_dt:
                who_prev = f"{prev.get('Last Name','')} {prev.get('First Name','')}".strip()
                who_new = f"{d.get('Last Name','')} {d.get('First Name','')}".strip()
                problems.append({
                    "kind": "sort", "row": prev["_row"],
                    "value": prev.get("Contact Date", ""),
                    "expected": f"below row {d['_row']} ({d.get('Contact Date')})",
                    "msg": (
                        f"row {prev['_row']} {who_prev} Contact Date {prev.get('Contact Date')} is out of order: "
                        f"it sits above newer row {d['_row']} {who_new} {d.get('Contact Date')}"
                    ),
                })
        last_dated_idx = i

    # A dated row after a blank-date row (blank should stay at the bottom)
    seen_blank = None
    for dt, d in dated:
        if dt is None and (d.get("Last Name") or d.get("First Name") or d.get("Email Address") or d.get("Phone Number")):
            seen_blank = d
        elif dt is not None and seen_blank is not None:
            problems.append({
                "kind": "sort", "row": d["_row"],
                "value": d.get("Contact Date", ""),
                "expected": "above blank Contact Date rows",
                "msg": (
                    f"row {d['_row']} {d.get('Last Name','')} {d.get('First Name','')}".strip()
                    + f" Contact Date {d.get('Contact Date')} sits below blank-date "
                    + f"row {seen_blank['_row']}"
                ),
            })
    return problems


def insert_row_number(dicts, contact_dt):
    """First data row whose Contact Date is strictly older than contact_dt,
    or blank; otherwise just above the AVERAGES / trailing blank-date block.
    Data rows start at sheet row 2."""
    if contact_dt is None:
        return None
    for d in dicts:
        dt = parse_date(d.get("Contact Date", ""))
        if dt is None or dt < contact_dt:
            return d["_row"]
    if dicts:
        return dicts[-1]["_row"] + 1
    return 2


def normalize_phone(s):
    s = (s or "").strip()
    if not s:
        return ""
    digs = digits_phone(s)
    if len(digs) == 11 and digs.startswith("1"):
        digs = digs[1:]
    if len(digs) == 10:
        return digs
    return s



# Verbose Comments markers that belong in the journal, not column N.
COMMENT_MAX_CHARS = 80
COMMENT_BANNED = (
    (r"(?i)via\s+Chief", "via Chief"),
    (r"(?i)per\s+Ryne\s+via", "per Ryne via"),
    (r"(?i)Chief\s+1:1", "Chief 1:1"),
    (r"(?i)read-?back|sheet_readback", "readback"),
    (r"(?i)calendar check", "calendar check"),
    (r"(?i)log-send", "log-send"),
    (r"(?i)Gmail\s+[0-9a-f]{8,}", "Gmail id"),
    (r"(?i)\b[0-9a-f]{16}\b", "Gmail id"),
    (r"(?i)touch\s+\d", "touch N"),
    (r"(?i)Contact Count", "Contact Count"),
    (r"(?i)NFU blank", "NFU blank"),
    (r"(?i)Achieve Minute newsletter", "process note"),
    (r"(?i)RULES\s+\d+", "RULES citation"),
    (r"(?i)\d{1,2}:\d{2}\s*(am|pm)", "timestamp to the minute"),
)


def comment_issues(text):
    """Return problem strings for a Comments cell that is too long or bot-verbose."""
    s = text or ""
    if not str(s).strip():
        return []
    s = str(s)
    issues = []
    if len(s) > COMMENT_MAX_CHARS:
        issues.append(f"{len(s)} chars (max {COMMENT_MAX_CHARS})")
    seen = set()
    for pat, label in COMMENT_BANNED:
        if re.search(pat, s) and label not in seen:
            issues.append(label)
            seen.add(label)
    return issues


def normalize_row(row):
    """Return (normalized dict, list of change/problem messages, fatal?)."""
    notes, fatal = [], False
    out = dict(row)
    for key in ("Last Name", "First Name", "Month", "Contact Date", "Stage",
                "Contact Count", "Referral Source", "Eval?", "Sign-Up",
                "Sign-Up Date", "Email Address", "Phone Number", "Service Type",
                "Comments", "Last Contact", "Next Follow-Up"):
        out.setdefault(key, "")
        if isinstance(out[key], (int, float)) and key != "Contact Count":
            out[key] = str(out[key])
        if out[key] is None:
            out[key] = ""
        elif not isinstance(out[key], str):
            out[key] = str(out[key])
        else:
            # keep comments as-is except strip the cell, not inner spaces
            if key != "Comments":
                stripped = out[key].strip()
                if stripped != out[key]:
                    notes.append(f"{key}: trimmed whitespace")
                out[key] = stripped

    for col in ("Last Name", "First Name"):
        new = title_name(out[col])
        if new != out[col]:
            notes.append(f"{col}: {out[col]!r} -> {new!r}")
            out[col] = new

    for col in DATE_COLS:
        raw = out[col]
        if not raw:
            continue
        dt = parse_date(raw)
        if dt is None:
            notes.append(f"{col}: {raw!r} is not a date")
            fatal = True
            continue
        new = format_mdyy(dt)
        if new != raw:
            notes.append(f"{col}: {raw!r} -> {new!r}")
            out[col] = new

    cd = parse_date(out["Contact Date"])
    if cd is None:
        notes.append("Contact Date is required to place the row")
        fatal = True
    else:
        want_month = MONTHS[cd.month - 1]
        if out["Month"] != want_month:
            if out["Month"]:
                notes.append(f"Month: {out['Month']!r} -> {want_month!r}")
            else:
                notes.append(f"Month: (blank) -> {want_month!r}")
            out["Month"] = want_month

    new_phone = normalize_phone(out["Phone Number"])
    if new_phone != out["Phone Number"]:
        notes.append(f"Phone Number: {out['Phone Number']!r} -> {new_phone!r}")
        out["Phone Number"] = new_phone

    def canon_from(val, official, label):
        if not val:
            return val
        for item in official:
            if val.lower() == item.lower():
                if val != item:
                    notes.append(f"{label}: {val!r} -> {item!r}")
                return item
        return val

    out["Stage"] = canon_from(out["Stage"], STAGES, "Stage")
    out["Service Type"] = canon_from(out["Service Type"], SERVICES + LEGACY_SERVICES, "Service Type")
    out["Referral Source"] = canon_from(out["Referral Source"], REFERRALS, "Referral Source")
    out["Eval?"] = canon_from(out["Eval?"], EVAL_SIGNUP, "Eval?")
    out["Sign-Up"] = canon_from(out["Sign-Up"], EVAL_SIGNUP, "Sign-Up")

    if out["Stage"] and out["Stage"] not in STAGES:
        notes.append(f"Stage: {out['Stage']!r} is not an allowed Stage value")
        fatal = True
    if out["Service Type"] and out["Service Type"] not in SERVICES + LEGACY_SERVICES:
        notes.append(f"Service Type: {out['Service Type']!r} is not an allowed Service Type value")
        fatal = True
    if out["Referral Source"] and out["Referral Source"] not in REFERRALS + LEGACY_REFERRALS:
        notes.append(f"Referral Source: {out['Referral Source']!r} is not an allowed Referral Source value")
        fatal = True
    if out["Eval?"] and out["Eval?"] not in EVAL_SIGNUP:
        notes.append(f"Eval?: {out['Eval?']!r} must be Yes, No, or blank")
        fatal = True
    if out["Sign-Up"] and out["Sign-Up"] not in EVAL_SIGNUP:
        notes.append(f"Sign-Up: {out['Sign-Up']!r} must be Yes, No, or blank")
        fatal = True

    for issue in comment_issues(out.get("Comments", "")):
        notes.append(f"Comments: {issue}")
        fatal = True

    return out, notes, fatal


def load_proposed_row(path):
    text = load_text(path)
    data = strip_wrapper(text)
    if data is None and not path.lower().endswith(".csv"):
        # maybe a single JSON object without going through strip (already unwrapped failure)
        try:
            data = json.loads(text, strict=False)
        except json.JSONDecodeError:
            data = None
    if isinstance(data, list) and data and isinstance(data[0], dict):
        data = data[0]
    if isinstance(data, dict) and "ranges" not in data and "values" not in data:
        # already a row object; canonicalize keys
        return {canon_header(k): v for k, v in data.items() if k != "_row"}
    if data is not None:
        rows = rows_from_payload(data)
        if rows and len(rows) >= 2:
            _, dicts = as_dicts(rows)
            d = {k: v for k, v in dicts[0].items() if k != "_row"}
            return d
        if rows and len(rows) == 1:
            # headerless? treat as values under default headers if JSON list of values
            pass
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise ValueError(f"no row in {path}")
    if len(rows) == 1 and not any(canon_header(h) in ("Last Name", "First Name", "Contact Date") for h in rows[0]):
        raise ValueError(f"{path} needs a header row or a JSON object")
    _, dicts = as_dicts(rows)
    return {k: v for k, v in dicts[0].items() if k != "_row"}


def print_conventions(conv):
    print("conventions from existing rows:")
    print(f"  date format: {conv['date_format']}  (seen {conv['date_counts']})")
    print(f"  phone format: {conv['phone_format']}  (seen {conv['phone_counts']})")
    print(f"  month: full English name")
    print(f"  Stage: {', '.join(STAGES)}")
    print(f"  Service Type: {', '.join(SERVICES)}")
    print(f"  Eval? / Sign-Up: Yes, No, or blank")



# --- format lint (grid data / xlsx) -----------------------------------------

PT_TO_PX = 96.0 / 72.0  # 15.0 pt -> 20 px, 15.75 pt -> 21 px, 22.5 pt -> 30 px
# Body date/number columns display right under general alignment.
RIGHT_GENERAL_COLS = {"Contact Date", "Sign-Up Date", "Phone Number"}
# Service Type "@" (plain text) and "General" look the same.
TEXT_NUM_FMTS = {"General", "@", "GENERAL"}
DATE_NUM_FMTS = {"m/d/yy", "M/d/yy", 'm"/"d"/"yy', 'M"/"d"/"yy', "m/d/yyyy", "M/d/yyyy"}


def _rgb_hex(color):
    if not color:
        return None
    if isinstance(color, str):
        s = color.strip().lstrip("#")
        if len(s) == 8:
            s = s[2:]
        return s.upper() if len(s) == 6 else s
    if isinstance(color, dict):
        rgb = color.get("rgbColor") or color
        if "red" in rgb or "green" in rgb or "blue" in rgb:
            def ch(k):
                v = rgb.get(k, 0) or 0
                if isinstance(v, float) and v <= 1:
                    v = int(round(v * 255))
                return int(v)
            return f"{ch('red'):02X}{ch('green'):02X}{ch('blue'):02X}"
    return None


def _fmt_from_sheets_format(fmt):
    if not fmt or not isinstance(fmt, dict):
        return None
    tf = fmt.get("textFormat") or {}
    fg = tf.get("foregroundColorStyle") or {}
    color = _rgb_hex(fg.get("rgbColor") if isinstance(fg, dict) else None) or _rgb_hex(tf.get("foregroundColor"))
    nf = fmt.get("numberFormat") or {}
    pattern = (nf.get("pattern") if isinstance(nf, dict) else None) or "General"
    wrap = fmt.get("wrapStrategy") or "OVERFLOW_CELL"
    valign = fmt.get("verticalAlignment") or None
    if valign == "MIDDLE":
        valign = "center"
    elif valign:
        valign = valign.lower()
    halign = fmt.get("horizontalAlignment") or None
    if halign:
        halign = halign.lower()
    size = tf.get("fontSize")
    return {
        "fmt": pattern or "General",
        "font": tf.get("fontFamily"),
        "size": size,
        "bold": bool(tf.get("bold")),
        "color": color,
        "h": halign,
        "v": valign,
        "wrap": wrap in ("WRAP", "wrap", True),
    }


def _fmt_from_openpyxl(cell):
    f, a = cell.font, cell.alignment
    color = None
    try:
        if f.color is not None and f.color.type == "rgb" and f.color.rgb:
            color = _rgb_hex(str(f.color.rgb))
    except Exception:
        color = None
    return {
        "fmt": cell.number_format or "General",
        "font": f.name,
        "size": f.size,
        "bold": bool(f.bold),
        "color": color,
        "h": (a.horizontal or None),
        "v": (a.vertical or None),
        "wrap": bool(a.wrap_text),
    }



def _cell_string_from_grid(data, row0, col0):
    """Best-effort string value of a grid cell (0-based)."""
    sheets = data.get("sheets") if isinstance(data, dict) else None
    if not sheets and isinstance(data, dict) and data.get("data"):
        sheets = [data]
    if not sheets:
        return None
    sheet = None
    for s in sheets:
        title = ((s.get("properties") or {}).get("title") or "")
        if title == "2026":
            sheet = s
            break
    if sheet is None:
        sheet = sheets[0]
    for block in sheet.get("data") or []:
        r0 = int(block.get("startRow") or 0)
        c0 = int(block.get("startColumn") or 0)
        rd = block.get("rowData") or []
        i = row0 - r0
        if i < 0 or i >= len(rd):
            continue
        vals = rd[i].get("values") or []
        j = col0 - c0
        if j < 0 or j >= len(vals):
            continue
        v = vals[j]
        ev = (v.get("effectiveValue") or v.get("userEnteredValue") or {})
        return ev.get("stringValue") or v.get("formattedValue") or ev.get("formattedValue")
    return None


def _row_is_averages(d, header, data, row0):
    # Check Last Name or first column text
    for name in header:
        if name.lower() in ("last name", "last", "c1") or name == header[0]:
            s = _cell_string_from_grid(data, row0, header.index(name) if name in header else 0)
            if s and str(s).strip().upper() == "AVERAGES":
                return True
            break
    # Also check any formattedValue on the row
    s = _cell_string_from_grid(data, row0, 0)
    return bool(s and str(s).strip().upper() == "AVERAGES")


def load_grid(path):
    """Load includeGridData JSON or an .xlsx of the 2026 (or first) tab.

    Returns (header, rows) where each row is
    {"_row": n, "_height_px": int, "<col>": style-dict}.
    """
    path = str(path)
    if path.lower().endswith(".xlsx") or path.lower().endswith(".xlsm"):
        return _load_grid_xlsx(path)
    text = load_text(path)
    data = strip_wrapper(text)
    if data is None:
        try:
            data = json.loads(text, strict=False)
        except json.JSONDecodeError as e:
            raise ValueError(f"not grid JSON or xlsx: {e}") from e
    return _load_grid_json(data)


def _load_grid_json(data):
    # Accept {sheets:[{data:[{rowData,rowMetadata}]}]} or a single sheet object
    sheets = data.get("sheets") if isinstance(data, dict) else None
    if not sheets and isinstance(data, dict) and data.get("data"):
        sheets = [data]
    if not sheets:
        raise ValueError("grid JSON needs sheets[].data[] (includeGridData) or an xlsx export")
    sheet = None
    for s in sheets:
        title = ((s.get("properties") or {}).get("title") or "")
        if title == "2026":
            sheet = s
            break
    if sheet is None:
        sheet = sheets[0]
    blocks = sheet.get("data") or []
    if not blocks:
        raise ValueError("grid JSON has no data blocks")
    # Merge blocks by startRow/startColumn
    cells = {}  # (r,c) 0-based -> format
    heights = {}  # r 0-based -> px
    max_r, max_c = -1, -1
    for block in blocks:
        r0 = int(block.get("startRow") or 0)
        c0 = int(block.get("startColumn") or 0)
        meta = block.get("rowMetadata") or []
        for i, m in enumerate(meta):
            px = (m or {}).get("pixelSize")
            if px is not None:
                heights[r0 + i] = int(px)
        for i, rd in enumerate(block.get("rowData") or []):
            for j, cv in enumerate(rd.get("values") or []):
                fmt = _fmt_from_sheets_format(cv.get("userEnteredFormat") or cv.get("effectiveFormat") or {})
                # Prefer userEnteredFormat, fall back to effective
                if cv.get("userEnteredFormat") and cv.get("effectiveFormat"):
                    ue = _fmt_from_sheets_format(cv["userEnteredFormat"])
                    ef = _fmt_from_sheets_format(cv["effectiveFormat"])
                    # fill holes in user-entered from effective
                    for k, v in (ef or {}).items():
                        if ue and (ue.get(k) is None or ue.get(k) == ""):
                            ue[k] = v
                    fmt = ue
                cells[(r0 + i, c0 + j)] = fmt
                max_r, max_c = max(max_r, r0 + i), max(max_c, c0 + j)
    if max_r < 0:
        raise ValueError("grid JSON has no cells")
    # Header names from first row values if present, else A-P defaults
    header = []
    first_vals = (blocks[0].get("rowData") or [{}])[0].get("values") or []
    for j in range(0, max(max_c + 1, 16)):
        name = None
        if j < len(first_vals):
            v = first_vals[j]
            ev = (v.get("effectiveValue") or v.get("userEnteredValue") or {})
            name = ev.get("stringValue") or ev.get("formattedValue") or v.get("formattedValue")
        header.append(canon_header(name or f"C{j+1}"))
    rows = []
    for r in range(1, max_r + 1):  # skip header row 0
        # Stop at the AVERAGES / summary block (not a prospect row)
        first_name_cell = None
        # Prefer Last Name / col A string from the original JSON if present later
        d = {"_row": r + 1, "_height_px": heights.get(r)}
        for c, name in enumerate(header):
            d[name] = cells.get((r, c))
        if _row_is_averages(d, header, data, r):
            break
        rows.append(d)
    return header, rows


def _load_grid_xlsx(path):
    import openpyxl
    from openpyxl.utils import get_column_letter
    import zipfile, re
    wb = openpyxl.load_workbook(path, data_only=False)
    ws = wb["2026"] if "2026" in wb.sheetnames else wb[wb.sheetnames[0]]
    # row heights from the raw worksheet XML (openpyxl can miss defaults)
    heights_pt = {}
    default_pt = 15.75
    sheet_path = None
    # map title -> xml via workbook rels is handled below: iterate worksheets
    with zipfile.ZipFile(path) as z:
        wb_xml = z.read("xl/workbook.xml").decode("utf-8", "replace")
        rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8", "replace")
        rid = None
        for m in re.finditer(r'<sheet\b[^>]*>', wb_xml):
            tag = m.group(0)
            name = re.search(r'name="([^"]+)"', tag)
            id_ = re.search(r'r:id="([^"]+)"', tag)
            if name and id_ and name.group(1) == ws.title:
                rid = id_.group(1)
                break
        target = None
        if rid:
            m = re.search(rf'Id="{re.escape(rid)}"[^>]*Target="([^"]+)"', rels) or re.search(
                rf'Target="([^"]+)"[^>]*Id="{re.escape(rid)}"', rels)
            if m:
                target = m.group(1)
                if not target.startswith("xl/"):
                    target = "xl/" + target.lstrip("/")
        if not target:
            target = "xl/worksheets/sheet1.xml"
        xml = z.read(target).decode("utf-8", "replace")
    m = re.search(r'defaultRowHeight="([^"]+)"', xml)
    if m:
        default_pt = float(m.group(1))
    for tag in re.findall(r'<row [^>]*>', xml):
        r = re.search(r'\br="(\d+)"', tag)
        ht = re.search(r'\bht="([^"]+)"', tag)
        if r:
            heights_pt[int(r.group(1))] = float(ht.group(1)) if ht else default_pt

    header = [canon_header(ws.cell(1, c).value or f"C{c}") for c in range(1, 17)]
    # last data row: AVERAGES
    last = ws.max_row
    for r in range(2, (ws.max_row or 2) + 1):
        if any(str(ws.cell(r, c).value or "").strip().upper() == "AVERAGES" for c in range(1, 17)):
            last = r - 1
            break
    rows = []
    for r in range(2, last + 1):
        pt = heights_pt.get(r, default_pt)
        d = {"_row": r, "_height_px": int(round(pt * PT_TO_PX)), "_height_pt": pt}
        for c, name in enumerate(header, start=1):
            d[name] = _fmt_from_openpyxl(ws.cell(r, c))
        rows.append(d)
    return header, rows


def _h_equiv(col, got, want):
    """General (None) displays left for text and right for dates/numbers."""
    def norm(v):
        return None if v in (None, "", "general") else str(v).lower()
    g, w = norm(got), norm(want)
    if g == w:
        return True
    if col in RIGHT_GENERAL_COLS:
        return {g, w} <= {None, "right"}
    if col in ("Referral Source", "Eval?"):
        return g == w  # center is explicit; general is not center
    return {g, w} <= {None, "left"}


def _fmt_equiv(col, got, want):
    g = (got or "General").replace('"', "")
    w = (want or "General").replace('"', "")
    if g == w:
        return True
    gl, wl = g.lower(), w.lower()
    if gl == wl:
        return True
    if col in ("Service Type",) or (g in TEXT_NUM_FMTS and w in TEXT_NUM_FMTS):
        return True
    # date columns: M/d/yy vs m/d/yy; General on a date col is a missing format, not a mismatch if both general-or-date
    def dateish(p):
        p = p.lower().replace('"', "")
        return p in {x.lower().replace('"', "") for x in DATE_NUM_FMTS}
    if col in DATE_COLS and (dateish(g) or g in TEXT_NUM_FMTS) and (dateish(w) or w in TEXT_NUM_FMTS):
        # Flag only wild patterns (e.g. yyyy-mm-dd) against M/d/yy; General vs M/d/yy is historical and looks the same when blank
        if dateish(g) and dateish(w):
            return True
        if g in TEXT_NUM_FMTS or w in TEXT_NUM_FMTS:
            return True
    return False


def _size_equiv(got, want):
    if got == want:
        return True
    # Default size (None) vs explicit 10 is not equivalent for Last/First Name (those are 10).
    return False


def _color_equiv(got, want):
    def n(v):
        if not v:
            return None
        s = str(v).upper().lstrip("#")
        if len(s) == 8:
            s = s[2:]
        return s
    return n(got) == n(want)


def infer_format_conventions(rows, header):
    from collections import Counter
    heights = Counter(r.get("_height_px") for r in rows if r.get("_height_px") is not None)
    height = max(heights, key=heights.get) if heights else 20
    cols = {}
    style_keys = ("fmt", "font", "size", "bold", "color", "h", "v", "wrap")
    for col in header:
        if col.startswith("_"):
            continue
        if True:
            c = Counter()
            for r in rows:
                st = r.get(col)
                if not isinstance(st, dict):
                    continue
                key = tuple(st.get(k) for k in style_keys)
                c[key] += 1
            if c:
                top = max(c, key=c.get)
                cols[col] = dict(zip(style_keys, top))
    return {"height_px": height, "height_counts": dict(heights), "columns": cols}


def lint_formats(rows, header, conv):
    problems = []
    want_h = conv["height_px"]
    for r in rows:
        row = r["_row"]
        prefix = f"row {row}"
        got_h = r.get("_height_px")
        if got_h is not None and got_h != want_h:
            problems.append({
                "kind": "format", "row": row, "column": "_height",
                "value": got_h, "expected": want_h,
                "msg": f"{prefix}: row height {got_h}px != body height {want_h}px",
            })
        for col, want in conv["columns"].items():
            st = r.get(col)
            if not isinstance(st, dict):
                continue
            diffs = []
            if st.get("font") != want.get("font"):
                diffs.append(f"font {st.get('font')!r} != {want.get('font')!r}")
            if not _size_equiv(st.get("size"), want.get("size")):
                diffs.append(f"size {st.get('size')!r} != {want.get('size')!r}")
            if bool(st.get("bold")) != bool(want.get("bold")):
                diffs.append(f"bold {st.get('bold')} != {want.get('bold')}")
            if not _color_equiv(st.get("color"), want.get("color")):
                diffs.append(f"color {st.get('color')!r} != {want.get('color')!r}")
            if not _h_equiv(col, st.get("h"), want.get("h")):
                diffs.append(f"horizontal {st.get('h')!r} != {want.get('h')!r}")
            if (st.get("v") or "center") != (want.get("v") or "center"):
                diffs.append(f"vertical {st.get('v')!r} != {want.get('v')!r}")
            if bool(st.get("wrap")) != bool(want.get("wrap")):
                diffs.append(f"wrap {st.get('wrap')} != {want.get('wrap')}")
            if not _fmt_equiv(col, st.get("fmt"), want.get("fmt")):
                diffs.append(f"number format {st.get('fmt')!r} != {want.get('fmt')!r}")
            if diffs:
                problems.append({
                    "kind": "format", "row": row, "column": col,
                    "value": st, "expected": want,
                    "msg": f"{prefix} {col}: " + "; ".join(diffs),
                })
    return problems

def main(argv=None):
    ap = argparse.ArgumentParser(description="Lint Prospect Tracking format and Contact Date order.")
    ap.add_argument("sheet", nargs="?", help="read_range JSON/CSV (values lint), or grid JSON/xlsx with --format")
    ap.add_argument("--insert", metavar="ROW", help="proposed new row (JSON object or CSV) to normalize and place")
    ap.add_argument("--format", action="store_true",
                    help="lint per-column cell style and row height from a grid-data JSON (includeGridData) or .xlsx")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    a = ap.parse_args(argv)
    if not a.sheet:
        ap.error("SHEET_EXPORT is required")
    if a.format:
        try:
            header, frows = load_grid(a.sheet)
            # stop at AVERAGES if those rows slipped in (xlsx loader already stops)
            kept = []
            for r in frows:
                kept.append(r)
            conv = infer_format_conventions(kept, header)
            problems = lint_formats(kept, header, conv)
        except Exception as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        if a.json:
            print(json.dumps({
                "mode": "format",
                "height_px": conv["height_px"],
                "height_counts": conv["height_counts"],
                "data_rows": len(kept),
                "problem_count": len(problems),
                "problems": [{"row": p["row"], "column": p["column"], "msg": p["msg"]} for p in problems],
            }, indent=2, default=str))
        else:
            print(f"format conventions: body row height {conv['height_px']}px (seen {conv['height_counts']})")
            print(f"data rows: {len(kept)}")
            if not problems:
                print("0 problems")
            else:
                for p in problems:
                    print(p["msg"])
                print(f"{len(problems)} problem" + ("" if len(problems) == 1 else "s"))
        return 1 if problems else 0
    try:
        rows = load_sheet(a.sheet)
        header, dicts_all = as_dicts(rows)
        dicts, avg = stop_at_averages(dicts_all)
        conv = infer(dicts)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if a.insert:
        try:
            proposed = load_proposed_row(a.insert)
            normalized, notes, fatal = normalize_row(proposed)
            place = insert_row_number(dicts, parse_date(normalized.get("Contact Date", "")))
        except Exception as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        payload = {
            "normalized": {k: v for k, v in normalized.items() if k != "_row"},
            "insert_row": place,
            "notes": notes,
            "ok": not fatal,
        }
        if a.json:
            print(json.dumps(payload, indent=2))
        else:
            print_conventions(conv)
            print("normalized row:")
            print(json.dumps(payload["normalized"], indent=2))
            if place is None:
                print("insert_row: unknown (Contact Date missing or unparseable)")
            else:
                print(f"insert_row: {place}")
            if notes:
                print("notes:")
                for n in notes:
                    print(f"  {n}")
            print("ok" if not fatal else "NOT CLEAN")
        return 1 if fatal else 0

    problems = lint_rows(dicts, conv)
    if a.json:
        print(json.dumps({
            "conventions": {k: conv[k] for k in ("date_format", "phone_format", "month_style")},
            "averages_row": avg,
            "data_rows": len(dicts),
            "problem_count": len(problems),
            "problems": problems,
        }, indent=2))
    else:
        print_conventions(conv)
        if avg:
            print(f"data rows: {len(dicts)} (AVERAGES at row {avg})")
        else:
            print(f"data rows: {len(dicts)}")
        if not problems:
            print("0 problems")
        else:
            for p in problems:
                print(p["msg"])
            print(f"{len(problems)} problem" + ("" if len(problems) == 1 else "s"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
