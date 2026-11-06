# bookmarks-sync-gate  (Token Officer, built 2026-10-19, NOT live)

**Replaces:** the `CRON_TZ=America/Chicago 17 9 * * 1,4` schedule on Bookmarks' "x-bookmarks-sync". It can also gate
"mental-models-synthesis" (`45 9 * * 1,4`), which only has work when new bookmarks land.

**Live schedule quoted by Bookmarks 10/19 08:52 CT:** x-bookmarks-sync Mon/Thu ~9:17 AM, enabled, last run 10/15 9:23 AM CT;
mental-models-synthesis Mon/Thu ~9:45 AM, enabled, first run 10/19.

**Logic:** pull the newest 100 X bookmarks for user 25647800, compare them to the `Tweet ID` column of the X Bookmarks Notion
data source (1c3a4778-...). Wake only if some id is missing. This is the same dedup rule as the 10/18 fix. An empty X pull
wakes the bot, because empty is treated as a possible error, not as zero. Read-only.

**Run**
- `python3 gate.py --fixture fixtures-2026-10-19`
- Live: `X_USER_TOKEN=... NOTION_TOKEN=... python3 gate.py`

**Missing to go live:** `X_USER_TOKEN` (bookmark.read), `NOTION_TOKEN` (read on the X Bookmarks DB), the Bookmarks webhook, and a scheduler.

## Wiring (updated 2026-10-19 7:25pm CT, rollout approved by Ryne 7:22pm CT)
- **Scheduler:** `../scheduler/` runs it with `--wake` at Mon/Thu 9:17 America/Chicago.
- **Secrets** (names only; the values are never printed or logged): `X_USER_TOKEN`, `NOTION_TOKEN`, `WAKE_URL_BOOKMARKS`, `WAKE_KEY_BOOKMARKS`.
  - The gate reads each one from the process env first, then from the box secret store (`/home/box/agent-data/box-secrets.json` → `card.NAME`) on every run.
  - If any are missing it prints/logs `missing secrets, no wake (missing: NAMES)` and exits 0 with nothing sent.
- **Wake:** `POST WAKE_URL_BOOKMARKS` with JSON, `Authorization: Bearer <key>` and `X-Automation-Key: <key>`. 8 s timeout, one try.
  - On failure, the payload (no secrets) is appended to `pending-wakes.jsonl`.
- **Target routine:** Bookmarks 'x-bookmarks-gate' webhook routine (folder `x-bookmarks-gate`; it skips synthesis when `new` is 0). The owner's cron stays ON for now, so expect double coverage until Ryne approves removing it.
- **Payload** always has `"new": <count>`.
- **Run log:** `run-log.jsonl`, one heartbeat line per run.

### Tested 10/19 7:25pm CT
- Dry-run on the 10/19 connector fixtures: SKIP.
- Dry-run on the synthetic fixtures: WAKE.
- `--wake` with no secrets: `missing secrets, no wake`, exit 0.
- `--wake` against a local fake endpoint with a dummy key: both headers arrived and it returned HTTP 200. A wrong key returned 401 and the payload went to the pending log.
- No real wake was sent.
