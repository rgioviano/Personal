# linus-pr-review-gate  (Token Officer, built 2026-10-19, NOT live)

**Replaces:** the weekday `0 9 * * 1-5` (CT, ±15m) *backup cron* on Linus's "IronBlueprint PR review" routine.
The PR-opened trigger stays as is.

**Live schedule quoted by Linus 10/19 08:52 CT:** trigger on PR opened in IronBluePrint/frontend-website,
nodejs-backend, nexus-ai-agent, plus weekday cron 0 9 * * 1-5 (flexible ±15m). Enabled.

**Logic:** list open, non-draft PRs in the 3 repos → wake Linus only if any (repo#n, head_sha) isn't in
`/workspace/ironblueprint-agent-prep/pr-review-state.json` → `reviewed`. Read-only, and it never writes Linus's state.

**Run**
- Dry run with connector data: `python3 gate.py --fixture fixtures-2026-10-19`
- Live (read-only): `GITHUB_TOKEN=... python3 gate.py` (still a dry run; it only prints the wake)
- Real wake (only after Ryne approves): `GITHUB_TOKEN=... WAKE_URL_LINUS_PR=... WAKE_KEY_LINUS_PR=... python3 gate.py --wake`

**Missing to go live:** `GITHUB_TOKEN` (read-only on the IronBluePrint org; `gh` on the box isn't logged in),
a webhook trigger on Linus's routine (`WAKE_URL`), and a scheduler (the box has no cron daemon, so use Zapier Schedule + webhook, or install cron).

Dry-run outputs: `dry-run-2026-10-19.txt` (real data → SKIP) and `dry-run-synthetic-wake.txt` (injected new PR/new SHA → WAKE; draft ignored).
Each run appends one heartbeat line to `run-log.jsonl`.

## Wiring (updated 2026-10-19 7:25pm CT, rollout approved by Ryne 7:22pm CT)
- **Scheduler:** `../scheduler/` runs it with `--wake` at weekdays 9:00 America/Chicago.
- **Secrets** (names only; the values are never printed or logged): `GITHUB_TOKEN`, `WAKE_URL_LINUS_PR`, `WAKE_KEY_LINUS_PR`.
  - The gate reads each one from the process env first, then from the box secret store (`/home/box/agent-data/box-secrets.json` → `card.NAME`) on every run.
  - If any are missing it prints/logs `missing secrets, no wake (missing: NAMES)` and exits 0 with nothing sent.
- **Wake:** `POST WAKE_URL_LINUS_PR` with JSON, `Authorization: Bearer <key>` and `X-Automation-Key: <key>`. 8 s timeout, one try.
  - On failure, the payload (no secrets) is appended to `pending-wakes.jsonl`.
- **Target routine:** Linus 'IronBlueprint PR review' webhook routine (folder `ironblueprint-pr-review`). The owner's cron stays ON for now, so expect double coverage until Ryne approves removing it.
- **Payload** always has `"new": <count>`.
- **Run log:** `run-log.jsonl`, one heartbeat line per run.

### Tested 10/19 7:25pm CT
- Dry-run on the 10/19 connector fixtures: SKIP.
- Dry-run on the synthetic fixtures: WAKE.
- `--wake` with no secrets: `missing secrets, no wake`, exit 0.
- `--wake` against a local fake endpoint with a dummy key: both headers arrived and it returned HTTP 200. A wrong key returned 401 and the payload went to the pending log.
- No real wake was sent.
