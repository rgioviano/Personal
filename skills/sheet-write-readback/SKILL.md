---
name: Sheet write read-back
description: >-
  Use whenever you write to a spreadsheet (Google Sheets directly or through
  Zapier) or keep a running total in one. A success response is not proof the
  row is right: read it back, never retry blind, and treat the sheet as truth.
---
# Sheet write read-back

## Before a write (prospect rows)
Check for duplicates first: `python3 /home/box/agent-data/shared/scripts/chief/sheet_readback.py --prewrite --rows --key "Email Address" --intended <file> --readback <current sheet export>`. If it reports two matching rows, do not write; flag a possible duplicate.

## After every write
1. Save what you meant to write (JSON of cell/range to value, or the row) as a file. Re-read the row or cell you just wrote, looking it up by its key (email, row number, or cell address), not by trusting the write response, and save that re-read as a file.
2. Run `python3 /home/box/agent-data/shared/scripts/chief/sheet_readback.py --intended <file> --readback <file>` (add `--rows --key "Email Address"` for prospect rows; `--help` lists options). It compares name, email, phone, Contact Date, Stage, or the cell values, ignoring formatting-only differences.
3. Say "written and verified" only on exit 0. Any MISMATCH, MISSING, DUPLICATE, or NOT READ BACK line is a failure.

## On a mismatch or an error
- Mismatch: stop writing to that sheet for this run, and flag it to the owner or the user with the row, the field, what you wrote, and what you read back.
- Write error or timeout: look the row up first. Retry at most once, and only if the write is truly absent. If the second try fails or the lookup is unclear, stop and flag. Never loop retries.
- Two rows match one person or key: do not write. Flag a possible duplicate.

## Source of truth
- The sheet is the source of truth. Side files, logs, or memory notes that track the same thing are helpers; when they disagree with the sheet, the sheet wins and the difference gets flagged.
- Running totals: never add to a total you computed yourself. Read the sheet's own SUM or cells, then report.
- Counts parsed from chat: treat "add N" or "N more" as an increment only when the wording is explicit. A number that could be a total ("12 so far", "12 from Saturday to now") is ambiguous: ask before writing.

## Reconcile
For any sheet fed from messages (chat counts, form emails), run a recount once a day or once a week: re-count from the source for the period, compare with the sheet, and post any differences. Silent only when they match.
