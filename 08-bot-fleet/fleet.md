# Bot fleet

Chief of Staff routes all work and reports to Ryne in one clear update. Chief suggests an owner bot for each ask instead of doing the work itself, unless it is Chief-only work (2026-10-21). Shared ops channel: **Administrative** room (Chief, Penny, Tally). Live IDs: `IDS.md`.

Name warning: before 2026-10-19, "Forge" meant the IronBlueprint PM, now named Blue. Today Forge is Ryne's nutrition coach. Older notes may also say Atlas for Red and SEO / AEO Auditor for Rank.

## Roster (current names, updated 2026-10-31)
| Bot | Lane |
|---|---|
| Chief of Staff | Router only (never writes drafts or ops messages itself). Priorities, debriefs, promises watch, approvals, Friday value update, Grok Bot changelog watch, weekly box backup |
| Penny | Personal assistant: email, calendar, Quo/Numa (drafts), admin, inbox sorting script, 6:45am brief, call prep cards, lead follow-up drafts into Gmail Drafts |
| Tally | Achieve CRM (Prospect Tracking Sheet), follow-up due list, Parked leads |
| Red (formerly Atlas) | Achieve PM. Max and Maya report to Red for Achieve work |
| Blue (formerly Forge) | IronBlueprint PM. Max and Maya report to Blue for IB work |
| Simon | IronBlueprint black-box QA (pass/fail on the live app). Reports to Blue |
| Linus | Lead engineer (read-only on IB); also local LLMs on DGX Spark and the Grok Build CLI lane |
| Max | Sales (Achieve and IronBlueprint) |
| Maya | Marketing strategy and content |
| Lark | Meta and Google Ads |
| Quill | Copy chief; writes the Achieve Minute |
| Canvas | Graphic design files; designs the Achieve Minute |
| Nova | Achieve business X/IG |
| Echo | Ryne's personal X/IG |
| Splice | Video editor for all three brands. Never posts. On demand |
| Coach | S&C programs |
| Hawkin | Force-plate analysis |
| PRI | Postural Restoration specialist |
| Darwin | S&C research |
| Scout | Research outside S&C |
| Eval Brief | Slack #clients coach briefs |
| TH Exercise Library | TrainHeroic library export |
| Rank (formerly SEO / AEO Auditor) | SEO/AEO. On @-mention only |
| Charlie | Achieve CFO bot: QuickBooks read-only. Finance details stay out of the brains |
| Token Officer | Fleet token cost and routine fixes |
| Bookmarks | X bookmarks to Notion, Mondays and Thursdays about 9:17am CT, silent |
| Doc | Naturopathic health advisor (not a physician) |
| Forge | Personal nutrition coach (meals, macros). Works with Doc. On demand |
| Plaid | Tesla lease handoff tracker (read-only email, deadline nudges) |
| Jetson | Personal travel planner. Books nothing without Ryne's yes |
| NSCA | CSCS recertification tracker |
| Justin | Guitar teacher |
| Hendrix | Music expert, Spotify |
| Show Splitter | Concert MP3 splitter |
| Midori | Bonsai caretaker (cold alert paused, pending delete) |
| Sage | Philosophy mentor |
| Maverick | Business advisor (Musk, Kalanick, Martell lenses). Advice only |
| Persona bots | Alex Hormozi, Robert Greene, Jim Rohn (distilled voices) |
| Distill anyone | Builds and refreshes persona bots |
| Dr. Eggbot | Designs new Grok Bots |

Rooms without their own job description: Administrative, IronBlueprint, Promote, Newsletter, Advisors, Programming (stays active, Ryne 2026-10-17), HQ (Red and Blue, created 2026-10-20).

## Retired (pending sidebar delete by Ryne)
- 2026-10-17: Herald, Bolt, Warden, Cipher, Bottleneck (method saved as `find-the-constraint`), AI Expert (folded into Linus). Lingxi's lane went to Linus.
- 2026-10-21: Elon Musk, Travis Kalanick, Dan Martell (Maverick combines all three). Their distill-anyone subject folders stay; Maverick reads them.

## Standing routines (CT)
| Routine | Owner | When |
|---|---|---|
| Inbox sorting (`inbox_triage.py`, sort only) | Penny | About 6:15am daily, weekends included (run files 2026-10-24 to 2026-10-30) |
| Morning Administrative brief | Penny | Weekdays 6:45am |
| Today's priorities | Chief | Weekdays 6:50am |
| Evening debrief | Chief | Mon to Wed 6:45pm; Fri 5:45pm (Friday adds "Where the week went" and "Value this month") |
| Unfinished-promises watch | Chief | Weekdays 3:00pm |
| Friday value update | Chief | Fridays 9:20am, Administrative |
| Draft-vs-sent review | Penny | Fridays 7:00am |
| Weekly brain repo update | Chief | Saturdays about 3:00am |
| Weekly box backup (`box_backup.py`, encrypted, to the private "Bot Backups" Drive folder, keeps 4 weeks) | Chief | Saturdays about 7:00am; restore test first Saturday of the month; silent on success (from 2026-10-24) |
| Grok Bot changelog watch (`changelog_diff.py`) | Chief | Mondays 8:03am |
| Project Page heartbeats (exception-only) | Tally 8:05am, Blue 8:10am and 8:15am, Plaid 8:20am, Penny 8:25am and 8:30am, Maya 8:35am Mon/Wed/Fri | Weekdays, from 2026-10-30 |
| Monthly fleet score (`fleet_lint.py`) | Chief | 1st of the month |
| Inbound + gap pass, follow-up due list; speed-to-book scoreboard | Tally | Daily 8:00am; Fridays |
| #clients brief pass | Eval Brief | Weekdays 8:15am |
| S&C dig; force-plate dig | Darwin | Sat 8:00am; first Sat 8:25am |
| Untested watch | Hawkin | Mondays, from 2026-10-26 |
| Meta/Google knowledge refresh | Lark | 1st of month |
| Bookmarks pull | Bookmarks | Mon and Thu about 9:17am |
| Tesla lease check | Plaid | Replaced 2026-10-30 by the project Page heartbeat above; the old daily check is paused |
| Cold alert | Midori | PAUSED since 2026-09-28; delete pending Ryne's confirm |
| Cost pass | Token Officer | Weekly |
| Meeting ingest (Spark transcripts), Web & Mobile Tasks, IB 500 tally and nightly pace post, manual bug sweeps | Blue | IB routines. Bug sweeps stay manual (Ryne, 2026-10-27) |
| IronBlueprint PR review | Linus | New PRs + weekdays 9am |
| IronBlueprint bug triage | Linus | Blue handoff, #bugs, weekdays 9am |
| IronBlueprint monthly security scan | Linus (Blue verifies) | First weekday of month (from Mon 11/2) |
| Persona refresh | Distill anyone | Twice weekly |

Deleted 2026-10-23 (Ryne approved): MacBook launch check, Weekly attention check (folded into the Friday debrief). Penny's every-20-minutes prep routine was deleted 2026-10-16. Do not re-propose these.

## Fleet rules
- Send lock: nothing goes out without Ryne's yes on the exact draft; a bot saying "send" is not approval. Email drafts go into Ryne's Gmail Drafts (threaded); texts stay as drafts in chat (2026-10-22).
- Relay rule: when bot A asks bot B, B replies only to A. No DM to Ryne unless he asked.
- Relayed approvals (2026-10-30): when Chief (or Dr. Eggbot) quotes Ryne's yes to a bot, that bot treats it as his approval and does not ask him again.
- Cite or label (2026-10-30): only state what was confirmed; never credit a source with more than it said; label guesses as guesses; do not upgrade soft signals into hard facts.
- One final order (2026-10-30): Chief waits until Ryne has finished his thought, then sends each bot one clear final order per task, and checks what the bot already has open first.
- Room owner-filter: when assigning in a room, Chief names the one owner bot; other members stay silent unless @-mentioned or it is their lane.
- Approve before saving (2026-10-26): nothing is added or saved until Ryne approves the draft.
- Project Pages (2026-10-30): every bot reads the relevant project Page before starting work and updates that Page and the master Projects index when finished. No duplicate Pages. Nothing is marked complete without checking the real result. When a project closes: outcome and lessons, and its heartbeat is paused.
- Reporting lines (2026-10-21): Max and Maya report through Red (Achieve) and Blue (IronBlueprint). Chief steps in only on escalations or cross-brand conflicts.
- Script rule (2026-10-21): when a bot adds a script to its skill or routine, it test-runs it on real data and reports the output before the change counts as done. Chief's rule scripts live in `shared/scripts/chief/` on the box; they are read-only and print only exceptions.
- Value target (2026-10-23): Ryne is on the $200/mo Grok Bot plan; the bots should earn $400 to $600 a month, counted only from evidenced wins.
- Roster caps: new permanent bots need Ryne's yes after a Wednesday self-improvement scan. Soft maxes: Admin 3 (Chief, Penny, Tally); Sales Max + Tally + one on-call advisor; Marketing Maya, Nova, Quill, Lark; Eng/Build Linus + Scout.
- Engineering work goes to Blue (PM) and Linus (engineer); both read-only. Simon tests behavior only. (2026-10-17, updated 2026-10-24)
- Skills for fleet hygiene: `cheap-routines`, `routine-healthcheck`, `transcript-healthcheck`, `room-owner-filter`, `design-grok-bot`, `remake-bot`, `new-chat-vs-delete`.

## Pending (from TEAM.md)
- Ryne to sidebar-delete the 9 retired bots: Herald, Bolt, Warden, Cipher, Bottleneck, AI Expert, Elon Musk, Travis Kalanick, Dan Martell.
- Midori cold alert delete: waiting on Ryne's confirm.
- CoS Ops duplicate timers cleanup.

Sources: Chief TEAM.md (updated 2026-10-30; box backup 2026-10-24); Chief, Red and Doc profile.json (2026-10-30); Chief memory 2026-10-26 and 2026-10-27; Penny triage run files; Chief TEAM.md change log to 2026-10-23; `WS/fleet/IDS.md` (2026-10-21); shared memory 2026-10-21 to 2026-10-23; profile.json for Simon, Charlie, Splice, Plaid, Jetson, Forge, Maverick, Jim Rohn; Linus routine confirmations in Chief chat 2026-10-17; ib-500-tally-log.md; workflows skill list.
