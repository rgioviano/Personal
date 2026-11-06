#!/usr/bin/env python3
"""hawkin_untested.py: Hawkin untested watch. Which athletes are due for a CMJ or SJ retest.

The bot pulls Hawkin with its own connector or script and exports two files. This script
never calls Hawkin and never reads a key. It only applies the rule:

  High school (age 14 to 18): last active CMJ/SJ test 21 to 42 days ago (3 to 6 weeks)
  Ages 11 to 13:              last active CMJ/SJ test 56 to 84 days ago (8 to 12 weeks)
  Age = this year minus birth year (Hawkin stores birth year only for most athletes).
  Skipped: inactive athletes, inactive trials, test types other than CMJ/SJ,
           athletes on the away list whose last test is on or before the day they were marked away.
  Listed separately: active athletes tested in the window of the export with no birth year.

Inputs (CSV or JSON list of objects; column names are case-insensitive):
  --tests   one row per test or session: athlete_id (or athlete), date (YYYY-MM-DD, CT), test, active
  --roster  one row per athlete: athlete_id, name, birth_year (or dob), active
  --away    optional: name, marked_on (YYYY-MM-DD)
  or --hawkin-json  the raw cache the weekly-trends pull writes ({now, athletes, tests}).

Usage:
  python3 hawkin_untested.py --tests tests.csv --roster roster.csv [--away away.csv] [--today 2026-10-19]
  python3 hawkin_untested.py --hawkin-json /workspace/hawkin/2026-10-19/cache.json --away away.csv
  options: --json, --markdown (print the Slack-ready post), --hs-window 21-42, --young-window 56-84
Exit code: 0 nobody due, 1 athletes due (or no-birth-year athletes to fix), 2 script error.
"""
import argparse, csv, datetime as dt, json, re, sys
from zoneinfo import ZoneInfo

CHI = ZoneInfo("America/Chicago")
CANON = {"7nNduHeM5zETPjHxvm7s": "CMJ", "QEG7m7DhYsD6BrcQ8pic": "SJ"}


def load_rows(path):
    if path.lower().endswith(".json"):
        data = json.load(open(path, encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("data") or data.get("rows") or []
        return [{str(k).strip().lower(): v for k, v in r.items()} for r in data]
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def pick(r, *names):
    for n in names:
        if n in r and str(r[n]).strip() != "":
            return str(r[n]).strip()
    return ""


def truthy(v, default=True):
    if v is None or str(v).strip() == "":
        return default
    return str(v).strip().lower() not in {"false", "0", "no", "n", "inactive"}


def parse_day(v):
    v = str(v).strip()
    if re.fullmatch(r"\d{9,11}(\.\d+)?", v):
        return dt.datetime.fromtimestamp(float(v), CHI).date()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", v)
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", v)
    if m:
        y = int(m[3]); y = y + 2000 if y < 100 else y
        return dt.date(y, int(m[1]), int(m[2]))
    raise ValueError(f"unreadable date {v!r}")


def window(s):
    a, b = s.split("-")
    return int(a), int(b)


def from_hawkin_json(path):
    d = json.load(open(path, encoding="utf-8"))
    today = dt.datetime.fromtimestamp(d["now"], CHI).date() if d.get("now") else None
    roster = []
    for a in (d.get("athletes") or {}).get("data", []):
        dob = str(a.get("dob") or "")[:4]
        roster.append({"athlete_id": a["id"], "name": a.get("name", ""), "birth_year": dob if dob.isdigit() else "",
                       "active": "false" if a.get("active") is False else "true"})
    tests = []
    for t in d.get("tests", []):
        k = CANON.get((t.get("testType") or {}).get("canonicalId"))
        if not k:
            continue
        tests.append({"athlete_id": t["athlete"]["id"], "athlete": t["athlete"].get("name", ""),
                      "date": dt.datetime.fromtimestamp(t["timestamp"], CHI).date().isoformat(), "test": k,
                      "active": "false" if t.get("active") is False else "true"})
    return roster, tests, today


def run(roster, tests, away, today, hs_win, young_win):
    by_id, by_name = {}, {}
    for r in roster:
        aid = pick(r, "athlete_id", "id")
        name = pick(r, "name", "athlete", "athlete name")
        by = pick(r, "birth_year", "dob", "birthyear", "birth year")[:4]
        rec = {"id": aid, "name": name, "birth_year": int(by) if by.isdigit() else None,
               "active": truthy(r.get("active"))}
        if aid:
            by_id[aid] = rec
        by_name.setdefault(name.casefold(), rec)
    last, skipped_types = {}, 0
    for t in tests:
        typ = pick(t, "test", "test_type", "type").upper()
        if typ and not any(x in typ for x in ("CMJ", "SJ", "COUNTERMOVEMENT", "SQUAT JUMP")):
            skipped_types += 1
            continue
        if not truthy(t.get("active")):
            continue
        aid = pick(t, "athlete_id", "id")
        rec = by_id.get(aid) if aid else None
        if rec is None:
            nm = pick(t, "athlete", "name", "athlete name")
            rec = by_name.get(nm.casefold())
            if rec is None:
                rec = {"id": aid or nm, "name": nm, "birth_year": None, "active": True}
                by_name[nm.casefold()] = rec
        day = parse_day(pick(t, "date", "timestamp", "tested_on"))
        key = rec["id"] or rec["name"]
        if key not in last or day > last[key][1]:
            last[key] = (rec, day)
    away_map = {pick(a, "name").casefold(): parse_day(pick(a, "marked_on", "date", "since")) for a in away}
    hs, young, no_by, away_skip = [], [], [], []
    for rec, day in last.values():
        if not rec["active"]:
            continue
        days = (today - day).days
        if rec["birth_year"] is None:
            no_by.append({"name": rec["name"], "last_test": day.isoformat(), "days": days})
            continue
        mk = away_map.get(rec["name"].strip().casefold())
        if mk and day <= mk:
            away_skip.append(rec["name"])
            continue
        age = today.year - rec["birth_year"]
        row = {"name": rec["name"], "last_test": day.isoformat(), "days": days, "age": age}
        if 14 <= age <= 18 and hs_win[0] <= days <= hs_win[1]:
            hs.append(row)
        elif 11 <= age <= 13 and young_win[0] <= days <= young_win[1]:
            young.append(row)
    key = lambda r: (-r["days"], r["name"])
    return {"today": today.isoformat(), "hs_window_days": list(hs_win), "young_window_days": list(young_win),
            "high_school_due": sorted(hs, key=key), "ages_11_13_due": sorted(young, key=key),
            "no_birth_year": sorted(no_by, key=key), "away_skipped": sorted(away_skip),
            "athletes_with_tests": len(last),
            "export_span_days": (today - min(d for _, d in last.values())).days if last else 0,
            "away_marked_on": sorted({v.isoformat() for v in away_map.values()})}


def fmt_day(iso):
    d = dt.date.fromisoformat(iso)
    return d.strftime("%b ") + str(d.day)


def markdown(res, hs_win, young_win):
    d = dt.date.fromisoformat(res["today"])
    out = [f"**Hawkin untested watch, {d.strftime('%b')} {d.day}, {d.year}.** Athletes due for a CMJ or SJ, based on their last active test.", ""]
    for title, rows in ((f"High school (14 to 18), last test {hs_win[0]//7} to {hs_win[1]//7} weeks ago", res["high_school_due"]),
                        (f"Ages 11 to 13, last test {young_win[0]//7} to {young_win[1]//7} weeks ago", res["ages_11_13_due"])):
        out += [f"**{title}**", ""]
        if rows:
            out += ["| Athlete | Last test | Days |", "|---|---|---|"]
            out += [f"| {r['name']} | {fmt_day(r['last_test'])} | {r['days']} |" for r in rows]
        else:
            out.append("- Nobody due")
        out.append("")
    if res["no_birth_year"]:
        out.append(f"- {len(res['no_birth_year'])} active athletes tested in the last {res['export_span_days']} days have no birth year in Hawkin, so they can't be sorted into a group.")
    if res["away_skipped"]:
        on = res["away_marked_on"]
        when = f" on {fmt_day(on[0])}" if len(on) == 1 else ""
        out.append(f"- The {len(res['away_skipped'])} athletes you marked as away{when} are left out until they test again.")
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Hawkin untested watch: who is due for a CMJ/SJ retest (exported files in, no API calls).")
    ap.add_argument("--tests"); ap.add_argument("--roster"); ap.add_argument("--away")
    ap.add_argument("--hawkin-json", help="raw weekly-trends cache {now, athletes, tests}")
    ap.add_argument("--today", help="YYYY-MM-DD in CT (default: cache 'now', else today)")
    ap.add_argument("--hs-window", default="21-42"); ap.add_argument("--young-window", default="56-84")
    ap.add_argument("--json", action="store_true"); ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()
    cache_today = None
    if a.hawkin_json:
        roster, tests, cache_today = from_hawkin_json(a.hawkin_json)
    elif a.tests and a.roster:
        roster, tests = load_rows(a.roster), load_rows(a.tests)
    else:
        ap.error("give --tests and --roster, or --hawkin-json")
    if not tests:
        print("FLAG_EMPTY_PULL: the tests export has 0 CMJ/SJ rows. Empty is not zero; check the pull.", file=sys.stderr)
        return 2
    away = load_rows(a.away) if a.away else []
    today = parse_day(a.today) if a.today else (cache_today or dt.datetime.now(CHI).date())
    hs_win, young_win = window(a.hs_window), window(a.young_window)
    res = run(roster, tests, away, today, hs_win, young_win)
    n = len(res["high_school_due"]) + len(res["ages_11_13_due"]) + len(res["no_birth_year"])
    if a.json:
        print(json.dumps(res, indent=2))
    elif a.markdown:
        print(markdown(res, hs_win, young_win), end="")
    else:
        print(f"as of {res['today']} CT: {len(res['high_school_due'])} high school due, {len(res['ages_11_13_due'])} ages 11-13 due, "
              f"{len(res['no_birth_year'])} with no birth year, {len(res['away_skipped'])} away skipped")
        for grp in ("high_school_due", "ages_11_13_due"):
            for r in res[grp]:
                print(f"  {grp}  {r['name']}  last {r['last_test']}  {r['days']} days  age {r['age']}")
        for r in res["no_birth_year"]:
            print(f"  no_birth_year  {r['name']}  last {r['last_test']}")
    return 1 if n else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:
        print(f"hawkin_untested error: {e}", file=sys.stderr)
        sys.exit(2)
