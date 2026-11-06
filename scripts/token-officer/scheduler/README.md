# Gate scheduler (supervised loop, started 2026-10-19 7:25pm CT)

**Why not cron:** the box has no cron package (`apt-cache policy cron` shows no candidate), no systemd (PID 1 is `tini`), and no user boot hook. This is a small Python loop instead.

**What it does:**
- Every 30 s it checks the clock in America/Chicago.
- Jobs:
  - `linus-pr-review-gate` and `linus-bug-triage-gate`: weekdays 9:00.
  - `bookmarks-sync-gate`: Mon/Thu 9:17.
- Each job runs with `--wake`, at most once per local day. If the scheduler was down at fire time, the job catches up within 120 minutes.
- Last-fire dates are kept in `scheduler-state.json`, so a restart never double-fires.
- Logs: `logs/<job>.log` and `logs/scheduler.out`.
- Heartbeat with pid, alive time and next fire times: `heartbeat.json`.

**Commands:**
- Start (idempotent): `./ensure-running.sh`
- Verify: `./status.sh`. It prints RUNNING/NOT RUNNING, the heartbeat (`alive_at` should be under ~30 s old) and which secret NAMES are present (true/false only).

**Secrets:**
- The loop starts with a clean `env -i`, so it inherits no agent-shell secrets.
- Each gate re-reads `/home/box/agent-data/box-secrets.json` → `card` on every run. Grok Bot saved secrets (the ones agent shells see as env vars, listed in `CLOUD_AGENT_INJECTED_SECRET_NAMES`) live there.
- A secret Ryne saves later is picked up on the next run without a restart.
- Save them as named Grok Bot secrets with these exact names: `GITHUB_TOKEN SLACK_BOT_TOKEN BASECAMP_TOKEN X_USER_TOKEN NOTION_TOKEN WAKE_URL_LINUS_PR WAKE_KEY_LINUS_PR WAKE_URL_LINUS_BUGS WAKE_KEY_LINUS_BUGS WAKE_URL_BOOKMARKS WAKE_KEY_BOOKMARKS`.
- A sender key captured with the make-bot-ui "secret-request" card lands in `connector-secrets/<slug>/` instead, and the gates do NOT read it from there.

**Known gap:** the loop does NOT survive a box restart. The box last booted 10/19 4:07am CT. Something must run `ensure-running.sh` after each boot. See the parent report for the proposed fix.
