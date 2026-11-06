# Chief rule scripts

Read-only scripts that apply one rule set to many items and print only the exceptions.
The first three were built 2026-10-20 for Chief's routines; the four check scripts below were added 2026-10-21. None of them send, edit, or delete anything.
Python 3 standard library only.

| Script | Used by | Checks |
|---|---|---|
| `fleet_lint.py` | Monthly fleet score (1st of month) | Every bot and room on disk vs the fleet rules and vs IDS.md, FLEET.md, TEAM.md |
| `brain_lint.py` | Weekly brain repo update (before the PR) | Secrets, client PII, em dashes in proposed content |
| `draft_lint.py` | Evening debrief, unfinished-promises watch, any draft review | Em dashes, prices, "Aurora", banned check-in phrases |

Exit codes for all of them: 0 clean, 1 exceptions found, 2 script error (report the error, do not guess).

## fleet_lint.py

```
python3 /home/box/agent-data/shared/scripts/chief/fleet_lint.py          # human list, also writes JSON
python3 /home/box/agent-data/shared/scripts/chief/fleet_lint.py --json   # JSON only
```
JSON always lands at `/workspace/routine-scripts/fleet_lint.latest.json` (change with `--out`).
Prints `0 exceptions` when clean.

Per bot (`agents/*/profile.json`, `settings.json`): empty name or description, no Self-fix line,
em dashes in name/title/description, unreadable settings.json, duplicate names, retired names
(CRM Watch, Personal Assistant 8b769a17, PA Schedules, Ledger, Morgan, Lingxi, AI Expert, Herald,
Bolt, Warden, Cipher, Bottleneck, CoS Ops) unless the nearby text says they are retired or stale,
SCDD Instant Form watch as active, Numa as preferred over Quo, Aurora in an ad-targeting sentence,
and IDs listed in `deleted-agents.json`.
Rooms (`group.json`): members that are deleted or have no folder.
On-disk routines (`automations/*/automation.json`, enabled only): schedules that fire on Sat/Sun or
between 9pm and 7am CT, and retired names in prompts. These copies can be stale, so each line says so;
confirm live with the owning bot before acting.
Docs: IDS.md bots/rooms missing on disk or with a different name, retired bots still on disk,
on-disk bots missing from IDS.md / FLEET.md / TEAM.md, TEAM.md IDs and names with no bot on disk.
Never reads `secrets/` or `store.db`.

Routine step: run it, paste the exception list (grouped by rule) into the fleet score, and score
the rest as passing. Do not re-read every profile by hand.

## brain_lint.py

```
python3 brain_lint.py /workspace/brains-push/stage            # every hit as file:line rule [REDACTED]
python3 brain_lint.py --summary /workspace/brains-push/stage  # counts per file and rule
git -C <repo> diff --cached | python3 brain_lint.py --diff -   # only added lines of a diff
python3 brain_lint.py --diff changes.diff --json
```
Rules: private keys, AWS AKIA/ASIA keys, Stripe sk_live/rk_live (and test keys, whsec_), mongodb and
other DB URIs with a password, JWTs, GitHub, Slack, Google, OpenAI-style and xAI keys, Bearer tokens,
user:pass in URLs, password/token/api_key assignments; client emails (anything but Ryne's business
addresses, calendar group IDs and example domains) and US phone numbers (the public Achieve number
630-340-4114 is allowed); em dashes. `--rules secrets,pii` skips the em-dash rule.
It never prints a matched value: only the rule name and `[REDACTED ... #hash]`, where the hash lets
you tell repeats apart. Default cap is 50 hits per file (`--max-per-file 0` for no cap).
Add one-off allowances with `--allow-email ADDR` or `--allow-phone NUMBER`.

Routine step: run it on the staged content or the PR diff before opening the PR. Any secret hit
blocks the PR. PII and em-dash hits get fixed or the file is left out, then re-run until exit 0.

## draft_lint.py

```
python3 draft_lint.py draft.txt
echo "$DRAFT" | python3 draft_lint.py
python3 draft_lint.py --not-lead draft.txt   # skip the price rule (draft is not to a lead)
python3 draft_lint.py --price-ok draft.txt   # skip the price rule (price was read live today)
```
Flags em dashes, $ amounts, "Aurora", "thanks / thank you (so much) for checking in", and
"reach out anytime". Prints `0 exceptions` when clean, else `line N:col rule "match"`.

Routine step (debrief, promise watch, any draft shown to Ryne): run each draft through it and
fix or mark HELD every exception before showing it.

## Test fixtures
`/workspace/routine-scripts/fixtures/` holds fake-value fixtures (`brain/`, `sample.diff`, `draft/`).
The fixtures contain em dashes and fake secrets on purpose so the scripts have something to catch.

## Check scripts (added 2026-10-21, not wired into any skill or routine yet)

These four take files the bot exported with its own connectors. None of them calls an API, reads a key,
or writes anything. Each has `--help` and `--json`. Exit 0 = pass, 1 = findings, 2 = script error
(including an empty export: empty is not zero).

| Script | For | Checks |
|---|---|---|
| `pre_draft_check.py` | Pre-draft check skill (Penny, Tally, Max) | READY or HELD with one-line reasons |
| `sheet_readback.py` | Sheet write read-back skill (Tally, Blue) | written and verified, or MISMATCH / MISSING / DUPLICATE |
| `ib500_recount.py` | IB 500 nightly pace post (Blue) | Slack count posts vs the Daily log tab |
| `hawkin_untested.py` | Hawkin untested watch (Hawkin, Monday weekly-trends) | who is due for a CMJ/SJ retest |

### pre_draft_check.py
```
python3 pre_draft_check.py draft.txt --contacts row.csv --touches touches.json --busy busy.json [--mode confirm] [--kind ad|email|text] [--no-signature]
python3 pre_draft_check.py draft.txt --workdir /workspace/predraft-test/<bot>-<person>-<timestamp>/ --contacts row.csv ...
```
Draft file may start with `To:`, `Phone:`, `Channel: email|text`, `Drafted:` lines, then a blank line, then the body.
A `Drafted:` date with no time counts as the end of that day.
Parent check: a "Parent X." note in Comments must name the To first name ("Parent Lisa." on a draft to Anthony HOLDS).
A WordPress Lead Form that names the lead's email or phone counts as their own words for the parent check (never as a touch).
In --mode confirm a bare "at 5" counts as checked when 5pm (with its day) is already in the draft.
--touches and --busy take several files (repeat the flag or list paths). A touches or calendar file with content but nothing
readable is ERROR, exit 2, never a pass. Quo plain text is read in the real layouts ("id | participant | direction | timestamp"
with the text on the next line, and "id | direction | timestamp | text"). Gmail entries with only a snippet use the snippet. Quo/Sona call or voicemail alert emails ("Sona handled a call from ...") are inbound touches from the caller,
labeled "they called <time> (Quo alert email)"; they hold within 48 hours like any message from them.
Until the Quo port finishes, texts land in Numa: Numa "New conversation"/"New message" notification emails (no-reply@example.com)
are inbound texts from the "Sent by" person, matched by phone or full name, labeled "they texted <time> (Numa notification)".
They hold within 48 hours or after the draft. "Still waiting" reminders are a note only.
--mode reply (or --reply-to <message id>): the message being answered, and earlier ones in the thread, are not touches;
any message after it still holds. Household contact: a To person not on the Sheet with the same last name as a row whose
own email/phone is empty or different, and whose email/phone is on no other row, is a WARN "household contact, confirm
relation"; an email/phone on a different row still HOLDS.
A Drafted date with no time, or no Drafted line, is a WARN (48-hour check approximate or not done).
Every time in a list is checked ("Wed 10/28 4pm or 6pm", "4, 5 or 6pm", "4pm/6pm", "4 or 6pm"), sharing the day and am/pm.
A weekday next to a date ("Wednesday 10/28", "Wed, 10/28") uses that date; a weekday alone means its next occurrence on or
after today and then gets the past-time check.
HOLD (exit 1): name plus phone or email not matching exactly one Sheet row; a real Gmail/Quo touch in the last 48h or
since the draft (WordPress Lead Form notifications and unsent drafts don't count); an offered time that has passed, a
weekday that doesn't match its date (also "Tuesday (10/21)"), or a clash with a busy block (blocks with the recipient's
last name are their own booking and are ignored); "your son/daughter" with no parent confirmation (parent column,
"Parent X." in Comments, or the lead's own "my son" message); a $ amount (always with `--first-touch`, else unless
`--price-source` names the live source); a draft older than 48h; draft_lint style rules; Aurora in ad or targeting wording
(any Aurora with `--kind ad`); for email, a partial or wrong signature (name only, a missing line, a different phone/email/URL,
extra lines after the block).
Email signature (since 2026-10-23): the Gmail connector's create_draft does NOT add Ryne's signature, so a saved email draft
must end with "Thanks,", a blank line, then the exact block (Ryne Gioviano, MSEd, CSCS / Owner, Achieve Sports Performance &
Personal Training / www.achievesportsperformance.com / blank line / For scheduling or account questions: /
Contact@achieve-personaltraining.com | Text: 630.340.4114). The full block passes; blank lines, extra spaces and a
Gmail-style htmlBody (`<div>` per paragraph, `<div><br></div>` spacers, `&amp;`, `&nbsp;`) are tolerated, since HTML
bodies are turned into text first. An email with no signature is a WARN "connector drafts need the full signature typed in"
(never for texts). `--no-signature` keeps the old rule for bodies checked without it (any typed signature HOLDS).
WARN (exit 0): a time with no day or am/pm ("See you at 5!") is NOT CHECKED; an offered slot later today; Aurora as a town
call-out; a closing line (the line before the signature) that is not "Thanks,"; an email with no signature; in `--mode confirm`, no booking with their last name at the confirmed time.
A missing export is NOT CHECKED and holds. Every run lists the checks that passed, including "phone check skipped" when
the draft has only an email but the row has a phone. `--busy` should cover all calendars (Achieve, where evals live,
Personal and Work). `--touches` accepts JSON or a Quo plain-text export (`timestamp | in/out | from | to | text`).
`--help` has the exact formats.

### sheet_readback.py
```
python3 sheet_readback.py --intended writes.json --readback read.json                 # cells, e.g. {"Daily log!C15": 5}
python3 sheet_readback.py --rows --key "Email Address" --intended row.json --readback sheet.csv
python3 sheet_readback.py --rows --key "Email Address,First Name" --intended row.json --readback sheet.csv   # siblings
python3 sheet_readback.py --rows --key row --intended row.json --readback sheet.csv   # fallback, rows carry "row": N
python3 sheet_readback.py --rows --prewrite --key "Email Address" --intended row.json --readback sheet.csv
```
Accepts a Sheets values read (`{"range": ..., "values": [[...]]}`). Ignores format-only differences (5 vs "5.0",
10/21/2026 vs 2026-10-21, phone punctuation, email case). Rows mode checks First Name and Last Name (both), email,
phone, Contact Date and Stage, plus any other column in the intended row. Stage is compared case-insensitively but
trim-sensitively ("Eval Booked" = "Eval booked"; " Eval booked" is a mismatch). NO_KEY shows the empty value it found. A DUPLICATE prints once per key value, with the value written (email or composite key) and the intended rows.
Both sheet_readback.py (rows mode) and pre_draft_check.py (--contacts) stop reading at the first row with a cell saying
AVERAGES, in any column and any case (the 2026 tab's summary table at row 287), and print a note with that row.

### ib500_recount.py
```
python3 ib500_recount.py --slack day-messages.json --sheet daily-log.csv --date 2026-10-21
```
Counts only explicit increments ("Add 5", "5 more", "5 done", "5 programs added"). Lists as ASK anything that could be a
total ("so far", "from Saturday to now", "total") or doesn't fit a pattern. Skips the pace post (anything with "N/500" or
"N of 500", after stripping markdown _ * ~ ` so "_213 / 500_" is a pace post too). The goal number 500 ("once we have
the 500 programs done") is never a count. Spelled-out numbers ("three programs in a row") count only next to an add verb
("added five", "five done"). Notes of 4+ lines (meeting notes, feedback lists) are skipped unless a line is an explicit add.
Also checks Day total and Running total against the person cells.

### hawkin_untested.py
```
python3 hawkin_untested.py --tests tests.csv --roster roster.csv --away away.csv [--markdown]
python3 hawkin_untested.py --hawkin-json /workspace/hawkin/<date>/cache.json --away away.csv --markdown
```
High school (14 to 18) last active CMJ/SJ 21 to 42 days ago; ages 11 to 13, 56 to 84 days ago. Age = year minus birth
year. Skips inactive athletes and trials and anyone on the away list not tested since being marked. Lists no-birth-year
athletes separately. `--markdown` prints the Slack post in the same layout as the 10/19 post.

### Tests
`tests/run_tests.sh` runs all cases (125 as of 10/21) and prints PASS/FAIL. Fixtures live in `tests/`:
`hawkin/` (real 10/19 export reduced to name, birth year and test dates, no metrics, no key), `ib500/` (rebuilt from
Blue's real tally log by `build_fixture.py`), `readback/` and `predraft/` (made-up people on example.com and 555 numbers, shaped like real past cases,
including anonymized copies of Penny's, Max's and Tally's 10/21 test cases). `predraft/D-rule-breaks-email.txt` has an em dash on purpose.


## Routine scripts (added 2026-10-23, Ryne approved scripting three Chief routines)

Same rules as above: the bot exports with its own connectors, the script filters, Python 3 standard library only,
no keys read, nothing sent. Exit 0 = nothing new/pass, 1 = findings, 2 = script error (empty input is an error, not zero).
Tests: `/workspace/.venv-pytest/bin/python -m pytest -q tests/test_changelog_diff.py tests/test_promise_scan.py tests/test_value_tally.py`
(30 cases as of 10/23; pytest lives in that venv because system pip is locked). Fixtures are made-up people on example.com,
except `tests/changelog/real-changelog-2026-10-23.html` (the public changelog page).

| Script | Used by | Does |
|---|---|---|
| `changelog_diff.py` | Grok Bot changelog watch (Mon) | live changelog vs `memory/changelog-last-seen.md`, prints only new releases |
| `promise_scan.py` | Unfinished promises watch (weekdays 3pm) | flags promises in Ryne's sent messages, drops fulfilled/skipped, prints due ones |
| `value_tally.py` | Friday value update (Fri 9:20am) | month total from `/workspace/value-tracker/YYYY-MM.md`, x of $200, gaps, unlogged sign-ups |

### changelog_diff.py
```
python3 changelog_diff.py              # fetch https://x.ai/changelog/bot, print new entries as JSON (read-only)
python3 changelog_diff.py --commit     # same, then write the newest entry to the last-seen file
python3 changelog_diff.py --html saved.html --no-items
```
Parses each `<article>` (time dateTime, h2 id = version, title, "Also includes", New/Improved/Fixed bullets).
New = later date than last seen, or same date with a higher version. 0 entries parsed (blocked or redesigned page)
is exit 2, never "nothing new". `--commit` only after the update was reported to Ryne.

### promise_scan.py
```
python3 promise_scan.py --sent sent.json --activity activity.json --since 2026-10-20 [--unanswered-hours 12] [--show-dropped]
python3 promise_scan.py --gmail-thread '/workspace/promise-scan/<date>/raw-thread-*.txt' --since <date>
```
Phrase list, non-promise list, action verbs, conditional patterns, built-in skip list and Ryne's addresses are at the top
of the script. Extra skips go in `promise_skip.txt` (one per line, `re:` for a regex). Strips quoted replies before
looking. Drops a promise when a later outbound message exists in the same thread or to the same email/phone (done),
when it matches the skip list, or when it is conditional on them ("Once you do that, we'll ...") and they have not
written since. Due date: today/tonight, tomorrow, weekday, next week, 10/30, Nov 2, in N days; no date = sent + 1 day
(`--grace-days`). Prints only overdue or due-today ones, each with `they_replied_after`. `--unanswered-hours N` also lists
inbound messages nobody answered (only as complete as the activity exported). `--gmail-thread` takes raw get_thread output.

### value_tally.py
```
python3 value_tally.py --month 2026-10 [--sheet prospect-2026.csv] [--since 2026-10-23] [--json]
```
Log line: `date | type | person | dollars | evidence` (types signup, autopay-recovered, winback, other). A line with no
dollar amount, no evidence or a date outside the month is listed as BAD and not counted: dollars are never estimated.
With `--sheet` (CSV, read_range JSON or values JSON of the 2026 tab; stops at AVERAGES) it lists rows with Sign-Up = Yes
and a Sign-Up Date in the month (on/after `--since`) whose name or email is not in the log, as CHECK items. Comment
amounts are shown as `comments_mention` only. A sign-up is not a bot win until the bot finds the bot follow-up evidence.
