#!/usr/bin/env python3
"""value_tally.py: month-to-date value total for the Friday value update, plus sign-ups not yet in the log.

Reads the value log /workspace/value-tracker/YYYY-MM.md, one win per line:
    date | type | person | dollars | evidence
    2026-10-23 | autopay-recovered | Lexie Scheetz | 329 | Gmail 1a16... Mindbody receipt 10/23
(Markdown table rows with outer pipes are fine; '#' headings, blank lines, header and |---| rows are ignored.)
Dollars come only from the log's dollars cell. A line with no readable dollar amount is listed under
bad_lines and is NOT counted: the script never invents or estimates dollars.

Optional --sheet: an export of the Prospect Tracking 2026 tab (CSV, a Sheets values JSON {"values": [[...]]},
read_range output with "content", or a JSON list of row dicts). Rows with Sign-Up = Yes and a Sign-Up Date in
the month (on/after --since if given) whose person is not in the log are listed as signup_candidates for the
bot to check evidence and attribution. Reading stops at the AVERAGES row. Sheet amounts in Comments are shown
as comments_mention only and never added to the total.

Usage:
  python3 value_tally.py                                   # current month, default log path
  python3 value_tally.py --month 2026-10 --sheet prospect-2026.csv [--since 2026-10-23] [--json]
  options: --log PATH  --plan 200  --targets 400,600
Exit code: 0 nothing to check (no candidates, no bad lines), 1 candidates or bad log lines to check,
2 script error (missing log file, unreadable or empty sheet export, no Sign-Up header).
"""
import argparse, csv, datetime as dt, io, json, os, re, sys

LOG_DIR = "/workspace/value-tracker"
TYPES = {"signup", "sign-up", "autopay-recovered", "autopay", "winback", "win-back", "other"}
DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def parse_day(s, year=None):
    s = (s or "").strip()
    for f in DATE_FORMATS:
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})", s)
    if m and year:
        try:
            return dt.date(year, int(m.group(1)), int(m.group(2)))
        except ValueError:
            return None
    return None


def money(s):
    m = re.fullmatch(r"\s*\$?\s*(\d[\d,]*(?:\.\d{1,2})?)\s*(?:/mo|/month)?\s*", s or "")
    return float(m.group(1).replace(",", "")) if m else None


def read_log(path, month):
    if not os.path.exists(path):
        raise FileNotFoundError(f"value log not found: {path}")
    wins, bad = [], []
    y, mo = map(int, month.split("-"))
    for ln, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if cells and cells[0].lower() == "date":
            continue
        if len(cells) < 5:
            bad.append({"line": ln, "text": line, "why": "needs 5 cells: date | type | person | dollars | evidence"})
            continue
        day = parse_day(cells[0], y)
        dollars = money(cells[3])
        why = []
        if not day:
            why.append("unreadable date")
        elif (day.year, day.month) != (y, mo):
            why.append(f"date {day} is not in {month}")
        if dollars is None:
            why.append("no dollar amount (never estimated)")
        if not cells[4]:
            why.append("no evidence")
        if why:
            bad.append({"line": ln, "text": line, "why": "; ".join(why)})
            continue
        wins.append({"line": ln, "date": day.isoformat(), "type": cells[1], "person": cells[2],
                     "dollars": dollars, "evidence": " | ".join(cells[4:]),
                     "type_known": cells[1].lower() in TYPES})
    return wins, bad


def sheet_rows(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if not raw.strip():
        raise ValueError(f"empty sheet export: {path}")
    grid = None
    if raw.lstrip()[:1] in "{[":
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            d = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
        if isinstance(d, dict) and "ranges" in d:
            d = d["ranges"][0]
        if isinstance(d, dict) and isinstance(d.get("content"), str):
            grid = list(csv.reader(io.StringIO(d["content"])))
        elif isinstance(d, dict) and isinstance(d.get("values"), list):
            grid = d["values"]
        elif isinstance(d, list) and d and isinstance(d[0], dict):
            hdr = list(d[0].keys())
            grid = [hdr] + [[str(r.get(h, "")) for h in hdr] for r in d]
        elif isinstance(d, list):
            grid = d
    if grid is None:
        grid = list(csv.reader(io.StringIO(raw)))
    hi = next((i for i, r in enumerate(grid) if "Sign-Up" in [c.strip() for c in r]), None)
    if hi is None:
        raise ValueError("no header row with a 'Sign-Up' column in the sheet export")
    hdr = [c.strip() for c in grid[hi]]
    out, stop = [], None
    for i, r in enumerate(grid[hi + 1:], hi + 2):
        if any(str(c).strip().upper() == "AVERAGES" for c in r):
            stop = i
            break
        row = {h: (str(r[j]).strip() if j < len(r) else "") for j, h in enumerate(hdr) if h}
        row["_row"] = i
        out.append(row)
    if not out:
        raise ValueError("sheet export has a header but no rows")
    return out, stop


def in_log(row, wins):
    first, last = norm(row.get("First Name")), norm(row.get("Last Name"))
    email = (row.get("Email Address") or "").lower()
    for w in wins:
        p, ev = norm(w["person"]), w["evidence"].lower()
        if email and email in ev:
            return True
        if first and last and (first + last in p or last + first in p):
            return True
    return False


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--month", default=dt.date.today().strftime("%Y-%m"))
    ap.add_argument("--log")
    ap.add_argument("--sheet")
    ap.add_argument("--since")
    ap.add_argument("--plan", type=float, default=200.0)
    ap.add_argument("--targets", default="400,600")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not re.fullmatch(r"\d{4}-\d{2}", a.month):
        raise ValueError("--month must be YYYY-MM")
    log = a.log or os.path.join(LOG_DIR, f"{a.month}.md")
    wins, bad = read_log(log, a.month)
    total = round(sum(w["dollars"] for w in wins), 2)
    targets = [float(t) for t in a.targets.split(",") if t.strip()]
    res = {"month": a.month, "log": log, "wins": wins, "win_count": len(wins), "total": total,
           "plan": a.plan, "multiple": round(total / a.plan, 2) if a.plan else None,
           "gaps": {f"{t:g}": round(max(0.0, t - total), 2) for t in targets}, "bad_lines": bad}
    if a.sheet:
        y, mo = map(int, a.month.split("-"))
        since = dt.date.fromisoformat(a.since) if a.since else dt.date(y, mo, 1)
        rows, stop = sheet_rows(a.sheet)
        cands, no_date = [], 0
        for r in rows:
            if (r.get("Sign-Up") or "").strip().lower() not in ("yes", "y"):
                continue
            d = parse_day(r.get("Sign-Up Date"), y)
            if not d:
                no_date += 1
                continue
            if (d.year, d.month) != (y, mo) or d < since or in_log(r, wins):
                continue
            hint = re.findall(r"\$\s?\d[\d,]*(?:\.\d{2})?(?:\s?/\s?mo(?:nth)?)?", r.get("Comments", ""))
            cands.append({"row": r["_row"], "name": f"{r.get('First Name', '')} {r.get('Last Name', '')}".strip(),
                          "email": r.get("Email Address", ""), "sign_up_date": d.isoformat(),
                          "service": r.get("Service Type", ""), "referral": r.get("Referral Source", ""),
                          "stage": r.get("Stage", ""), "comments_mention": hint,
                          "monthly_on_sheet": r.get("Monthly Investment", "")})
        res["sheet"] = {"path": a.sheet, "rows_read": len(rows), "stopped_at_averages_row": stop,
                        "since": since.isoformat(), "signup_yes_without_date": no_date}
        res["signup_candidates"] = cands
    found = bool(bad) or bool(res.get("signup_candidates"))
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"{a.month} value to date: ${total:,.2f} from {len(wins)} wins = {res['multiple']}x the ${a.plan:,.0f} plan")
        print("gap to targets: " + ", ".join(f"${float(k):,.0f}: ${v:,.2f}" for k, v in res["gaps"].items()))
        for w in wins:
            print(f"  WIN {w['date']} {w['type']} {w['person']} ${w['dollars']:,.2f} ({w['evidence']})")
        for b in bad:
            print(f"  BAD line {b['line']}: {b['why']}")
        if a.sheet:
            s = res["sheet"]
            print(f"sheet: {s['rows_read']} rows (stopped at AVERAGES row {s['stopped_at_averages_row']}), "
                  f"sign-ups since {s['since']} not in log: {len(res['signup_candidates'])}, "
                  f"Sign-Up=Yes with no date: {s['signup_yes_without_date']}")
            for c in res["signup_candidates"]:
                print(f"  CHECK row {c['row']} {c['name']} signed {c['sign_up_date']} {c['service']} "
                      f"({c['referral']}){' sheet mentions ' + ', '.join(c['comments_mention']) if c['comments_mention'] else ''}")
        print("nothing to check" if not found else "check the items above before counting them")
    return 1 if found else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"value_tally error: {e}", file=sys.stderr)
        sys.exit(2)
