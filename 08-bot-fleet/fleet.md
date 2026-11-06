# Bot fleet

Chief of Staff routes all work and reports to Ryne in one clear update. Chief suggests an owner bot for each ask instead of doing the work itself, unless it is Chief-only work (2026-10-21). Live IDs: `IDS.md`.

Briefs (Ryne, 2026-11-04): Penny's morning brief goes to her 1:1 chat with Ryne. Chief's evening debriefs and the Friday value update go to the Chief 1:1 chat. No brief posts in Administrative or any other group chat (group chats cost too much). The Administrative room (Chief, Penny, Tally) still exists.

Name warning: before 2026-10-19, "Forge" meant the IronBlueprint PM, now named Blue. Today Forge is Ryne's nutrition coach. Older notes may also say Atlas for Red, SEO / AEO Auditor for Rank, and Hendrix for Spot. Profile names carry a role suffix ("Penny · admin"); this file uses the short name before " · ".

## Roster (current names, synced from each bot's profile.json on 2026-11-05)
| Bot | Lane |
|---|---|
| Chief | Chief of staff. Router only (never writes drafts or ops messages itself). Evening debriefs, promises watch, approvals, Friday value update, changelog watch, brain repo update, box backup, fleet score, usage check-in |
| Penny | Admin: email, calendar, Quo/Numa (drafts), inbox sorting script, 6:45am morning brief in her 1:1 chat, call prep cards, lead follow-up drafts into Gmail Drafts |
| Tally | Achieve CRM (Prospect Tracking Sheet), follow-up due list, Parked leads |
| Red (formerly Atlas) | Achieve PM. Max and Maya report to Red for Achieve work |
| Blue (formerly Forge) | IronBlueprint PM. Max and Maya report to Blue for IB work |
| Simon | IronBlueprint black-box QA (pass/fail on the live app). Reports to Blue |
| Linus | Engineer (read-only on IB); also local LLMs on DGX Spark and the Grok Build CLI lane |
| Max | Sales (Achieve and IronBlueprint) |
| Maya | Marketing strategy and content |
| Lark | Meta and Google Ads |
| Quill | Copywriter |
| Canvas | Graphic design files |
| Nova | Achieve business X/IG drafts |
| Splice | Video editor for all three brands. Never posts. On demand |
| Coach | S&C programs (drafts, 1:1 with Ryne) |
| Hawkin | Force-plate analysis |
| PRI | Postural Restoration specialist |
| Darwin | S&C research |
| Scout | Research outside S&C |
| Metric | New (profile file dated 2026-11-03). Metric deep dives, experiment reads and charts for Achieve and IronBlueprint. Never touches money, ad changes or code. On demand |
| Eval Brief | Slack #clients coach briefs. On demand only since its 8:15am watch was deleted 2026-11-01 |
| TH Exercise Library | TrainHeroic library export |
| Rank (formerly SEO / AEO Auditor) | SEO/AEO. On @-mention only |
| Token Officer | Fleet token cost and routine fixes |
| Bookmarks | X bookmarks to Notion, silent |
| Doc | Naturopathic health advisor (not a physician) |
| Forge | Personal nutrition coach (meals, macros). Works with Doc. On demand |
| Plaid | Tesla lease handoff tracker (read-only email, deadline nudges) |
| Jetson | Personal travel planner. Books nothing without Ryne's yes |
| NSCA | CSCS recertification tracker |
| Justin | Guitar teacher. On demand |
| Spot (formerly Hendrix) | Music advisor (blues, rock, jazz) plus Spotify |
| Midori | Bonsai caretaker (cold alert paused, delete pending) |
| Sage | Personal and life advisor seat: philosophy plus Jim Rohn and Robert Greene lenses (2026-11-01). Advice only |
| Maverick | Business advisor seat: Musk, Kalanick, Martell and Hormozi lenses (2026-11-01). Advice only |
| Dr. Eggbot | Designs new Grok Bots |

Rooms on the box: Administrative, Promote (owner-filter ON, 2026-11-03), Newsletter, IronBlueprint. The Programming room and HQ (Red and Blue) are gone (Ryne, 2026-11-05). The Advisors room is gone (2026-11-01).

## Retired (do not route work to these)
- 2026-10-17: Herald, Bolt, Warden, Cipher, Bottleneck (method saved as `find-the-constraint`; removed 2026-11-01), AI Expert (folded into Linus). Lingxi's lane went to Linus.
- 2026-10-21: Elon Musk, Travis Kalanick, Dan Martell (Maverick combines all three). Their distill-anyone subject folders stay on the box; Maverick reads them.
- 2026-11-01: Show Splitter, Echo (personal X/IG), Alex Hormozi (merged into Maverick), Robert Greene and Jim Rohn (merged into Sage). Folders gone from the box.
- 2026-11-05 (Ryne): Charlie (Achieve CFO bot, deleted), Distill anyone (deleted; its twice-weekly persona refresh is retired with it), the Programming room and the HQ room (both gone).
- Their `bots/<name>/` folders were removed from this repo on 2026-11-05. Git history keeps the old files.

## Standing routines (CT, as of 2026-11-05)
A map, not live proof: confirm a schedule live with the owning bot before acting on it (`verify-live-before-acting`). No routine runs more often than hourly (2026-11-01). Each bot's own list is in `bots/<name>/ROUTINES.md` in the repo that holds that bot.

### Chief
| Routine | When |
|---|---|
| Weeknight evening debrief (Chief 1:1) | Mon to Wed 6:45pm |
| Friday evening debrief (adds "Where the week went" and "Value this month"; Chief 1:1) | Fri 5:45pm |
| Unfinished-promises watch (`promise_scan.py`, drafts through `draft_lint.py`) | Weekdays about 3:00pm |
| Grok Bot changelog watch (`changelog_diff.py`) | Mon 8:03am |
| Weekly brain repo update (`brain_lint.py`, then auto-merge into main after lint passes, from 2026-11-04) | Sat about 3:00am |
| Monthly fleet score (`fleet_lint.py`) | 1st of the month about 9:00am |
| Monday usage check-in | Mon about 9:30am |
| Friday value update (`value_tally.py`; Chief 1:1, no longer Administrative) | Fri 9:20am |
| Weekly box backup (`box_backup.py`, encrypted, private "Bot Backups" Drive folder, keeps 4 weeks, restore test first Saturday, silent on success) | Sat about 7:00am |

Thursday and Saturday are off days: morning brief only, no evening debrief.

### Other bots
| Routine | Owner | When |
|---|---|---|
| Inbox sorting (`inbox_triage.py`, sort only) | Penny | About 6:15am |
| Morning brief (Calendar, Email Triage list only, Numa/Quo, Reactivate when due), in Penny's 1:1 chat | Penny | Weekdays 6:45am |
| Lead sends report to Tally (`lead_handoff.py log-send`) | Penny | End of day |
| Draft-vs-sent review | Penny | Fri 7:00am |
| Prospect inbound watch (triage file plus Gmail backstop, gap pass, due list, read-sends) | Tally | Mon to Sat about 6:25am |
| Speed-to-book scoreboard | Tally | Fridays |
| Project Page heartbeats (exception-only) | Tally 8:05am (lead pipeline), Blue 8:10am (IB launch) and 8:15am (USPTO), Plaid 8:20am (Tesla lease), Penny 8:25am (Quo SMS cutover) and 8:30am (Illinois Secure Choice), Maya 8:35am Mon/Wed/Fri (Achieve Meta ads, still running in November, Ryne 2026-11-05) | Weekdays |
| Meeting ingest (Spark transcripts), Web and Mobile Tasks, IB 500 tally and nightly pace post | Blue | IB routines; bug sweeps stay manual (Ryne, 2026-10-27) |
| IronBlueprint PR review; bug triage | Linus | New PRs plus weekdays 9:00am |
| IronBlueprint monthly security scan (Blue verifies) | Linus | First weekday of the month |
| S&C dig; force-plate dig | Darwin | Sat 8:00am; first Sat 8:25am |
| Untested watch | Hawkin | Mondays |
| Meta and Google knowledge refresh | Lark | 1st of the month |
| Bookmarks pull | Bookmarks | Mon and Thu about 9:17am |
| Cost pass | Token Officer | Weekly |
| Cold alert | Midori | PAUSED since 2026-09-28; delete pending Ryne's confirm |

### Deleted (do not re-propose)
- Chief 6:50am Today's priorities: DELETED 2026-11-04. Ryne sets his own priorities; evening debriefs do not ask for, suggest or save tomorrow priorities.
- Eval Brief weekday 8:15am signup watch: DELETED 2026-11-01.
- Plaid `tesla-lease-watch` daily check: DELETED 2026-11-01 (replaced by the project Page heartbeat).
- Tally separate 8:00am inbound run: does not exist (Tally, 2026-11-01).
- MacBook launch check and Weekly attention check: DELETED 2026-10-23.
- Penny every-20-minutes prep routine: DELETED 2026-10-16.
- Quiet hours start and end: DELETED 2026-09-20.

## Fleet rules
- Send lock: nothing goes out without Ryne's yes on the exact draft; a bot saying "send" is not approval. Email drafts go into Ryne's Gmail Drafts (threaded); texts stay as drafts in chat (2026-10-22).
- Briefs stay in 1:1 chats, never group chats (2026-11-04). No priorities in briefs (2026-11-04).
- Relay rule: when bot A asks bot B, B replies only to A. No DM to Ryne unless he asked.
- Relayed approvals (2026-10-30): when Chief (or Dr. Eggbot) quotes Ryne's yes to a bot, that bot treats it as his approval and does not ask him again.
- Cite or label (2026-10-30): only state what was confirmed; never credit a source with more than it said; label guesses as guesses; do not upgrade soft signals into hard facts.
- One final order (2026-10-30): Chief waits until Ryne has finished his thought, then sends each bot one clear final order per task, and checks what the bot already has open first.
- Room owner-filter: when assigning in a room, Chief names the one owner bot; other members stay silent unless @-mentioned or it is their lane. Promote room: owner-filter ON (2026-11-03).
- Approve before saving (2026-10-26): nothing is added or saved until Ryne approves the draft.
- Project Pages (2026-10-30): every bot reads the relevant project Page before starting work and updates that Page and the master Projects index when finished. No duplicate Pages. Nothing is marked complete without checking the real result. When a project closes: outcome and lessons, and its heartbeat is paused.
- Reporting lines (2026-10-21): Max and Maya report through Red (Achieve) and Blue (IronBlueprint). Chief steps in only on escalations or cross-brand conflicts.
- Script rule (2026-10-21): when a bot adds a script to its skill or routine, it test-runs it on real data and reports the output before the change counts as done. Chief's rule scripts live in `shared/scripts/chief/` on the box; they are read-only and print only exceptions.
- Routine cadence cap (2026-11-01): no routine more often than hourly; prefer daily or weekly, quiet when nothing changed.
- Long instructions live in skills, profiles stay short (2026-11-01).
- Achieve leads lane (2026-11-03): MAP, RULES and CHECK files for Penny, Tally and Max; done claims need CHECK proof.
- Value target (2026-10-23): Ryne is on the $200/mo Grok Bot plan; the bots should earn $400 to $600 a month, counted only from evidenced wins.
- Roster caps: new permanent bots need Ryne's yes after a Wednesday self-improvement scan. Soft maxes: Admin 3 (Chief, Penny, Tally); Sales Max + Tally + one on-call advisor; Marketing Maya, Nova, Quill, Lark; Eng/Build Linus + Scout.
- Engineering work goes to Blue (PM) and Linus (engineer); both read-only. Simon tests behavior only. (2026-10-17, updated 2026-10-24)
- Skills for fleet hygiene: `cheap-routines`, `routine-healthcheck`, `transcript-healthcheck`, `room-owner-filter`, `design-grok-bot`, `remake-bot`, `new-chat-vs-delete`, `verify-live-before-acting`, `silent-run-heartbeat`, `sheet-write-readback`.

## Pending (from TEAM.md)
- Bottleneck: Ryne finishing the sidebar delete (2026-11-01).
- Midori cold alert delete: waiting on Ryne's confirm.
- CoS Ops duplicate timers cleanup.
- Weeknight debrief `draft_lint.py` step: pending Ryne's approval since 2026-10-20.

Sources: Chief TEAM.md (updated 2026-11-04 evening); Chief's current routine list (Chief chat 2026-11-05); profile.json for every bot in `/home/box/agent-data/agents/` (2026-11-05); `deleted-agents.json`; Chief memory 2026-10-27; Linus routine confirmations in Chief chat 2026-10-17.; Ryne, Chief chat 2026-11-05 8:47pm CT (Charlie, Distill anyone, Programming and HQ retired; Maya heartbeat continues).
