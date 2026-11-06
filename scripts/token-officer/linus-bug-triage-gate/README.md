# linus-bug-triage-gate  (Token Officer, built 2026-10-19, NOT live)

**Replaces:** the weekday `0 9 * * 1-5` (CT, ±15m) *backup cron* on Linus's "IronBlueprint bug triage" routine.
The Slack #bugs message trigger stays as is.

**Live schedule quoted by Linus 10/19 08:52 CT:** trigger on any message in IB Slack #bugs, plus weekday cron
0 9 * * 1-5 (flexible ±15m). Enabled. Last run 10/19 12:17 AM CDT.

**Logic:** the 9am backup sweeps two places, so the gate checks both:
1. IB Slack #bugs (C0C8V38T082): top-level messages (thread replies ignored) at or after the oldest tracked ts and not in Linus's state.
2. Basecamp Bugs card table 10037160132 (project 47608498): open cards in Triage/Ready/In Progress/QA not in Linus's state.
"Tracked" means listed in `/workspace/ironblueprint-agent-prep/bug-triage-state.json` (triaged, skipped_non_bugs,
skipped_basecamp) or in `triage-locks/`. It wakes Linus only if something is untracked. Read-only.

**Run**
- `python3 gate.py --fixture fixtures-2026-10-19`
- Live: `SLACK_BOT_TOKEN=... BASECAMP_TOKEN=... python3 gate.py` (still a dry run unless `--wake` + `WAKE_URL`)

**Missing to go live:** `SLACK_BOT_TOKEN` (IB workspace, channels:history), `BASECAMP_TOKEN` (OAuth, account 6223040),
the Linus webhook (`WAKE_URL`), and a scheduler (no cron daemon on the box).

**Caveat:** a new #bugs post already fires Linus's Slack trigger. The gate mostly matters for Basecamp cards,
which today's 9am run found (BUG-17 to BUG-23).

## Wiring (updated 2026-10-19 7:25pm CT, rollout approved by Ryne 7:22pm CT)
- **Scheduler:** `../scheduler/` runs it with `--wake` at weekdays 9:00 America/Chicago.
- **Secrets** (names only; the values are never printed or logged): `SLACK_BOT_TOKEN`, `BASECAMP_TOKEN`, `WAKE_URL_LINUS_BUGS`, `WAKE_KEY_LINUS_BUGS`.
  - The gate reads each one from the process env first, then from the box secret store (`/home/box/agent-data/box-secrets.json` → `card.NAME`) on every run.
  - If any are missing it prints/logs `missing secrets, no wake (missing: NAMES)` and exits 0 with nothing sent.
- **Wake:** `POST WAKE_URL_LINUS_BUGS` with JSON, `Authorization: Bearer <key>` and `X-Automation-Key: <key>`. 8 s timeout, one try.
  - On failure, the payload (no secrets) is appended to `pending-wakes.jsonl`.
- **Target routine:** Linus 'IronBlueprint bug triage' webhook routine (folder `ironblueprint-bug-triage`). The owner's cron stays ON for now, so expect double coverage until Ryne approves removing it.
- **Payload** always has `"new": <count>`.
- **Run log:** `run-log.jsonl`, one heartbeat line per run.

### Tested 10/19 7:25pm CT
- Dry-run on the 10/19 connector fixtures: SKIP.
- Dry-run on the synthetic fixtures: WAKE.
- `--wake` with no secrets: `missing secrets, no wake`, exit 0.
- `--wake` against a local fake endpoint with a dummy key: both headers arrived and it returned HTTP 200. A wrong key returned 401 and the payload went to the pending log.
- No real wake was sent.
