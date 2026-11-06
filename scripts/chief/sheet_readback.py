#!/usr/bin/env python3
"""sheet_readback.py: Sheet write read-back. Did the Sheet end up holding what we meant to write?

The bot writes with its own connector, re-reads the row or cells, and exports both sides.
This script never calls Sheets or Zapier. It applies the Sheet write read-back skill:

  cells mode: every intended cell must read back the same value.
  rows mode:  look each intended row up by its key (email, phone or row number), never by the
              write response. 0 rows found = MISSING. 2+ rows = DUPLICATE (do not write again).
              A DUPLICATE prints once per key value, with the value written and every intended row that hit it.
              Each key field must match. Default fields: First Name, Last Name (both checked), a Name
              column if the sheet has one, email, phone, Contact Date, Stage, plus any other column
              in the intended row.
  AVERAGES:   rows mode stops at the first row with a cell saying AVERAGES (the 2026 tab's summary
              table, row 287) so its monthly counts are never read as contacts, and prints a NOTE.
  --key:      the lookup column. Composite keys are comma separated, e.g. --key "Email Address,First Name",
              so siblings who share a parent's email are told apart instead of coming back DUPLICATE.
              Fallback when there is no usable email: --key row with "row": N in each intended row.
  --prewrite: before a write, only checks the key: 0 rows = OK to add, 1 = update that row,
              2+ = DUPLICATE, do not write.
Values are compared after light normalising, so these count as equal: 5 / "5" / "5.0",
"10/21/2026" / "2026-10-21" / "Oct 21, 2026", "555-01-0001" / "6305550100", email case,
and extra spaces. Anything else that differs is a MISMATCH.
Stage is compared case-insensitively but trim-sensitively: "Eval Booked" matches "Eval booked",
" Eval booked" (stray space) does not.

Inputs:
  --intended  JSON. Cells: {"Daily log!C15": 5, ...}. Rows: [{"Email Address": "...", "Stage": "..."}, ...]
  --readback  JSON or CSV. Cells: {"Daily log!C15": "5"}, or a Sheets values read
              {"range": "Daily log!B15:F15", "values": [[3,5,3,"",""]]} (or a list of those).
              Rows: the sheet (or the re-read rows) as CSV, or JSON list of objects, or {"values": [...]}.

Usage:
  python3 sheet_readback.py --intended writes.json --readback readback.json            # cells
  python3 sheet_readback.py --rows --key "Email Address" --intended row.json --readback sheet.csv
  python3 sheet_readback.py --rows --prewrite --key "Email Address" --intended row.json --readback sheet.csv
  python3 sheet_readback.py --rows --key "Email Address,First Name" ...   # siblings sharing one email
  python3 sheet_readback.py --rows --key row ...                          # fallback: intended rows carry "row": N
  options: --fields "Full Name,Email Address,Phone,Contact Date,Stage", --json
Exit code: 0 written and verified (or OK to write), 1 mismatch / missing / duplicate, 2 script error.
"""
import argparse, csv, datetime as dt, json, re, sys

DEFAULT_FIELDS = ["first name", "last name", "=name", "=full name", "email", "phone", "contact date", "stage"]


def a1_to_rc(a1):
    m = re.fullmatch(r"\$?([A-Za-z]+)\$?(\d+)", a1)
    if not m:
        raise ValueError(f"bad cell {a1!r}")
    col = 0
    for ch in m[1].upper():
        col = col * 26 + (ord(ch) - 64)
    return int(m[2]), col


def rc_to_a1(r, c):
    s = ""
    while c:
        c, rem = divmod(c - 1, 26)
        s = chr(65 + rem) + s
    return f"{s}{r}"


def split_ref(ref):
    ref = ref.strip()
    if "!" in ref:
        tab, cell = ref.rsplit("!", 1)
        return tab.strip("'"), cell.replace("$", "").upper()
    return "", ref.replace("$", "").upper()


def norm(v):
    if v is None:
        return ""
    s = str(v).strip()
    s = re.sub(r"\s+", " ", s)
    if s == "":
        return ""
    t = s.replace(",", "")
    digits = re.sub(r"\D", "", re.sub(r"\.0+$", "", s))
    if re.fullmatch(r"[\d\s().+-]{10,}(\.0+)?", s) and len(digits) in (10, 11) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return "tel:" + digits[-10:]
    if re.fullmatch(r"-?\d+(\.\d+)?", t):
        f = float(t)
        return str(int(f)) if f == int(f) else str(f)
    for fmt in ("%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d", "%b %d %Y", "%B %d %Y", "%a %b %d %Y", "%A %B %d %Y"):
        try:
            return "date:" + dt.datetime.strptime(s.replace(",", ""), fmt).date().isoformat()
        except ValueError:
            pass
    m = re.match(r"(\d{4}-\d{2}-\d{2})[T ]00:00(:00)?", s)
    if m:
        return "date:" + m[1]
    if "@" in s:
        return s.lower()
    return s


def load_json_or_csv(path):
    if path.lower().endswith(".json"):
        return json.load(open(path, encoding="utf-8"))
    return list(csv.DictReader(open(path, newline="", encoding="utf-8-sig")))


def readback_cells(data):
    cells = {}
    blocks = data if isinstance(data, list) else [data]
    for b in blocks:
        if isinstance(b, dict) and "values" in b and "range" in b:
            tab, rng = split_ref(b["range"])
            start = rng.split(":")[0]
            r0, c0 = a1_to_rc(start)
            for i, row in enumerate(b["values"]):
                for j, v in enumerate(row):
                    cells[(tab, rc_to_a1(r0 + i, c0 + j))] = v
        elif isinstance(b, dict):
            for k, v in b.items():
                cells[split_ref(k)] = v
    return cells


def rows_from(data):
    if isinstance(data, dict) and "values" in data:
        vals = data["values"]
        hdr = [str(h).strip() for h in vals[0]]
        return [dict(zip(hdr, list(r) + [""] * (len(hdr) - len(r)))) for r in vals[1:]]
    if isinstance(data, dict):
        data = data.get("rows") or data.get("data") or [data]
    return data


def add_duplicate(findings, key, keyval, matches, n):
    """One DUPLICATE per key value, listing every intended row that hit it; wrote = the key value written."""
    read = f"sheet rows {', '.join(str(m[0]) for m in matches)}"
    for f in findings:
        if f["kind"] == "DUPLICATE" and f["wrote"] == keyval and f["read"] == read:
            f["intended_rows"].append(n)
            f["where"] = f"{key} (intended rows {', '.join(map(str, f['intended_rows']))})"
            return
    findings.append({"kind": "DUPLICATE", "where": f"{key} (intended row {n})", "wrote": keyval, "read": read,
                     "intended_rows": [n]})


def stop_at_averages(rows):
    """Contact rows end at the first row with a cell saying AVERAGES (any column, any case).
    Returns (rows, sheet_row_number_or_None); sheet row = list index + 2 (row 1 is the header)."""
    for i, r in enumerate(rows):
        vals = r.values() if isinstance(r, dict) else r
        if any(str(v).strip().upper() == "AVERAGES" for v in vals if v is not None):
            return rows[:i], i + 2
    return rows, None


def colmap(headers, wanted):
    """Map each wanted field to a header: exact (case-insensitive) first, then contains."""
    hl = {h.lower().strip(): h for h in headers}
    out = {}
    for w in wanted:
        exact_only = w.startswith("=")
        wl = w.lstrip("=").lower().strip()
        if wl in hl:
            out[w] = hl[wl]
            continue
        if exact_only:
            continue
        cands = [h for k, h in hl.items() if wl in k]
        if cands:
            out[w] = sorted(cands, key=len)[0]
    return out


def same(col, got, want):
    """Stage: case-insensitive, trim-sensitive. Everything else: norm()."""
    if col.strip().lower() == "stage":
        return str(got if got is not None else "").casefold() == str(want if want is not None else "").casefold()
    return norm(got) == norm(want)


def key_norm(v):
    s = str(v or "").strip()
    if "@" in s:
        return s.lower()
    d = re.sub(r"\D", "", s)
    if len(d) >= 10:
        return d[-10:]
    return s


def main():
    ap = argparse.ArgumentParser(description="Sheet write read-back: compare what was meant to be written with what the Sheet reads back (exported files in, no API calls).", epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--intended", required=True); ap.add_argument("--readback", required=True)
    ap.add_argument("--rows", action="store_true", help="row mode (prospect rows etc.)")
    ap.add_argument("--key", default="Email Address", help="row lookup column(s), comma separated for a composite key (e.g. \"Email Address,First Name\"); fallback: 'row' with \"row\": N in each intended row")
    ap.add_argument("--fields", help="comma list of fields to compare (rows mode)")
    ap.add_argument("--prewrite", action="store_true", help="rows mode: only check the key before writing")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    intended = json.load(open(a.intended, encoding="utf-8"))
    rb = load_json_or_csv(a.readback)
    findings, verified, notes = [], [], []
    if not a.rows:
        cells = readback_cells(rb)
        tabs = {t for t, _ in cells}
        for ref, want in intended.items():
            tab, cell = split_ref(ref)
            k = (tab, cell)
            if k not in cells and tab == "" and len(tabs) == 1:
                k = (next(iter(tabs)), cell)
            if k not in cells and not tab:
                hits = [kk for kk in cells if kk[1] == cell]
                k = hits[0] if len(hits) == 1 else k
            if k not in cells:
                findings.append({"kind": "NOT_READ_BACK", "where": ref, "wrote": want, "read": None})
            elif norm(cells[k]) != norm(want):
                findings.append({"kind": "MISMATCH", "where": ref, "wrote": want, "read": cells[k]})
            else:
                verified.append(ref)
    else:
        rows, stop = stop_at_averages(rows_from(rb))
        if stop:
            notes.append(f"stopped reading at sheet row {stop} (\"AVERAGES\" summary table); {len(rows)} contact rows read")
        if isinstance(intended, dict):
            intended = [intended]
        headers = list(rows[0].keys()) if rows else []
        for n, want in enumerate(intended, 1):
            if a.key.lower() == "row":
                rn = int(want.get("row") or want.get("Row"))
                matches = [(rn, rows[rn - 2])] if 2 <= rn <= len(rows) + 1 else []
                keyval = f"row {rn}"
            else:
                parts, bad_key = [], None
                for kname in [k.strip() for k in a.key.split(",") if k.strip()]:
                    kcol = colmap(headers, ["=" + kname]).get("=" + kname) or colmap(headers, [kname]).get(kname)
                    wk = kname if kname in want else colmap(list(want.keys()), [kname]).get(kname)
                    wkey = want.get(wk) if wk else None
                    if kcol is None:
                        bad_key = {"kind": "NO_KEY", "where": f"intended row {n}: sheet has no {kname!r} column", "wrote": wkey, "read": None}
                        break
                    if wkey is None or str(wkey).strip() == "":
                        bad_key = {"kind": "NO_KEY", "where": f"intended row {n}: {kname!r} is empty", "wrote": wkey, "read": None}
                        break
                    parts.append((kcol, wkey))
                if bad_key:
                    findings.append(bad_key)
                    continue
                keyval = " + ".join(str(v) for _, v in parts)
                matches = [(i + 2, r) for i, r in enumerate(rows)
                           if all(key_norm(r.get(kc)) == key_norm(wv) for kc, wv in parts)]
            if a.prewrite:
                if len(matches) > 1:
                    add_duplicate(findings, a.key, keyval, matches, n)
                else:
                    verified.append(f"{keyval}: {'update sheet row ' + str(matches[0][0]) if matches else 'not in sheet, OK to add'}")
                continue
            if not matches:
                findings.append({"kind": "MISSING", "where": f"{a.key} {keyval}", "wrote": "row", "read": None})
                continue
            if len(matches) > 1:
                add_duplicate(findings, a.key, keyval, matches, n)
                continue
            rn, got = matches[0]
            wanted_fields = [f.strip() for f in a.fields.split(",")] if a.fields else None
            wcols = colmap(list(want.keys()), wanted_fields or DEFAULT_FIELDS)
            if wanted_fields is None:
                wcols = {f: c for f, c in wcols.items()}
                for k in want:
                    if k not in wcols.values() and k.lower() != "row":
                        wcols[k] = k
            scols = colmap(headers, list(wcols.values()))
            bad = False
            for f, wc in wcols.items():
                sc = scols.get(wc)
                if sc is None:
                    findings.append({"kind": "NO_COLUMN", "where": f"row {rn} {wc}", "wrote": want.get(wc), "read": None})
                    bad = True
                elif not same(sc, got.get(sc), want.get(wc)):
                    findings.append({"kind": "MISMATCH", "where": f"row {rn} {sc}", "wrote": want.get(wc), "read": got.get(sc)})
                    bad = True
            if not bad:
                verified.append(f"{keyval} (row {rn})")
    res = {"verified": verified, "findings": findings, "notes": notes,
           "verdict": "STOP: do not write again this run; flag to the owner" if findings else
           ("OK to write" if a.prewrite else "written and verified")}
    if a.json:
        print(json.dumps(res, indent=2, default=str))
    else:
        for nt in notes:
            print(f"NOTE  {nt}")
        for f in findings:
            print(f"{f['kind']}  {f['where']}  wrote {f['wrote']!r}  read {f['read']!r}")
            if f["kind"] == "DUPLICATE":
                print("      several sheet rows share this key; if they are different people (siblings on one email), "
                      "re-run with a composite key, e.g. --key \"Email Address,First Name\"")
        if a.prewrite:
            for v in verified:
                print(f"OK  {v}")
        print(res["verdict"] if not findings else f"{len(findings)} problem{'s' if len(findings) != 1 else ''}. {res['verdict']}")
    return 1 if findings else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:
        print(f"sheet_readback error: {e}", file=sys.stderr)
        sys.exit(2)
