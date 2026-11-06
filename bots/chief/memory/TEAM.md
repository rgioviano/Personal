# TEAM: Chief of Staff (updated 2026-11-04 evening)

Timezone: America/Chicago. Quiet hours routines: deleted 2026-09-20 (no fleet mute/unmute). Stale on-disk copies moved to `/home/box/agent-data/archive/chief-stale-automations-2026-11-01-lauren/` (2026-11-01).
Routine lines below are a map, not proof. Before acting on any schedule, confirm it live per [Verify live before acting](sand-workflow:verify-live-before-acting).
Shared ops channel: **Administrative** (`03ad987e-906d-42bb-98ea-65d016ffc77c`) still exists, but briefs no longer post there (Ryne, 2026-11-04: group chats too expensive). Morning brief → Penny 1:1; evening debriefs + Friday value update → Chief 1:1.

## Operating rules (locked)
- Never send email, texts, or Numa unless Ryne has seen that exact draft and says send.
- CoS saying “send” is not approval.
- Relay rule (locked 2026-10-17): when bot A asks bot B for something, bot B replies only to bot A. No DM to Ryne unless he is the one who asked.
- Briefs (Ryne, 2026-11-04): Penny owns morning Calendar + Email Triage list-only + Numa (+ Reactivate when due) in her Penny 1:1 DM. CoS owns evening debriefs and Friday value update in the Chief 1:1 DM. Do not post briefs in Administrative or other group chats. Full email drafts only when Ryne asks. No status chatter.
- Brief format (locked 2026-09-25): keep Calendar; drop Asana for good (connector never works); Meta ads = short bullets only on Mon/Wed/Fri when relevant in Wrap up; rest = important items only.
- NO PRIORITIES IN BRIEFS (Ryne, 2026-11-04): Ryne sets his own priorities. 6:50am Today's priorities routine DELETED. Evening debriefs do not ask for, suggest, or save tomorrow priorities.
- Routine cadence cap (locked 2026-11-01, Lauren ops): no routine runs more often than hourly. Prefer daily/weekly, weekday daytime, quiet when nothing changed; use an event trigger instead of a fast timer. Token Officer flags any routine under 60 minutes. See [Cheap routines](sand-workflow:cheap-routines).


## Page-based project management (approved 2026-10-30)
Master index: [Projects](https://cursor.com/canvas/store-3df0cc9c-950c-4cf8-a37a-04bc6830b1cf/0f122f19-31cd-4982-843a-fd9fa7e64d1a) (`0f122f19-31cd-4982-843a-fd9fa7e64d1a`).

Rules: every bot reads the relevant project Page before starting work and updates that Page (+ master index row) when finished. No duplicate Pages. Don't mark complete without checking the actual result. Fresh chats for tasks; Pages hold history. Exception-only notify Ryne (blocked / overdue / needs decision / status change). Never send, purchase, publish, or delete without Ryne's approval. On Closed: outcome + lessons, pause that project's heartbeat.

| Project | Owner | Page canvas_id | Heartbeat (CT weekdays, flexible) |
|---|---|---|---|
| IronBlueprint → Launch | Blue | `79f4b059-dceb-49c6-9ba6-c500ea702c5e` | ~8:10am LIVE `project-heartbeat-ironblueprint-launch` |
| Achieve lead pipeline | Tally | `137df122-e186-44f6-a925-064f061e28a0` | ~8:05am LIVE `project-heartbeat-achieve-lead-pipeline` |
| Achieve Meta ads (Oct) | Maya | `0b507d15-bdc4-4e88-be8e-b91e3bea13ad` | ~8:35am M/W/F LIVE `project-heartbeat-achieve-meta-ads-oct` |
| Quo SMS cutover | Penny | `6575614d-0a82-4407-bbe6-5c0ddc6a9266` | ~8:25am LIVE `project-heartbeat-quo-sms-cutover` |
| Tesla lease handoff | Plaid | `754db176-d86f-426c-b75e-36893675015f` | ~8:20am LIVE `project-heartbeat-tesla-lease-handoff`; old `tesla-lease-watch` DELETED 2026-11-01 (Plaid confirmed) |
| Illinois Secure Choice | Penny | `c75b9b91-384a-49dd-b5a6-e8f2bff17815` | ~8:30am LIVE `project-heartbeat-illinois-secure-choice` |
| USPTO IRONBLUEPRINT | Blue | `1cadb49d-75a1-452b-815a-3294a0b29b04` | ~8:15am LIVE `project-heartbeat-uspto-ironblueprint` |

## Current names (renames 2026-10-16; Atlas, old Forge and SEO / AEO Auditor renamed later, table updated 2026-10-21)
Profile names carry a role suffix since about 2026-10-26 ("Penny · admin", "Blue · IronBlueprint"). The short name before " · " is the bot's name in this file; `fleet_lint.py` matches it (2026-11-01).
Name warning: "Forge" before 2026-10-19 meant the IronBlueprint PM, now Blue. Today Forge (`2b406f18-aad6-4a09-bfd3-fe56b2b4f37e`) is Ryne's nutrition coach.

| Old name | Current bot |
|---|---|
| Personal Assistant / PA Schedules | Penny (`163cd8df-275e-47c1-a5a2-e10e304a671a`) |
| CRM / Ledger | Tally (`5d07e236-9453-409d-ab6c-58711eae2f09`) |
| Designer | Canvas |
| Ads | Lark |
| Achieve Social (business X/IG) | Nova |
| Achieve PM / Atlas | Red (`cf4fe585-7bd8-4d68-b32a-67aca0067033`) |
| IronBlueprint PM / old Forge | Blue (`cceeaf4d-4c7b-45fb-b736-9be1fdf15b88`) |
| Naturopath (Dr. Hale) | Doc |
| Spot | Hendrix |
| Performance Coach / Strength Coach | Coach |
| Marketing | Maya |
| Sales | Max |
| Copywriter | Quill |
| Engineer | Linus |
| S&C Research | Darwin |
| Research | Scout |
| SEO / AEO Auditor | Rank (`87fc5650-543f-4643-9dc1-deebc8ef54e8`) |

## Administrative members (current)
- Chief of Staff (this chat)
- Penny (`163cd8df-275e-47c1-a5a2-e10e304a671a`): owns weekday 6:45am morning brief in her 1:1 with Ryne (not Administrative; took over from the old Personal Assistant and PA Schedules)
- Tally (`5d07e236-9453-409d-ab6c-58711eae2f09`)

Old Personal Assistant (`a9da8358-…`) and PA Schedules (`88465cbe-…`) are gone. Do not @ them. CRM Watch is retired; do not @ CRM Watch for prospect work.

## Standing routines - owner: Chief of Staff (this chat)
| Routine | Schedule (CT) | Folder |
|---|---|---|
| ~~6:50am Today's priorities~~ | DELETED 2026-11-04 | Ryne owns priorities; routine removed |
| Weeknight evening debrief (Mon–Wed) | `45 18 * * 1-3` | weeknight-evening-debrief |
| Friday evening debrief | `45 17 * * 5` | friday-evening-debrief |
| Unfinished-promises watch | weekdays 3:00pm only | unfinished-promises-watch |
| Weekly brain repo update | Saturdays | weekly-brain-repo-update |
| Monthly fleet score | 1st of the month | live only (no on-disk copy) |

Thu + Sat are off days: morning brief only (no evening debrief). Fri evening is 5:45pm CT.

### Routine scripts (changed 2026-10-20)
Scripts live in `/home/box/agent-data/shared/scripts/chief/` (README.md there). Each one is read-only and prints only exceptions.
- Monthly fleet score: runs `fleet_lint.py` on every bot, room and fleet doc (IDS.md, FLEET.md, this file).
- Weekly brain repo update: runs `brain_lint.py` before any PR, then merges to main automatically after lint exits 0 (Ryne, 2026-11-04). A secret hit blocks the PR/merge; values are never printed.
- Unfinished-promises watch: runs each draft through `draft_lint.py` first.
- Friday evening debrief: runs drafts through `draft_lint.py`.
- Weeknight evening debrief: the `draft_lint.py` change is PENDING Ryne's approval (approval card sent 2026-10-20). Not live yet.

Priorities file (retired 2026-11-04; no longer written by evening debriefs): `/home/box/agent-data/agents/ad6690d7-be33-4540-ac42-68eb3059c181/memory/tomorrow-priorities.md`

## Other schedule bots
- Penny: 6:45am morning brief in her 1:1 DM (Mon–Fri only; moved off Administrative 2026-11-04). The every-20-minutes before-call prep routine was deleted 10/16 (Ryne approved). Before-call prep cards are now scheduled from the 6:45am morning brief (prep card about 30 min before each Achieve eval / IB demo; day-of confirm drafted that morning).
- Tally: Mon–Sat ~6:25am `prospect-inbound-watch` (inbound via Penny triage + Gmail backstop; gap pass; due list file via `lead_handoff.py post-due`; read-sends for logged sends); weekdays ~8:05am lead-pipeline Page heartbeat; Friday speed-to-book scoreboard. No separate 8:00am inbound routine (Tally, 2026-11-01).
- Eval Brief: weekday 8:15am signup watch DELETED 2026-11-01 (Ryne approved; Eval Brief confirmed). On demand only until Ryne says otherwise.
- Darwin: Saturday 8:00am S&C dig; first Saturday 8:25am force-plate dig.
- Lark: monthly Meta and Google knowledge refreshes on the 1st.
- Bookmarks: x-bookmarks-sync Mondays and Thursdays about 9:17am CT (changed by Ryne 10/12; verified with Bookmarks 2026-10-18), silent.
- Midori: cold alert (bonsai-cold-night) PAUSED since 9/28; Ryne asked to delete it 2026-10-18, pending his confirm in Midori's chat.
- Token Officer: weekly cost pass.
- Blue: IB routines (meeting ingest, web/mobile tasks).
- Plaid: Tesla lease Page heartbeat ~8:20am CT weekdays (`project-heartbeat-tesla-lease-handoff`); old `tesla-lease-watch` deleted 2026-11-01.
- Distill anyone: twice-weekly persona refresh.

## Bot roster: bots not covered above (added 2026-10-21)
One-line jobs from each bot's profile.json. IDs are agent folders on disk.
- Red (`cf4fe585-7bd8-4d68-b32a-67aca0067033`): Achieve PM. Owns the Achieve brand, coordinates bots on gym work, files Coach's finished programs. Formerly Atlas. Max and Maya report to Red for Achieve work (2026-10-21).
- Blue (`cceeaf4d-4c7b-45fb-b736-9be1fdf15b88`): IronBlueprint PM. Owns everything IronBlueprint, runs the IB bots, Basecamp is the source of truth. Formerly Forge. Max and Maya report to Blue for IronBlueprint work (2026-10-21).
- Rank (`87fc5650-543f-4643-9dc1-deebc8ef54e8`): SEO/AEO. Tracks keyword, technical, AI-prompt and competitor movement and returns an optimization plan. Formerly SEO / AEO Auditor.
- Splice (`78243869-cbf6-458c-bc54-0c2f5761b198`): video editor. Turns raw footage into ready-to-post edits for Achieve, IronBlueprint or the personal brand. Never posts. On demand.
- Plaid (`e9e0ed13-6c69-4849-8c61-8046655580e6`): Tesla lease handoff. Tracks the current lease return and the new lease through delivery, read-only on email, nudges on deadlines.
- Forge (`2b406f18-aad6-4a09-bfd3-fe56b2b4f37e`): personal nutrition coach. Logs meals, estimates macros, coaches toward muscle gain, fat loss and health. Works with Doc. On demand.
- PRI (`e9d0fc7f-22cc-4b14-80a6-4b8361108e36`): Postural Restoration Institute specialist for Achieve athletes (pattern recognition, breathing and ZOA work, technique selection).
- NSCA (`30219af9-fdf8-47e6-abd9-e97a0c953950`): tracks Ryne's NSCA recertification (CEUs, fees, deadlines) so it does not lapse.
- Justin (`c7a7b01f-ecbe-41aa-8f5e-73e22419f868`): personal guitar teacher with a progressive plan. On demand only.
- Dr. Eggbot (`f38722d3-a9d5-4d98-b294-ee15f3361f11`): bot maker. Asks preference questions, then designs and creates new Grok Bots.
- Sage (`99b4a25d-4d82-4a64-b955-4e756140e461`): personal/life advisor seat (2026-11-01). Philosophy plus Jim Rohn and Robert Greene lenses; answers from whichever fits Ryne's situation. Advice only.
- Alex Hormozi: RETIRED 2026-11-01, merged into Maverick (folder gone, in deleted-agents.json). Do not route work to it.
- Robert Greene: RETIRED 2026-11-01, merged into Sage (folder gone, in deleted-agents.json). Do not route work to it.
- Jim Rohn: RETIRED 2026-11-01, merged into Sage (folder gone, in deleted-agents.json). Do not route work to it.
- Maverick (`2772b984-fa9d-4c82-90e4-ea4bc1feae0b`): single business advisor seat (Musk/Kalanick/Martell lenses, plus Hormozi since 2026-11-01), created 2026-10-21. Formerly Boardroom. Advice only, no sends. Reports to no one (advisor). Not in the Advisors room. Self-fix line added 2026-10-21. Replaces the retired Elon Musk, Travis Kalanick and Dan Martell bots (2026-10-21).
- Jetson (`1f99ce18-87fe-439a-896b-b4d2c8182bd8`): personal travel planner (flights, stays, itineraries), created 2026-10-21 in Personal as Travel, renamed Jetson same day; teardrop, cyan. Books nothing without Ryne's yes; hands booked dates to Penny for the calendar. Current trips: John Mayer show (Apr 2027), Wyoming (Jun 2027).
- Rooms on disk not named above: HQ (`10dece0d-b4a4-4ab7-b0f7-3fe8ad7b6765`, Red and Blue, created 2026-10-20), Promote, Newsletter, IronBlueprint, Programming. The Advisors room folder is gone from disk (checked 2026-11-01). Full list in `/workspace/fleet/IDS.md`.
- Bottleneck (`c5d9f0a7-0864-407c-9ae2-7aae48909c69`) stays RETIRED (2026-10-17); REMOVED from the roster, Ryne is finishing the sidebar delete (2026-11-01). Folder still on disk as of 2026-11-01.
- Elon Musk, Travis Kalanick and Dan Martell are RETIRED (2026-10-21); their agent folders are gone from disk (checked 2026-11-01), so their IDs were dropped here (still listed in `/workspace/fleet/IDS.md` retired table). Maverick combines all three. Do not route work to them. Their distill-anyone subject folders (`/home/box/agent-data/distill-anyone/subjects/elon-musk`, `travis-kalanick`, `dan-martell`) STAY: Maverick reads them and the Distill daily routine keeps refreshing them. Keep `companion_agent_id` in each subject's PROFILE.json so Distill daily does not create a new companion bot.

## Bot roster: bots added 2026-11-01 (fleet-score fix, Ryne approved)
One-line jobs from each bot's profile.json (names before " · "). IDs are agent folders on disk.
- Simon (`48b8dd87-193d-4128-8463-4a6f523dc8fa`): black-box QA for IronBlueprint. Tests the live app from outside, pass/fail to Blue (his lead), fails also to Linus. Never reads or changes code. No routines on disk.
- Charlie (`5217cd51-c36e-4f22-83b7-3a2382a7957c`): CFO for Achieve. Reads QuickBooks Online (read-only) and explains cash, money in, money out, trends. Never writes to QuickBooks or moves money. On demand.
- Canvas (`567bde28-effb-4c09-bad5-579aa0d6d7ec`): graphic designer for Achieve and IronBlueprint (images, PDFs, slides, lead magnets, ad statics).
- Coach (`5d64c948-3315-41b3-b9a6-196b4d1e2072`): S&C coach; designs athlete programs 1:1 with Ryne (drafts only), finished programs to Red.
- Doc (`4fe8ab9a-957c-48ea-8e12-5cff32e2388a`): personal naturopathic health advisor (education, not a physician). Works with Forge.
- Echo: personal X and Instagram drafts. Folder gone from disk, in deleted-agents.json (checked 2026-11-01). Do not route work to it.
- Hawkin (`93d38eed-d001-4265-a229-8527e2efa46f`): reads Achieve's Hawkin force plates, analyzes tests and trends, writes plate-driven prescriptions.
- Hendrix (`5a0276a8-6560-4018-b4ac-b889ca11cbb3`): music advisor (blues, rock, jazz) plus Spotify.
- Lark (`bf5d1606-57b1-4b0d-b7f3-c5a52f934a2a`): Meta Ads and Google Ads platform expert for both brands; owns the in-platform build.
- Linus (`5ec70d9b-e978-4b41-8c2f-f2219c13815a`): engineer. Read-only advisory on IronBlueprint code (Suffescom devs code), local LLMs, Grok Build CLI lane.
- Midori (`0e8c74eb-4d9c-4850-9c37-e831fccf92a2`): caretaker for Ryne's rainbow dwarf jade bonsai.
- Nova (`6b3492d4-c1d7-448a-bed0-38dbb76b7828`): Achieve business X and Instagram post drafts and captions from Maya's briefs. Drafts only.
- Quill (`aa920346-b0d4-4e99-854d-8d288d0dc1ff`): copywriter for Achieve and IronBlueprint. Drafts only.
- Scout (`620dd6ee-1975-442b-be2a-a64a7a88c07b`): researcher for anything outside S&C (S&C evidence goes to Darwin).
- Jetson is listed in the 2026-10-21 roster above.

## Reporting lines: Max and Maya (approved 2026-10-21)
- Max (sales, `6404a542-bb7c-48e5-822a-a2afd90ad591`) and Maya (social strategy, `c37d4499-a97f-4961-bfcb-9df42e9376a3`) report through Red for Achieve work and Blue for IronBlueprint work, not to Chief.
- Red and Blue review Max's and Maya's output for their brand before it goes to Chief or Ryne.
- Chief only steps in on escalations or cross-brand conflicts.
- Profile edits: proposed in `/workspace/fleet/proposed-2026-10-21-reporting/` (Max, Maya, Red, Blue), to be applied by Chief via UpdateAgent.

## CRM ownership (approved 2026-09-16)
- Tally owns Prospect / WordPress Lead Form → Prospect Tracking.
- Daily at 8:00am CT, Tally checks WordPress Lead Form emails whose subject begins `Lead Form -` or `form Submission`.
- Add genuinely new prospects to the top of the 2026 Prospect Tracking tab with Website source.
- Penny flags other confirmed first-time email prospects to Tally for logging.
- The SCDD Instant Form watch remains retired.
- Alex Boomgarden was caught up and added at row 259 on Sep 16; Tara Simpson and Efuru Harmon-Miller already existed.

## Pending
- [x] Retire CRM SCDD watch (done 2026-09-15; routine deleted)
- [ ] CoS Ops must delete its duplicate five timers (asked 2026-09-09 night)
- [ ] Sidebar-delete old fat CoS if still visible (agent folder already gone)
- [ ] CoS Ops itself optional to sidebar-delete after its timers are gone
- [x] Show Splitter, Jim Rohn, Robert Greene, Alex Hormozi (and Echo): folders gone, in deleted-agents.json (checked 2026-11-01).
- [ ] Ryne to sidebar-delete the 9 retired bots (see change log 2026-10-17 and 2026-10-21): Herald, Bolt, Warden, Cipher, Bottleneck, AI Expert, Elon Musk, Travis Kalanick, Dan Martell. Update 2026-11-01: only Bottleneck's folder is still on disk (Ryne finishing it); the other 8 folders are gone from disk (app delete not confirmed in deleted-agents.json).
- [x] Programming room (`7c23ca84-4ef9-4dd7-8421-66e0ab6932ec`) stays ACTIVE (Ryne, 2026-10-17). Do not archive or delete it.

## Darwin standing dig (locked 2026-09-25)
- Owner: Darwin (`d38c0d3f-1a03-4e7e-9ca3-b73ac3057287`)
- Schedule: Saturday 8:00am CT (`CRON_TZ=America/Chicago 0 8 * * 6`)
- Output: 3–5 papers in Darwin's chat for Ryne; then route by relevance to Coach (programming) and Hawkin (plates/testing); silent if nothing new

## Eval Brief → Slack #clients (locked 2026-09-27)
- Owner: Eval Brief (`690e65de-c38a-4858-b3cd-831335e62504`)
- Drive Clients folder: `1o_k6aDUbkWcSJGYXwYbmI9wF-Hi78VAF` (NameAssessmentMM.DD.YY; skip templates + *Program)
- Gate: Prospect Tracking Sign-Up = Yes (and/or paid Mindbody). Eval-only never posts.
- Channel: Slack #clients `C1J8VTFU4`. Draft-first; Ryne approves before post.
- Watch: the weekdays 8:15am CT routine was DELETED 2026-11-01 (Ryne approved; Eval Brief confirmed it had still been running through 10/30).
- Locked on Grok Bot for now (not Cursor) as of 2026-09-27.

## Achieve Meta ads M/W/F (locked 2026-09-17)
- Standing 45–60 min Mon/Wed/Fri only. Checklist: `memory/achieve-meta-ads-mwf-block.md`.
- Evening wrap may note leftover Marketing ads block items; Penny may mirror on Calendar briefs when Maya/Lark is on the day. (6:50 priorities deleted 2026-11-04.)
- Sep pre-launch SCRAPPED 2026-09-23. Prep = October Day 1 (Oct 1). October chapter ($500/mo).

## Roster caps (locked 2026-10-06)
New permanent bots need Ryne's yes after a Wednesday self-improvement scan. Soft maxes:
- **Admin:** CoS + Penny + Tally. No extra admins by default.
- **Sales:** Max + Tally + one advisor on-call (not permanent seats for every advisor).
- **Marketing:** Maya + Nova + Quill + Lark. Rank and Canvas only when @-mentioned.
- **Eng / Build:** Linus + Scout. (Bottleneck retired 2026-10-17; use the Find the constraint skill instead.) Cloud agents and one-offs do not get a room seat.

## Call prep + promises (updated 2026-10-17)
- Penny: before-call prep cards for Achieve evals and IB demos, scheduled from the morning brief (who accepted, leave-with, talking points, do-nots; IB free/busy → UNVERIFIED).
- CoS: unfinished-promises watch weekdays 3:00pm CT only (`unfinished-promises-watch`). Quiet when nothing overdue. Drafts only.

## Prospect Tracking stages + contacts (locked 2026-10-06)
Tally owns process stage and contact count on every open row (evidence from Gmail / Quo / calendar / sheet only). Suggested stages: New inquiry → Replied → Eval booked → Eval done → Offer → Signed / Lost / Hold.

## Lauren ops 2026-11-01 (Ryne approved items 1, 2, 3, 6 from the @poteto team guide)
Source: Ryne t773u 2026-11-01. Drafts and evidence: `/workspace/fleet/` (`lark-profile-short-2026-11-01.md`, `penny-tally-handoff-2026-11-01.md`, `owner-access-audit-2026-11-01.md`, `reviewers-2026-11-01.md`).

**Roster changes (same day):**
- Show Splitter RETIRED (Ryne overrode his 10/17 "leave as is").
- Jim Rohn + Robert Greene merged into **Sage** = personal/life advisor seat (answers from whichever lens fits).
- Alex Hormozi merged into **Maverick** = the one business advisor seat (Musk/Kalanick/Martell + Hormozi).
- Distill companion remaps: subjects `jim-rohn` and `robert-greene` → Sage (`99b4a25d`); `alex-hormozi` → Maverick (`2772b984`). Distill daily keeps refreshing these subjects and must not create new companion bots.
- All four retired folders are gone from disk (deleted-agents.json); Echo's folder is gone too. Eggbot stays (Ryne already has it).

**1. Long instructions live in skills, profiles stay short.**
- New skills: [Meta and Google Ads playbook](sand-workflow:meta-google-ads-playbook) (from Lark), [Design model routing](sand-workflow:design-model-routing) (from Canvas).
- DONE 2026-11-01: Lark and Canvas short descriptions live via UpdateAgent; both confirmed skills ([Meta and Google Ads playbook](sand-workflow:meta-google-ads-playbook), [Design model routing](sand-workflow:design-model-routing)). Lark's monthly refreshes edit the skill, not the profile.
- Next candidates when a profile goes over ~3,000 chars: Justin, Coach, Tally, Simon, Midori, Nova, Hawkin.

**2. No list handoffs in chat (Penny ↔ Tally first).**
- Script `/home/box/agent-data/shared/scripts/handoff/lead_handoff.py` (README there); files in `/home/box/agent-data/shared/handoffs/penny-tally/`.
- New leads: Tally reads Penny's 6:15 triage file (`triage-leads`), Gmail stays the backstop. Due list: Tally writes `due/DAY.md` (`post-due`), Penny reads it (`read-due`). Sends: Penny logs each real send (`log-send`), Tally reads them (`read-sends`).
- Chat between Penny and Tally is for exceptions only. LIVE 2026-11-01: Tally updated `prospect-inbound-watch` + Standing (triage-leads / read-sends / post-due; no chat due list). Penny updated `6:45am morning brief` + `lead-sends-report-to-tally` + morning-brief skill (read-due / log-send; no chat send list). Backups under `penny/routines-backup/`.

**3. Routine cadence cap + stale copies + brand connectors.**
- No routine more often than hourly (rule added under Operating rules).
- Chief's stale on-disk `quiet-hours-start` / `quiet-hours-end` copies archived (live ones were deleted 2026-09-20). The stale `5-35am-today-s-priorities` copy is still on disk (not part of this approval).
- Brand connector rule (proposed, see audit): Achieve work uses the `--work`/`--contact`/`--achieve` connectors, IronBlueprint work the `--ironblueprint` ones plus Basecamp, personal work `--personal`, X, Notion, Spotify. Cross-brand bots say which set they used. `user-Gmail` (no suffix) stays unused until Chief confirms which account it is. Proposed owners for "unclear" bots are in `owner-access-audit-2026-11-01.md` (not applied, except PRI → Red, which the profile states).

**6. One reviewer + a done bar per lane.**
| Bot | Reviewer | Done when |
|---|---|---|
| Nova | Maya (Red for brand claims) | Post draft with hook, caption, asset note; passes brand lock; waits for Ryne's yes to post. |
| Quill | Maya (Red/Blue for brand facts) | Final lines for the named field/asset, within limits, no invented prices or claims. |
| Canvas | Maya (Red Achieve / Blue IB) | Real file in chat, right size and brand, prices from the locked sheet. |
| Lark | Maya; Ryne approves spend | Names account, date range, currency, total spend and one ranked action, ready for Ryne's yes. |
| Rank | Maya | Ranked fix list with evidence and an owner per fix; nothing published. |
| Coach | Ryne approves; Red files | Program passes the style and design skills, Ryne OKs it, Red has filed it. |
| Hawkin | Coach | Pull finished the same turn, units and dates, FLAG_EMPTY_PULL on 0 tests, blocks to Coach. |
| PRI | Coach | Pattern, tests, technique family, specific Achieve-safe exercises and cues. |
| Darwin | Coach (programming) / Hawkin (plates) | 3-5 papers with citation, how it fits Achieve, unknowns; routed; silent if nothing new. |
| Eval Brief | Red | #clients brief draft for a verified sign-up, waiting for Ryne's yes. |
| TH Exercise Library | Red | Count exported, Sheet URL, failures listed. |
| Charlie | Ryne (Chief for ops) | Cash by account from QBO with as-of date; gaps named. |
| Scout | Whoever asked (Red / Blue / Chief) | Answer, best links, unknowns; primary sources. |
| Token Officer | Chief | Runs/week saved; only approved fixes applied and read back live. |
| Dr. Eggbot | Chief | New bot has one job, anti-jobs, reviewer + done bar, and is in TEAM/FLEET/IDS. |
| Distill anyone | Chief | Subject refreshed, companion id unchanged, no new bot. |
| Bookmarks | Chief | New bookmarks filed, state advanced, heartbeat logged. |
| Plaid / Jetson / NSCA | Penny | Page or plan current; deadlines or booked dates on the calendar; nothing booked or sent without Ryne. |
| Forge | Doc | Meal logged with macros and one next step. |
| Midori, Doc, Hendrix, Justin | Ryne | Answer he asked for; never posts or books. |
| Splice | Bot that sent the job | Edited file delivered; never posts. |
| Sage, Maverick | none (advisors) | n/a |

Reviewer picks not stated in a source are Chief's proposals (marked [guess] in `reviewers-2026-11-01.md`); Ryne can swap any one.

## Achieve leads triad (approved 2026-11-03)
- Lauren Tan–style MAP / RULES / CHECK for the Achieve leads lane.
- Live files: `/home/box/agent-data/shared/lanes/achieve-leads/{MAP,RULES,CHECK}.md`
- Readers: Penny · admin, Tally · crm, Max · sales (one profile line each).
- Rule 0: when Ryne corrects anyone in the lane, that bot appends one dated line to RULES.md and tells Chief.
- Done claims require CHECK proof. Quo Support +16303404114 is default outbound SMS (cutover Closed 11/3; Alternate interim dropped). Sheet columns follow the 10/22 live header.

## Promote room owner-filter (approved 2026-11-03)
- Ryne approved the 11/2 fleet-review recommendation: owner-filter ON in Promote.
- Rule: only the bot Ryne @-mentions answers that turn. With no @:
  - Quill drafts the lines
  - Maya reviews for brand/offer fit
  - Lark Meta-QAs once on the final package before Ryne's yes (not every rewrite)
  - Max speaks only when the offer or the lead is involved
- Profile lines live on Lark, Maya, Quill (Max already had the room rule). Follow [Room owner-filter](sand-workflow:room-owner-filter).
- Do not change Promote membership, reviewer table, athlete-first November social, or Achieve Minute HOLD.

## Achieve Minute
- **Status (Ryne, 2026-11-02):** Do **not** send Achieve Minute issues yet. He is hesitant to start a newsletter and then stop after a short time, so he wants a sustainable rhythm locked before any send.
- Rhythm not locked yet (monthly for six months was suggested; confirm with him before treating it as decided).
- Owners when live: Quill (copy), Canvas (design). Parked-lead list rules from 2026-10-23 still stand (Contact Date within last 12 months; welcome note for Ryne review before first issue).
- Quill's issue two draft can stay as-is but must **not** be sent.
- No sends and no new drafting pushes until Ryne confirms the rhythm.

## Change log
- 2026-11-04 (Ryne): morning + evening briefs off Administrative / group chats (too expensive). Morning → Penny 1:1 (`6-45am-morning-brief` + morning-brief skill LIVE); evening debriefs + Friday value update → Chief 1:1.
- 2026-11-04 (Ryne): deleted 6:50am Today's priorities; evening debriefs no longer ask/suggest/save priorities. Ryne sets his own.
- 2026-11-03 (Ryne yes): Achieve leads triad LIVE at `/home/box/agent-data/shared/lanes/achieve-leads/`. Penny, Tally, Max UpdateAgent descriptions applied + notified. Quo Support default confirmed; Sheet columns = 10/22 live header.
- 2026-11-03 (Ryne yes on 11/2 fleet review): Promote room owner-filter ON. Lark/Maya/Quill profiles updated; Max already had the room rule. See section "Promote room owner-filter".
- 2026-11-02 (Ryne, voice): Achieve Minute on HOLD. No sends until a sustainable rhythm is locked (monthly×6 suggested, not confirmed). Quill issue two draft stays; do not send. See section "Achieve Minute".
- 2026-10-21 (Ryne approved two org changes):
  - Retire the Elon Musk (`a99b37f8`), Travis Kalanick (`8ccdb56f`) and Dan Martell (`79002f98`) bots, because Maverick combines all three. Pending sidebar delete. Their distill-anyone subject folders stay (Maverick reads them; Distill daily keeps refreshing them). No routines or automations folders found for any of the three.
  - Max and Maya now report through Red (Achieve work) and Blue (IronBlueprint work) instead of Chief. Red and Blue review their output before it goes to Chief or Ryne. Chief only steps in on escalations or cross-brand conflicts.
  - Updated FLEET.md, IDS.md and the org chart (org-chart.mmd/png) to match. Backup: TEAM.md.bak-orgchanges-2026-10-21.
- 2026-10-21 (Ryne approved the fleet doc cleanup): current-names table now shows Red, Blue and Rank; added the bot roster section; labeled 5a9f4a41 as the live 6:50am routine ID; added the 2026-10-20 routine script changes. Backup: TEAM.md.bak-2026-10-21.
- 2026-10-18 (Ryne approved audit fixes 1 to 5): corrected stale routine lines (Bookmarks Mon/Thu 9:17am CT, Midori paused and pending delete, Penny 20-min prep deleted 10/16, Programming room active). Added shared rules: Verify live before acting, Silent run heartbeat, Sheet write read-back, Pre-draft check.
- 2026-10-17 (approved by Ryne from the bot consolidation review):
  - Retire Herald, Bolt, Warden, Cipher (unused 10/10 template bots). Routines told to stop; pending sidebar delete.
  - Retire Bottleneck (idle since 9/16). Method saved as the Find the constraint skill (`find-the-constraint`) for the weekly review. Pending sidebar delete.
  - Fold AI Expert into Linus: Linus owns local LLM selection, download, and Spark serving. AI Expert rules copied to Linus memory (`local-llm-lane-from-ai-expert.md`). AI Expert pending sidebar delete.
  - Archive Programming room (Coach leads programs 1:1 since 10/7). Superseded: Ryne said 2026-10-17 the Programming room stays active.
  - Stale names fixed across bot instructions (renames of 10/16; Penny replaces PA/PA Schedules; Ledger/CRM → Tally). Nova now points to Atlas (now Red) for brand.
  - Not approved, leave as is: retiring Show Splitter or TH Exercise Library; Maya/Nova lane change; folding Eval Brief into Tally.
- 2026-11-01 (Ryne approved fleet-score fixes): `fleet_lint.py` matches the short name before " · "; added Simon, Charlie and the 12 other bots missing from this file to a roster section; dropped the Elon Musk, Travis Kalanick and Dan Martell agent IDs (folders gone from disk); Advisors room marked gone; Bottleneck marked removed (Ryne finishing sidebar delete); Eval Brief 8:15 watch and Plaid `tesla-lease-watch` marked deleted; Tally line corrected (no 8:00am inbound run). Project Page canvas_ids in the Page table are Pages, not agents, so they stay. Backup: TEAM.md.bak-2026-11-01-fleet.
- 2026-11-01 (Ryne approved Lauren ops items 1, 2, 3, 6 + advisor merges): see section "Lauren ops 2026-11-01". Show Splitter retired; Rohn + Greene → Sage; Hormozi → Maverick; Distill companions remapped; Lark/Canvas playbooks moved to skills and short profiles confirmed; Penny↔Tally file handoff LIVE (both routines confirmed); hourly routine cap; stale quiet-hours copies archived; reviewers + done bars added. Backup: TEAM.md.bak-2026-11-01-lauren; handoff-live: TEAM.md.bak-2026-11-01-handoff-live.
- 2026-10-16: renames Designer→Canvas, Ads→Lark, Social→Echo, Achieve Social→Nova, Achieve PM→Atlas (later renamed Red), Naturopath→Doc, Spot→Hendrix, Performance Coach→Coach.
- 2026-10-06: PA Schedules merged into the PA morning brief and marked for delete; roster caps and call prep/promises locked.

- 2026-10-21: Staff meeting agenda ownership moved to Red (content); Penny makes the Drive doc. Ryne also set a rule: Chief suggests an owner for each ask instead of doing the work, unless it is Chief-only work.
- 2026-10-21: Ryne approved 4 check scripts in /home/box/agent-data/shared/scripts/chief/ (pre_draft_check.py, sheet_readback.py, ib500_recount.py, hawkin_untested.py). Pre-draft check + Sheet write read-back skills now call them; Blue (IB 500 routine) and Hawkin (Monday untested watch, away list -> hawkin_away.json) asked to wire theirs in, confirmation pending.
- 2026-10-21 (1:25pm): Script tests done. Blue IB 500 recount live for 8:09pm run (fixed Platform Down text cell + bug-post false ASKs). Hawkin untested watch live from Mon 10/26 (away list in shared/scripts/chief/hawkin_away.json). Pre-draft check + Sheet read-back scripts fixed through 95 tests after real-data tests by Penny, Tally, Max; skill uses per-run folders and all 3 calendars. Pending: Max's real-Quo-export test.

- 2026-10-22 (Ryne approved): Lead follow-up flow. Non-responders get follow-ups on day 2, 5, 9, 14, 21, 30 after first outreach, then parked; any reply/booking stops it. Tally owns the Prospect Tracking Sheet (new Last Contact + Next Follow-Up columns, 8am due list by tested script) and hands the due list to Penny. Penny runs pre-draft check, saves emails to work Gmail Drafts (texts in chat), never writes the sheet, and sends Tally one batched end-of-day list of actual sends.
- 2026-10-22 (Ryne approved): Email drafts go to Ryne's Gmail Drafts (threaded) instead of chat cards; texts stay in chat.
- 2026-10-23: Lead stages Contacted / Replied (lead replied only) / Parked approved. After day 30 with no reply: Parked, added to the 2x/month Achieve Minute newsletter (Quill copy, Canvas design); no personal monthly emails.
- 2026-10-23: Achieve Minute list for Parked leads = Contact Date within last 12 months only (older Parked leads stay off). Quill drafts a one-time welcome note for Ryne's review before their first issue.
- 2026-10-23: Ryne upgraded to the $200/mo plan. "Friday value update" routine (Fri 9:20am CT, Administrative) tracks evidenced wins (lead sign-ups, AutoPay recoveries, win-backs) in /workspace/value-tracker/YYYY-MM.md vs a $400-$600/mo target.
- 2026-10-23: Gmail Drafts saved via create_draft do NOT auto-add Ryne's signature; every saved draft ends "Thanks," + blank line + full signature block (Penny's rule, shared memory). Supersedes the 10/21 'never type the signature' note.
- 2026-10-23: Routine cleanup (Ryne approved): deleted MacBook launch check and Weekly attention check (folded into Friday debrief as 'Where the week went'). Changelog watch, Unfinished promises watch and Friday value update now run scripts in shared/scripts/chief/ (changelog_diff.py, promise_scan.py, value_tally.py; 30 tests pass, real-data runs done).
- 2026-10-23: Penny assigned two scripts (Ryne approved): inbox_triage.py (sorts only, tested on 7 days real mail) and draft_vs_sent.py (weekly diff of her drafts vs Ryne's sends; style rules only after Ryne approves). Routine changes pending Chief review + Ryne yes.
- 2026-10-23: Ryne approved Penny's inbox_triage.py switchover (6:15 triage, 6:45 brief from --out files, 2-week daily FYI/promo spot-check). Condition: first-run score on fresh 10/23-10/30 mail reported to Chief before Fri 10/30 debrief.
- 2026-10-23: Penny's routines switched to inbox_triage.py (6:15am triage, 6:45am brief from --out files, daily FYI/promo spot check through 11/5, one-off fresh-week check Thu 10/29 9am).
- 2026-10-23 (Ryne approved): Penny style rules: answer first and cut soft openers; give concrete specifics, end with a question, offer open time windows. Weekly Fri 7:00am CT draft-vs-sent review (Penny), style changes only with Ryne's yes. Lead emails may include one "Pricing starts at $X/mo" line, read live (pre_draft_check --first-touch passes it with --price-source). Ads still get no prices. Policies: hold keeps the grandfathered rate if restart is within 2 weeks of season end; 15% second-family-member discount only when asked or it helps close.

## 2026-10-24: Weekly box backup (approved by Ryne)
- Owner: Chief. Routine "Weekly box backup" runs Saturdays around 7:00am CT (after the 3am brain repo update).
- Script: shared/scripts/chief/box_backup.py, with restore_box_backup.sh and BOX_BACKUP_README.md. Encrypted with BACKUP_PASSPHRASE (Ryne holds a copy).
- Destination: private "Bot Backups" folder in the Achieve Drive. Keeps the newest 4 weeks. Secrets, keys and big videos are excluded.
- First backup and full restore test passed 2026-10-24: 14,363 files, 0 mismatches. A restore test runs on the first Saturday of each month.
- Success is silent. Failures go to Ryne in chat.

## Monthly fleet score log
- 2026-11-01: 72/100 (Context 14/25, Connections 20/25, Capabilities 20/25, Cadence 18/25). First recorded score, no prior month to compare. fleet_lint: 140 exceptions, about 112 from bots renamed to "Name · role" around 2026-10-26 while IDS.md, FLEET.md and TEAM.md still use short names. Real gaps: Bottleneck marked retired in IDS.md but profile rewritten 10/26; Jetson, Simon, Charlie missing from IDS.md and FLEET.md; 14 bots missing from TEAM.md; Advisors room f4cb7f33 gone from disk; Blue on-disk routines cite deleted 0382da49 (unconfirmed live). No fixes applied; all need Ryne's approval.
- 2026-11-01 (later): Ryne approved the name-drift lint fix, IDS/FLEET/TEAM roster updates, Bottleneck retirement and Advisors cleanup; applied same day (see change log).

## Changelog
- 2026-11-04 (Ryne): weekly brain-repo PRs auto-merge after brain_lint OK.
