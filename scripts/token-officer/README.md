# Token Officer gate scripts (built 2026-10-19 3:53pm CT; rollout approved 7:22pm CT; scheduled via ./scheduler, waiting on secrets)

Each gate does the cheap "is there anything new?" check that a bot run currently does, and wakes the bot only when
there is something to do. Dry run is the default. Nothing is sent, and no bot state file is ever written.
`_wake.py` = shared stubbed wake + heartbeat log.

| Gate | Owning routine | Dry run 10/19 |
|---|---|---|
| linus-pr-review-gate | Linus / IronBlueprint PR review (weekday 9am backup) | SKIP: 7 open PRs, all reviewed at current SHA |
| linus-bug-triage-gate | Linus / IronBlueprint bug triage (weekday 9am backup) | SKIP: 3 #bugs posts, 18 open cards, all tracked |
| bookmarks-sync-gate | Bookmarks / x-bookmarks-sync (+ mental-models-synthesis) | SKIP: 97 bookmarks, all in Notion (107 rows) |

Skipped from the 10/17 ranking: #1 Penny before-call prep (deleted 10/16), #2 Forge IB 500 listener (live, but it's an event trigger
that last fired 10/13, ends Nov 1, and the ranking itself said not worth building), #3 and #6 Tally (the 8am watch folded into the Mon-Sat
6:25 lead log, which Chief says still needs a daily run).

Status 10/19 7:25pm CT: the scheduler is running (`scheduler/status.sh`). Every gate currently ends with `missing secrets, no wake` until the 11 named secrets are saved. Owner crons stay ON.
