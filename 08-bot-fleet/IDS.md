# Fleet ID reference (IDS.md)

One place for every live ID Ryne Gioviano's Grok Bot fleet needs. Built Saturday 2026-10-17, 10:15 PM CT from the box. Read this before guessing any room, sheet, folder, channel or repo.

**Updated Wednesday 2026-10-21, 8:00 AM CT (Chief, Ryne approved the fleet doc cleanup):** renamed Atlas to Red, the old Forge (IronBlueprint PM) to Blue and SEO / AEO Auditor to Rank, using each bot's current profile.json. Added the new Forge (nutrition), Splice, Plaid and Jim Rohn to the bot table and the HQ room to the room table.

**Updated Wednesday 2026-10-21 (Chief, two org changes Ryne approved):** retired the Elon Musk, Travis Kalanick and Dan Martell bots (Maverick combines all three; pending Ryne's sidebar delete; their distill-anyone subject folders stay). Max and Maya now report through Red (Achieve work) and Blue (IronBlueprint work), not Chief; Chief only steps in on escalations or cross-brand conflicts.

**Updated Sunday 2026-11-01 (Chief, fleet-score fixes Ryne approved):** bot profile names now carry a role suffix ("Penny · admin", about 2026-10-26); the Bot column below uses the short name before " · ", which `fleet_lint.py` now matches. Added Jetson, Simon and Charlie from their profile.json. Bottleneck stays retired; Ryne is finishing the sidebar delete. Elon Musk, Travis Kalanick and Dan Martell folders are gone from disk (checked 2026-11-01). Advisors room (`f4cb7f33`) folder is gone from disk, so its row moved to section 3.

**Updated Thursday 2026-11-05 (full brain sync):** this repo copy now matches the box file of 2026-11-01. New on the box since then: Metric (`247984e5-d450-4fd5-a9d6-f2d2b0902f95`, data and metric deep dives, on demand). Hendrix's profile name is now Spot (`5a0276a8`). No agent folder was found on the box for Charlie (`5217cd51`) on 2026-11-05; that ID is not in deleted-agents.json either (open question). Briefs no longer post in the Administrative room (2026-11-04).

**Name warning:** before 2026-10-19, "Forge" meant the IronBlueprint PM, now named Blue (`cceeaf4d`). Today Forge is Ryne's nutrition coach (`2b406f18`). Older notes and sources cited below may still say Forge for Blue or Atlas for Red.

**Rules for this file**
- No secret values here, ever (API keys, tokens, passwords, webhook secrets). Where a secret matters, this file says where it lives, not what it is.
- On-disk `automations/*.json` files are STALE copies. Do not take room IDs from them. Live routine targets come from the owning bot (for example Blue confirmed his on 2026-10-17).
- When an ID changes, update this file and add a line to the brain repo LOG.md.
- Flags: **CONFLICT** = two sources disagree. **UNCERTAIN** = inferred or not confirmed by the owner. **STALE** = old, do not use.

Paths used below: `A/<id>` = `/home/box/agent-data/agents/<id>`, `W/<skill>` = `/home/box/agent-data/workflows/<skill>/SKILL.md`, `WS/` = `/workspace/`.

## Contents
1. Bots (agent IDs)
2. Group rooms
3. Old and deleted IDs (do not use)
4. Slack (workspaces, channels, users)
5. Google Drive, Sheets, Docs, Calendars
6. Basecamp
7. GitHub repos and pull requests
8. Cursor cloud projects and agents
9. Email inboxes and phone
10. Other IDs (Asana, Notion, Zapier, Meta, X, machines, infra)
11. Conflicts and open questions

---

## 1. Bots (agent IDs)

Source for every row: `A/<id>/profile.json` (name, title) plus `WS/fleet/FLEET.md` (business, reports-to). "Reports to" says "unclear" when no source states it. Chief's own instructions say all bots report to Chief. Exception from 2026-10-21: Max and Maya report through Red and Blue.

### Active bots (41)
| Bot | Agent ID | Title | Business | Reports to | Job (short) |
|---|---|---|---|---|---|
| Chief | `ad6690d7-be33-4540-ac42-68eb3059c181` | chief of staff | Fleet | Ryne | Chief of staff. Routes work to every bot, checks results, sends Ryne one clear update. |
| Linus | `5ec70d9b-e978-4b41-8c2f-f2219c13815a` | engineer | IronBlueprint | Chief; Blue on IB work (Linus instructions 2026-10-17) | Lead engineer. Read-only advisory on IronBlueprint (Suffescom devs do all IB coding); also owns local LLMs... |
| Token Officer | `10242c51-88e8-4583-b81d-61c9525bcc8b` | (none) | Fleet | unclear (proposes directly to Ryne) | Watches fleet token spend, flags waste, and applies routine schedule fixes only after Ryne approves. |
| Dr. Eggbot | `f38722d3-a9d5-4d98-b294-ee15f3361f11` | bot maker | Fleet | unclear | Designs and creates new Grok Bots. |
| Distill anyone | `f9154cb1-6362-4907-85f4-12d50f99279c` | (none) | Fleet | unclear | Builds and refreshes the distilled persona bots (the advisors). |
| Scout | `620dd6ee-1975-442b-be2a-a64a7a88c07b` | research | Fleet | unclear (Red and Blue both coordinate Scout on brand work) | General researcher for anything outside S&C (products, people, tools, business, health, places). |
| Penny | `163cd8df-275e-47c1-a5a2-e10e304a671a` | admin | Personal | Chief (Administrative room) | Personal assistant: email, calendar, Quo, Numa and admin across Ryne's Google accounts. |
| Tally | `5d07e236-9453-409d-ab6c-58711eae2f09` | crm | Achieve | Chief (Administrative room) | Owns Achieve's prospect book (Prospect Tracking sheet): inbound, gap fill, dashboard. |
| Red | `cf4fe585-7bd8-4d68-b32a-67aca0067033` | Achieve | Achieve | Chief (Max and Maya report to Red for Achieve work, 2026-10-21) | Achieve PM. Owns the Achieve brand and coordinates bots on gym work; files Coach's finished programs. |
| Nova | `6b3492d4-c1d7-448a-bed0-38dbb76b7828` | achieve social | Achieve | unclear (brand from Red, strategy briefs from Maya) | Achieve business X and Instagram: owns all Achieve post drafts and captions from Maya's strategy briefs. |
| Eval Brief | `690e65de-c38a-4858-b3cd-831335e62504` | (none) | Achieve | unclear | Turns a newly signed-up client's Drive assessment into a draft Slack #clients coach brief. |
| Coach | `5d64c948-3315-41b3-b9a6-196b4d1e2072` | performance | Achieve | unclear (works 1:1 with Ryne; sends finished programs to Red) | S&C coach. Designs athlete programs one-on-one with Ryne (drafts only). |
| Hawkin | `93d38eed-d001-4265-a229-8527e2efa46f` | force plates | Achieve | unclear | Reads Achieve's Hawkin force plates, analyzes tests and trends, writes plate-driven prescriptions. |
| PRI | `e9d0fc7f-22cc-4b14-80a6-4b8361108e36` | (none) | Achieve | unclear | Postural Restoration Institute specialist for Achieve athletes. |
| Darwin | `d38c0d3f-1a03-4e7e-9ca3-b73ac3057287` | s&c research | Achieve | unclear (reports finds to Ryne; routes to Coach and Hawkin) | S&C research: finds applicable evidence and routes it to Coach and Hawkin. |
| TH Exercise Library | `d5ec05e6-1a00-4136-9f89-90c09a3c6e80` | (none) | Achieve | unclear (on-demand from Ryne or Chief) | Exports Achieve's TrainHeroic exercise library to a Google Sheet on request. |
| Rank | `87fc5650-543f-4643-9dc1-deebc8ef54e8` | SEO/AEO | unclear | unclear | Tracks keyword, technical, AI-prompt and competitor SEO movement (template description). |
| Max | `6404a542-bb7c-48e5-822a-a2afd90ad591` | sales | Achieve + IronBlueprint | Red (Achieve work), Blue (IronBlueprint work); Chief on escalations only (2026-10-21) | Sales lead for Achieve and IronBlueprint, from outreach through expansion. Drafts only. |
| Maya | `c37d4499-a97f-4961-bfcb-9df42e9376a3` | marketing | Achieve + IronBlueprint | Red (Achieve work), Blue (IronBlueprint work); Chief on escalations only (2026-10-21) | Marketing strategy only for both brands; still writes IronBlueprint post drafts. Achieve posts go to Nova. |
| Quill | `aa920346-b0d4-4e99-854d-8d288d0dc1ff` | copywriter | Achieve + IronBlueprint | unclear | Copywriter for Achieve and IronBlueprint. Drafts only. |
| Lark | `bf5d1606-57b1-4b0d-b7f3-c5a52f934a2a` | meta & google ads | Achieve + IronBlueprint | unclear (takes goals from Maya) | Meta Ads and Google Ads platform expert for both brands. |
| Canvas | `567bde28-effb-4c09-bad5-579aa0d6d7ec` | graphic design | Achieve + IronBlueprint | unclear | Graphic designer for Achieve and IronBlueprint (images, PDFs, slides). |
| Blue | `cceeaf4d-4c7b-45fb-b736-9be1fdf15b88` | IronBlueprint | IronBlueprint | Chief (Max and Maya report to Blue for IronBlueprint work, 2026-10-21) | IronBlueprint PM and verifier. Read-only advisory; Suffescom devs do all IB coding. |
| Midori | `0e8c74eb-4d9c-4850-9c37-e831fccf92a2` | bonsai caretaker | Personal | unclear | Caretaker for Ryne's rainbow dwarf jade bonsai; nightly cold alert. |
| NSCA | `30219af9-fdf8-47e6-abd9-e97a0c953950` | recertification | Personal | unclear | Tracks Ryne's NSCA CSCS recertification (cycle ends Dec 31, 2026). |
| Doc | `4fe8ab9a-957c-48ea-8e12-5cff32e2388a` | naturopath | Personal | unclear | Personal naturopathic health advisor (education, not a physician). |
| Hendrix | `5a0276a8-6560-4018-b4ac-b889ca11cbb3` | music expert | Personal | unclear | Music expert (blues, rock, jazz) plus Spotify account management. |
| Justin | `c7a7b01f-ecbe-41aa-8f5e-73e22419f868` | guitar | Personal | unclear | Personal guitar teacher with a progressive plan. On demand only. |
| Bookmarks | `d3bd8f4b-39f7-4316-8135-a9348be70b87` | (none) | Personal | unclear | Files Ryne's X bookmarks into a searchable Notion database. |
| Sage | `99b4a25d-4d82-4a64-b955-4e756140e461` | philosopher | Personal | advisor (no reporting line) | Mentor persona: calm counsel drawn from philosophy. |
| Forge | `2b406f18-aad6-4a09-bfd3-fe56b2b4f37e` | nutrition | Personal | unclear (tells Chief after a self-fix) | Personal nutrition coach: logs meals, estimates macros, coaches toward muscle gain, fat loss and health. Works with Doc. On demand only. Added 2026-10-21. |
| Plaid | `e9e0ed13-6c69-4849-8c61-8046655580e6` | Tesla | Personal | unclear (tells Chief after a self-fix) | Sees the Tesla lease handoff through: return the current lease, then get the new lease accepted and delivered. Read-only Tesla email, tracker, deadline nudges; daily routine about 8:30am CT. Added 2026-10-21. |
| Splice | `78243869-cbf6-458c-bc54-0c2f5761b198` | (none) | Achieve + IronBlueprint + Personal | unclear (returns work to the bot that sent it) | Video editor: turns raw footage into ready-to-post edits (cuts, captions, reformats, branding, audio). Never posts. On demand only. Added 2026-10-21. |
| Maverick | `2772b984-fa9d-4c82-90e4-ea4bc1feae0b` | (none) | Achieve + IronBlueprint | advisor (no reporting line) | Business advisor combining the distilled thinking of Elon Musk, Travis Kalanick and Dan Martell (Musk/Kalanick/Martell lenses). Advice only, no sends. Formerly Boardroom. Created 2026-10-21; not in the Advisors room. Self-fix line added 2026-10-21. Added 2026-10-21. Replaces the retired Elon Musk, Travis Kalanick and Dan Martell bots. |
| Jetson | `1f99ce18-87fe-439a-896b-b4d2c8182bd8` | travel (in name; title field empty) | Personal | unclear (hands booked dates to Penny; tells Chief after a self-fix) | Personal travel planner: flights, stays, event tickets, rental cars, itineraries. Books nothing without Ryne's yes. On demand. Added 2026-11-01. |
| Simon | `48b8dd87-193d-4128-8463-4a6f523dc8fa` | quality assurance (in name; title field empty) | IronBlueprint | Blue ("Blue (IronBlueprint PM) is your lead", profile.json) | Black-box QA for IronBlueprint: tests the live app from outside, pass/fail to Blue, fails also to Linus. Never reads or changes code. Added 2026-11-01. |
| Charlie | `5217cd51-c36e-4f22-83b7-3a2382a7957c` | (none; name has no role suffix) | Achieve (IronBlueprint later, only when Ryne says so) | unclear (tells Chief after a self-fix) | CFO for Achieve: reads QuickBooks Online (read-only) and explains cash, money in, money out and trends. Never writes to QuickBooks or moves money. On demand. Added 2026-11-01. |

### Retired bots (15)
Retired by Ryne's 2026-10-17 approval (TEAM.md change log). Lingxi's lane went to Linus; AI Expert folded into Linus. Elon Musk, Travis Kalanick and Dan Martell retired by Ryne's 2026-10-21 approval; Maverick combines all three.
| Bot | Agent ID | Status | On disk (checked 2026-10-17 10:15 PM CT) | Was |
|---|---|---|---|---|
| Lingxi | `2d09bf74-e02a-4328-9718-b6aba4987c0a` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | Hands-off engineering supervisor. Lane absorbed by Linus 2026-10-17. |
| AI Expert | `51f262cc-37cc-422e-a3ff-b8f61d95a1c8` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | Local LLM picker for the DGX Spark. Lane folded into Linus 2026-10-17. |
| Herald | `2978f1af-afe2-48df-ac8a-480e466dc4cb` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | X product-launch template bot (unused). |
| Bolt | `30467a71-699f-45a6-adb2-8562757bfb0e` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | X API app-building template bot (unused). |
| Warden | `352e16fd-2df6-45de-865b-922f9db74bbb` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | Threat-hunting template bot (unused). |
| Cipher | `43dd7aad-440f-4cf1-b118-2688483617f2` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | Threat-intel template bot (unused). |
| Bottleneck | `c5d9f0a7-0864-407c-9ae2-7aae48909c69` | RETIRED 2026-10-17; REMOVED (Ryne finishing sidebar delete, 2026-11-01) | folder still on disk (checked 2026-11-01); profile renamed "Bottleneck · constraints" ~2026-10-26 | Constraint finder. Idle since 9/16; method saved as the Find the constraint skill. |
| Elon Musk | `a99b37f8-e227-4454-a363-eaf10adbf17a` | RETIRED 2026-10-21 | folder gone from disk (checked 2026-11-01; not in deleted-agents.json) | Distilled persona of Elon Musk (builder). Folded into Maverick. Subject folder `distill-anyone/subjects/elon-musk` stays. |
| Travis Kalanick | `8ccdb56f-3d72-4b95-aa96-6c104fc56d1f` | RETIRED 2026-10-21 | folder gone from disk (checked 2026-11-01; not in deleted-agents.json) | Distilled persona of Travis Kalanick (operator). Folded into Maverick. Subject folder `distill-anyone/subjects/travis-kalanick` stays. |
| Dan Martell | `79002f98-df78-4d4f-80c7-91e62522560e` | RETIRED 2026-10-21 | folder gone from disk (checked 2026-11-01; not in deleted-agents.json) | Distilled persona of Dan Martell (time). Folded into Maverick. Subject folder `distill-anyone/subjects/dan-martell` stays. |
| Echo | `05b8df47-d725-4b70-9e11-f865e7f66612` | RETIRED 2026-11-01 | folder gone from disk, in deleted-agents.json (checked 2026-11-01) | Personal X/IG drafts. |
| Show Splitter | `37c3f952-fedd-4331-a78c-ddd39a32104c` | RETIRED 2026-11-01 (Ryne t773u) | folder gone from disk, in deleted-agents.json (checked 2026-11-01) | Concert MP3 splitter (one-off). |
| Alex Hormozi | `08182d5e-b9ed-43b0-a15d-2ce55ad75312` | RETIRED 2026-11-01, merged into Maverick | folder gone from disk, in deleted-agents.json (checked 2026-11-01) | Distilled persona (sales and marketing). Subject `alex-hormozi` companion → Maverick. |
| Robert Greene | `fb65246d-d183-49b8-ac6d-36abf8ec300e` | RETIRED 2026-11-01, merged into Sage | folder gone from disk, in deleted-agents.json (checked 2026-11-01) | Distilled persona (strategy). Subject `robert-greene` companion → Sage. |
| Jim Rohn | `b85593ea-2b89-4199-ac7f-1d1c3acc4584` | RETIRED 2026-11-01, merged into Sage | folder gone from disk, in deleted-agents.json (checked 2026-11-01) | Distilled persona. Subject `jim-rohn` companion → Sage. |

- **UNCERTAIN:** the six retired bots marked "gone from disk" are not listed in `/home/box/agent-data/deleted-agents.json`, so this file cannot prove they were deleted in the app. Ryne should confirm in the sidebar. Bottleneck is still on disk; Ryne is finishing its sidebar delete (2026-11-01). Elon Musk, Travis Kalanick and Dan Martell (retired 2026-10-21) folders are gone from disk as of 2026-11-01, also not in deleted-agents.json.
- Keep `companion_agent_id` in each retired persona's `distill-anyone/subjects/<slug>/PROFILE.json`. Distill daily only creates a companion bot when that field is empty.
- Agent folders on disk that are not bots or rooms in this table: none.

---

## 2. Group rooms

Source: `A/<room id>/group.json` (members) and `A/<room id>/profile.json`.

| Room | Room ID | Members (from group.json) | Owner bot | Status / notes |
|---|---|---|---|---|
| Administrative | `03ad987e-906d-42bb-98ea-65d016ffc77c` | Tally, Chief, Penny | Chief | LIVE. Shared ops channel for morning briefs (Penny 6:45am, Chief 6:50am priorities). Source: TEAM.md line 4; Tally memory 2026-09-11. |
| IronBlueprint | `8857ae2a-0e5d-4af3-be8a-5ee7f2b04e50` | Blue, Linus | Blue | LIVE. Blue's IB meeting ingest and IB web/mobile tasks post here (Blue, 2026-10-17). **CONFLICT:** FLEET.md lists a 2026-10-17 member plan of Blue, Linus, Scout, Max, Quill, Maya, but group.json has only Blue and Linus. |
| Programming | `7c23ca84-4ef9-4dd7-8421-66e0ab6932ec` | Darwin, PRI, Red, Coach, Hawkin | unclear (Red or Coach) | **ACTIVE per Ryne (2026-10-17).** **CONFLICT:** TEAM.md still has a pending item "Ryne to archive/delete the Programming room" and FLEET.md marks it RETIRED. Ryne's word wins: keep it. |
| Promote | `447d77a8-9873-4b04-821c-87d82cc8c284` | Lark, Maya, Max, Quill | unclear (likely Maya) | LIVE. No description set. |
| Newsletter | `e30bd05f-c397-44ba-bab7-506ea9f73193` | Quill, Maya, Canvas, Red | unclear (likely Quill or Maya) | LIVE. No description set. |
| HQ | `10dece0d-b4a4-4ab7-b0f7-3fe8ad7b6765` | Red, Blue | unclear | LIVE per group.json (created 2026-10-20). No description set. Added 2026-10-21. |

---

## 3. Old and deleted IDs (do not use)

| ID | What it was | Source | Status |
|---|---|---|---|
| `0382da49-74aa-4f07-9175-22c6e94e2887` | Old IronBlueprint room | `/home/box/agent-data/deleted-agents.json`; FLEET.md line 1447 | **DELETED.** Only appears in stale automation copies. Blue confirmed 2026-10-17 none of his 6 live routines use it. |
| `f4cb7f33-0203-4bc5-a803-b5d8f4483365` | Advisors room (was Travis Kalanick, Elon Musk, Alex Hormozi, Dan Martell) | IDS.md room table until 2026-11-01 | **GONE from disk (checked 2026-11-01).** Not in deleted-agents.json, so the app delete is unconfirmed. Do not route to it. |
| `88465cbe-9e98-4275-8ff3-e07be473ebc1` | PA Schedules (merged into Penny) | deleted-agents.json; TEAM.md | DELETED. |
| `a9da8358-76ff-4221-bf2d-19d9548ed9bd` | Old Personal Assistant (replaced by Penny) | TEAM.md line 41; source-map.json | GONE. Do not @. |
| `8b769a17-b0a6-4194-9442-a47551294a2b` | An older Personal Assistant | Tally memory profile.md line 8 (2026-08-28) | **STALE in Tally's memory.** Tally should ping Penny `163cd8df-275e-47c1-a5a2-e10e304a671a` instead. |
| `015eae3a-8b98-45d2-a1b4-ec7679ac8b04` | Old Administrative room | Tally memory profile.md line 28 | RETIRED 2026-09-11. |
| `0c56f311-56b5-4ded-ae36-22f03da7a160` | Old "fat" Strength Coach agent | `A/5d64c948.../memory/reference/README.txt`; 36 skills in `/home/box/agent-data/workflows` | **GONE from disk, but 36 skills still point to its `memory/reference/` files** (exercise progressions CSV, tapering guide, program design basics, several PRI manuals). See section 11. |
| `8737cb6d-...`, `fa023a50-...`, `26543bbf-...`, `3b44cc52-...`, `b6f91743-...`, `c5f3a11f-...`, `d61cf18e-...` | Deleted agents (names not recorded) | deleted-agents.json | DELETED. Names unknown. |
| Chief automation folders `quiet-hours-start`, `quiet-hours-end`, `5-35am-today-s-priorities` | Old Chief routines | `A/ad6690d7.../automations/` | STALE copies. Quiet hours were deleted 2026-09-20; priorities now run at 6:50am (TEAM.md). |

---

## 4. Slack

### Workspaces
| Workspace | Domain | Connector | Notes |
|---|---|---|---|
| Achieve | achievept.slack.com | `user-Slack--achieve` | Ryne is not the workspace owner (Blue memory 2026-08-20; may refer to either workspace, UNCERTAIN). |
| IronBlueprint | ironblueprint.slack.com | `user-Slack--ironblueprint` | Messages to Suffescom go from Ryne's IB Slack, as drafts he approves. |

### Channels
| Channel | ID | Workspace | Used by (owner bot) | Source | Notes |
|---|---|---|---|---|---|
| #ironblueprint | `C09LEBCE40P` | Achieve | Blue (IB 500 daily pace post, IB 500 tally) | Blue 2026-10-17 message; `WS/ib-500-tally-log.md` | LIVE. Not the same as IB Slack #iron-blueprint below. |
| #programming | `C01KHUGT623` | Achieve | Hawkin (SJ/CMJ reports, weekly trends) | `A/93d38eed.../memory/profile.md` lines 11, 14 | LIVE. |
| #clients | `C1J8VTFU4` | Achieve (UNCERTAIN, inferred from Achieve client use) | Eval Brief (weekday 8:15am draft pass) | `A/690e65de.../profile.json`; TEAM.md line 92 | LIVE. Draft-first. |
| #bugs | `C0C8V38T082` | IronBlueprint | Blue (IB Slack bug watcher), Linus (triage) | `WS/ironblueprint-agent-prep/bug-triage-state.json`; `WS/thc/Forge.txt` (file named under the old name) | LIVE. |
| #web-app | `C06Q30B0UUA` | IronBlueprint | Blue (bug watcher) | `WS/thc/Forge.txt` (file still uses the old name; bug card "Source: IronBlueprint Slack #web-app") | LIVE. Name matched from one bug card. |
| #nexus-ai | `C06Q5DUACKE` | IronBlueprint | Blue (bug watcher) | `WS/agent-tools/*.txt` Basecamp card permalinks | **UNCERTAIN:** name inferred from nearby "#nexus-ai" mentions, not confirmed. |
| #mobile-app | not found | IronBlueprint | Blue (bug watcher) | Blue 2026-10-17 message (name only) | **MISSING ID.** Ask Blue. |
| #iron-blueprint | `C06LPV4C6P3` | IronBlueprint | Blue (Suffescom messages, as drafts) | `WS/agent-tools/b75a4930-....txt` (Chief brief to Blue) | LIVE. Easy to confuse with Achieve #ironblueprint. |

### Slack user IDs (Achieve workspace, for IB 500 tally)
Source: `WS/ib-500-tally-log.md`. Owner: Blue.
| Person | User ID |
|---|---|
| Ryne | `U0HPMS8MU` |
| Scott | `U0AJXGFCMR6` |
| Nick | `U62EKBP1Q` |
| Blake | `U09AYPV9F3Q` |

---

## 5. Google Drive, Sheets, Docs, Calendars

| What | ID | Account | Owner bot | Source | Notes |
|---|---|---|---|---|---|
| Prospect Tracking (Achieve CRM sheet) | `1x8KurT1AJOPYLca6Jz9f_zBqZ3yBUGv8-isf8pctv4g` | ryne@achievesportsperformance.com | Tally (writes); Eval Brief (reads Sign-Up) | Tally memory line 6; Tally and Eval Brief profile.json; `W/achieve-prospect-tracking` | LIVE. |
| Prospect Tracking, 2026 tab | worksheet `502533256` | same | Tally | Tally memory line 7; Tally profile.json | LIVE. New rows go at the top. |
| SCDD Instant Form leads sheet | `1mASw_Y5-jRy6ccBSnLdQQAfA33IYGZjkrw0lOj8Q1HE` | same | Tally | Tally memory line 6 | Form watch RETIRED 2026-09-15; existing rows still get gap-fill. |
| Clients folder (eval Assessments) | `1o_k6aDUbkWcSJGYXwYbmI9wF-Hi78VAF` | Achieve Drive | Eval Brief | Eval Brief profile.json; TEAM.md line 90 | LIVE. |
| NTA / Jeremy Meserole Gemini meeting notes folder | `1RoZsVphbmcbv3RO6ds-BDokuqbDQFc0P` | Achieve Drive | Red | Red memory lines 28, 30 | LIVE. |
| Achieve TrainHeroic Exercise Library sheet | `1UnQjlyH_wbVGWDIHTU0BbXJlcNwkarQF9nTECDaQuW8` | Achieve Drive | TH Exercise Library | TH Exercise Library memory line 8 | LIVE. |
| Achieve TrainHeroic Exercise Progressions sheet | `1Sjn2AxfGor3jwkCybvtrf12lC5E0zZttY6ztLladk38` | Achieve Drive | TH Exercise Library | TH Exercise Library memory line 10 | LIVE. |
| IronBlueprint Stock Exercise Progressions sheet | `1kveJElUB335NQ_7zGqPbElJhxkmo2boJdH20R7qge1g` | IB Drive | TH Exercise Library (read-only template) | TH Exercise Library memory line 9 | READ-ONLY. Never edit. |
| IronBlueprint 500 Program Feedback Tracker | `1nGFHBgUfoDInpSnwfBTGBa5y-cG9eFCfWv5zniAax5E` | ryne@ironblueprint.app | Blue (IB 500 tally) | `WS/thc/Forge.txt` (file named under the old name) | LIVE. Blue's tally routine writes here. |
| IB "Web & Mobile Tasks" sheet (Suffescom-owned) | not pinned on purpose | IB Drive (owned by Suffescom / Gaurav) | Blue (weekday 9:00am check) | Blue automation prompt | The routine searches by title each run and must not trust a stale file ID. |
| Google Doc "Reviews" (Achieve Google reviews) | `1TBqWHIV0rm1mhvE-nKgepOwfc3005Bd02Q7f9rx6Hfg` | Achieve Drive | unclear (Maya / Max) | `WS/achieve-review-mining.md` | UNCERTAIN owner. |
| IB Athlete Design Guidelines (ADG) doc | `1MpY-3Js6F1_k0w57sNpfwfxQTcJtLn2vuclolg7n0oM` | IB Drive | Blue | `WS/ib-doc-conflicts.md` | Reference doc. |
| IB "V&I" doc | `1l3wefb5HybCGVWcmdoVY_SmmreIUxQRQk3o98slb5cU` | IB Drive | Blue | `WS/ib-doc-conflicts.md` | Reference doc. Full title not recorded. |
| Staff Meeting 2026-06-01 notes | `1b4trwYNmUx_XBUNTnrKxmLBlKT8cUclsXxBUnmf1OoI` | Achieve Drive | Penny (Staff Meeting template owner) | `WS/nta-jeremy-brief.md` (Drive doc index) | UNCERTAIN whether this is the template or one meeting's notes. |
| NTA Contract (unsigned template) | `1-A99TRyc6fekjPON_Kq4lBLY6hebPUGugCyPRraEUTk` | Achieve Drive | Red | `WS/nta-jeremy-brief.md` (Drive doc index) | Reference. |
| NTA meeting notes (9 docs, 2025-07-31 to 2026-05-08) | see the Drive doc index table in `WS/nta-jeremy-brief.md` | Achieve Drive | Red | same | Reference. Not repeated here. |
| Achieve Mindbody calendar | `c_fef09087722dbbc1c9f8fbd060f8fedd345c3837388c858758268befb6126ca4@group.calendar.google.com` | Google Calendar | Penny (morning brief) | `W/morning-brief` line 28 | LIVE. |
| IronBlueprint calendar | calendarId `ryne@ironblueprint.app` | Google Calendar (IB) | Penny (morning brief) | `W/morning-brief` line 29 | LIVE. Missing from `list_calendars`, so call it by ID. |

---

## 6. Basecamp

Account and projects: Blue memory profile.md line 13; Blue profile.json; `W/morning-brief`. Owner: Blue (reads only). Linus may note items on the engineering boards. Bots never create, comment, complete or post unless Ryne names the item.

| What | ID | Notes |
|---|---|---|
| Account "IronBlueprint" | `6223040` | Basecamp CLI at `/home/box/.local/bin/basecamp` is signed in. |
| Project: Development | `47608498` | Engineering. Holds the two card tables below. |
| Project: Growth & Ops | `47842785` | Launch to-do lists. |
| Project: Beta Program | `47865981` | Beta. |
| Card table: Bugs | `10037160132` | Columns: Triage `10037160134`, Not now `10037160137`, Ready `10037160139`, In Progress `10037160140`, QA `10037163078`, Done `10037160142`. Source: `WS/agent-tools/*.txt` Basecamp API reads. |
| Card table: Improvements | `9970180966` | Columns: Triage `9970180967`, Not now `9970180968`, Ready `10018277331`, In Progress `10018277393`, QA `10018277478`, Done `9970180971`. **CONFLICT:** Linus's instructions and FLEET.md say "Bugs and Code Changes card tables". The API title is "Improvements". Probably the same board renamed, UNCERTAIN. |

---

## 7. GitHub repos and pull requests

### Brain repos (private, Ryne's personal account, created by Ryne 2026-10-17)
| Repo | Open PR | Branch | Cloud agent that pushed it | Notes |
|---|---|---|---|---|
| `rgioviano/Achieve` | https://github.com/rgioviano/Achieve/pull/1 | `brain-v1` | `bc-29bf588a-1589-54eb-b79e-e44c0e923aa2` | 178 files, latest commit c035c68. Open, not merged. |
| `rgioviano/IronBlueprint` | https://github.com/rgioviano/IronBlueprint/pull/1 | `brain-v1` | `bc-370afbcf-8755-5c05-b76a-e9177c402a95` | 68 files, commit 0d0c133. Open, not merged. |
| `rgioviano/Personal` | https://github.com/rgioviano/Personal/pull/1 | `brain-v1` | `bc-ecaf0708-b2a5-5aa2-a3a1-...` | 92 files. Open, not merged. **UNCERTAIN:** full cloud agent ID was cut off in Chief's notes. |

Source: Chief chat summary 2026-10-17. The box has no GitHub login; pushes go through Cursor cloud agents. The `cursor-github` connector is read-only for files.

### IronBlueprint code repos (Suffescom writes; Linus and Blue read only)
Source: `WS/ironblueprint-agent-prep/repo-map.md` (read-only audit 2026-10-17). Owner: Linus (review), Blue (PM).
| Repo | Live branch | Status |
|---|---|---|
| `IronBluePrint/frontend-website` | `main` (`staging` is ahead) | ACTIVE, core. Next.js coach and admin web app. Linus reviews PRs. |
| `IronBluePrint/nodejs-backend` | `master` | ACTIVE, core. Express and Mongo API. Linus reviews PRs. |
| `IronBluePrint/nexus-ai-agent` | `AIdevelopment` (inferred) | ACTIVE, core. FastAPI and LangGraph program generator. Linus reviews PRs. UNCERTAIN live branch. |
| `IronBluePrint/ironblueprint-nexus-ai-agent` | `developer-new` | STALE prototype. |
| `IronBluePrint/landing-website` | `main` | STALE. |
| `IronBluePrint/python-ai-backend` | `master` | STALE prototype. |
| `IronBluePrint/rn-mobile-apps` | none | EMPTY placeholder. |
| `Iron-Blueprint/IronBlueprint-Mobile-App` | unknown | **NOT ACCESSIBLE.** Real React Native athlete app, in a second org spelled `Iron-Blueprint` (with a hyphen). Cursor GitHub app not installed there. |

Note: the code org is spelled `IronBluePrint` (capital P) and the mobile org `Iron-Blueprint`. The brain repo is `rgioviano/IronBlueprint`. Do not mix them up.

---

## 8. Cursor cloud projects and agents

Source: `WS/cloud-agent-transcripts/` (first prompt of each) and bot instructions. All owned by Ryne's Cursor account.
| Project | Cloud agent ID | Owner bot | Notes |
|---|---|---|---|
| S&C Research Corpus | `bc-717fb255-6a8b-5628-bfb0-c562b82be24c` | Darwin | Named in Darwin's instructions. |
| SEO AEO Auditor Data | `bc-2714e58d-28d0-57ae-9361-c731932df50e` | Rank | |
| Ads Performance Data | `bc-d90d9738-ac10-52df-8d72-4443fdbb0386` | Lark | |
| Achieve Programming Data warehouse | `bc-354df073-adf9-554e-aa92-46cfa180c48d` | Programming room (Coach, Red) | |
| PRI Reference Corpus | `bc-e18f0ad0-1214-5a89-af2f-ff4fb4273a76` | PRI | Parent project. |
| PRI fast chat | `bc-dc8e89e3-1038-5726-997f-ca2dd9ab6d4f` | PRI | Chat on the PRI corpus. |
| Hawkin Dynamics | `bc-8e4b0d56-a64c-43cb-a78f-1d25e9038734` | Hawkin | Project. |
| Hawkin fast chats | `bc-66093db2-dcbc-50ba-89ae-d0b6fe6ccd67`, `bc-8f0802fb-bee2-5499-9dce-5e588fc2e6a5`, `bc-cb91bea7-7328-503b-b7d2-464486b8d2e1` | Hawkin | UNCERTAIN which one is current. |
| SCDD Meta landing page (one-off) | `bc-fc73599f-1b94-4137-bff5-378ec601f825` | Maya / Lark | One-off build. |
| Lead magnet PDF (one-off) | `bc-22425308-a842-570e-8896-9dc92cc0c009` | Maya | One-off build. |
| Safari/Brave bookmark sync (one-off) | `bc-8264c14e-03e6-543c-995e-8a8e4ec01fe5` | personal | One-off build. |

Note: Linus's old instructions said he hands repo work to Cursor cloud agents. As of 2026-10-17 he is read-only and must not launch coding agents.

---

## 9. Email inboxes and phone

| Address | What | Connector | Who uses it | Source |
|---|---|---|---|---|
| ryne@achievesportsperformance.com | Achieve work (primary) | `user-Gmail--work` | Penny, Tally, Max, Red | `W/achieve-mail`; Blue memory line 15 |
| contact@achieve-personaltraining.com | Achieve contact inbox (also the public CTA address) | `user-Gmail--contact` | Penny, Tally | `W/achieve-mail` |
| ryne@ironblueprint.app | IronBlueprint (Google account, calendar, Drive) | `user-Gmail--ironblueprint` | Blue, Penny | `W/achieve-mail`; Blue memory |
| ryne@iron-blueprint.com | Second IronBlueprint address | not mapped to a connector | Blue, Quill, Maya (copy context) | Scout, Quill, Maya memory; Blue profile.json |
| [address kept out of repo] | Personal | `user-Gmail--personal` | Penny, NSCA | `W/achieve-mail`; NSCA profile.json |
| [address kept out of repo] | Grok Bot's own inbox (receive and read; parent agent sends) | Grok Bot inbox | Chief | ListEmailInboxes 2026-10-17 |
| [address kept out of repo] | Staff (BCC on account changes) | n/a | Penny | `W/achieve-writing-style` |
| Achieve business text line 630.340.4114 | Public business number in signatures | Quo (Numa until cutover) | Penny | `W/achieve-mail`; Nova profile.json |

- **UNCERTAIN:** `user-Gmail` (no suffix) is also connected; which account it is was not checked.
- Quo inbox IDs were not found in any file. Penny should record them here when known.

---

## 10. Other IDs

| What | ID | Owner bot | Source | Notes |
|---|---|---|---|---|
| Asana workspace | `107643935803640` | Penny | Chief voice-call log | **CONFLICT:** TEAM.md says "drop Asana for good (connector never works)" for briefs, but the October marketing plan was loaded into Asana as daily tasks. |
| Asana project: Marketing | `156534408810902` | Penny / Maya | same | 78 October lead tasks loaded. |
| Notion database "X Bookmarks" | `260278794ab24f0f9f21c95a0d7fcb2d` (data source `1c3a4778-abaa-4081-b393-7e7e86f34856`) | Bookmarks | `/home/box/agent-data/x-bookmarks/state.json` | LIVE. |
| Ryne's X user ID | `25647800` | Bookmarks, Echo | same | |
| Meta page "Achieve Sports Performance" | `447963512069200` | Tally, Lark | Tally memory line 10 | |
| Meta Instant Form "Short Course Dryland Domination" | `1344866124503462` (also "...Domination 1" `4743940052492281`) | Tally | Tally memory line 10 | SCDD watch retired 2026-09-15. |
| Zapier connection: Facebook Lead Ads (default) | `02230b00-c593-8d7a-a74a-2b16dcfc617b` | Tally | Tally memory line 14 | Connection identifier, not a credential. Legacy `0250132f-af02-8772-a4cf-9cc454906fda` is STALE. |
| Zapier connection: Google Sheets (ryne@achievesportsperformance.com) | `02ca3905-95d2-80e0-b57c-e02585a27d1c` | Tally | Tally memory line 14 | Used for Prospect Tracking writes. |
| Ryne's Mac (registered machine) | `7d3c49a4-3b83-48f1-a860-c3821e2c2fff` | Linus (Passport drive staging) | Linus memory `local-llm-lane-from-ai-expert.md` | |
| Firebase project (IB web push) | `ironblueprint-faff9` | Blue / Linus | repo-map.md | Ryne-owned. |
| Firebase project used by backend push | `suffescom-mobiles` | Blue / Linus | repo-map.md; Ryne 2026-10-17 | **FLAG:** created by Suffescom, not Ryne. Ryne says he owns all accounts; this one needs an ownership check. |
| Nexus API host (prod) | `nexus-api.iron-blueprint.com` | Linus | repo-map.md | Host only. Secrets live in AWS SSM, never here. |
| USPTO serials | `99550047` (IRON BLUEPRINT, Ryne individually), `99383569` (IRONBLUEPRINT, Iron Blueprint LLC) | Blue | Blue memory line 7; IB decisions log | 99550047 examination suspended 2026-10-07. |
| Chief routine folders | `5a9f4a41-dbcf-5bdb-bcdf-f3cf132a4689` (6:50am priorities), `weeknight-evening-debrief`, `friday-evening-debrief`, `unfinished-promises-watch`, `weekly-brain-repo-update` | Chief | TEAM.md lines 46-49; Chief chat 2026-10-17 | Live routine IDs, not the stale on-disk copies. |
| Hawkin Dynamics integration key | location only: Hawkin bot and Red `secrets/` folders | Hawkin | Red memory line 42 | Secret. Value never copied anywhere. |

---

## 11. Conflicts and open questions

1. **36 skills point to a deleted agent.** Skills such as `exercise-progressions-and-selections`, every `*-progressions` ladder, `guide-to-tapering`, `program-design-basics`, `athlete-program-design-guidelines`, `adult-program-design-guidelines`, `isometrics-programming-guide`, `frc-progressions-and-prescriptions` and several `pri-*` skills cite `/home/box/agent-data/agents/0c56f311-.../memory/reference/...`. That folder is gone. The PRI manuals survive under PRI (`A/e9d0fc7f.../memory/reference/`), and `program-design-basics.txt` survives at `WS/uploads/`. The exercise progressions CSV and the tapering guide were not found anywhere on disk; the Achieve Programming Data Cursor project may hold copies. Highest priority fix.
2. **Programming room:** active per Ryne, but TEAM.md (pending archive) and FLEET.md (RETIRED) disagree. Update both.
3. **IronBlueprint room members:** on disk only Blue and Linus. FLEET.md's 2026-10-17 list adds Scout, Max, Quill, Maya.
4. **Retired bots:** six are gone from disk but not in deleted-agents.json. Confirm in the sidebar. Bottleneck, Elon Musk, Travis Kalanick and Dan Martell still need a sidebar delete. TEAM.md's pending list leaves out Lingxi.
5. **Tally memory has two stale IDs:** old Personal Assistant `8b769a17-...` (line 8) and a room description that still names CRM Watch and PA Schedules (line 28).
6. **Basecamp board name:** "Code Changes" (Linus instructions, FLEET.md) vs "Improvements" (Basecamp API).
7. **Slack names that look alike:** Achieve `#ironblueprint` `C09LEBCE40P` vs IronBlueprint `#iron-blueprint` `C06LPV4C6P3`.
8. **Missing IDs:** IB Slack `#mobile-app`, Quo inboxes, full Personal PR cloud agent ID, which account `user-Gmail` is.
9. **Asana:** "never Asana" in briefs vs the October marketing plan living in Asana.
10. **Midori's forecast location** is Aurora, IL (the gym is in Aurora). Ads now target Naperville (Ryne 2026-10-17). Both are correct for their own jobs; noted so nobody "fixes" one to match the other.

Sources: listed per row. Scan covered `A/*/profile.json`, `A/*/group.json`, `A/*/memory/*.md`, `/home/box/agent-data/workflows/*/SKILL.md`, `/home/box/agent-data/deleted-agents.json`, Chief TEAM.md, `WS/fleet/FLEET.md`, `WS/*.md`, `WS/ironblueprint-agent-prep/`, `WS/cloud-agent-transcripts/`, `WS/agent-tools/`. Secrets folders, connector secrets and `.env` files were not read.
