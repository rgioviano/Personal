# Fleet ID reference (IDS.md)

One place for every live ID Ryne Gioviano's Grok Bot fleet needs. Built Saturday 2026-10-17, 10:15 PM CT from the box. Read this before guessing any room, sheet, folder, channel or repo.

**Rules for this file**
- No secret values here, ever (API keys, tokens, passwords, webhook secrets). Where a secret matters, this file says where it lives, not what it is.
- On-disk `automations/*.json` files are STALE copies. Do not take room IDs from them. Live routine targets come from the owning bot (for example Forge confirmed his on 2026-10-17).
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

Source for every row: `A/<id>/profile.json` (name, title) plus `WS/fleet/FLEET.md` (business, reports-to). "Reports to" says "unclear" when no source states it. Chief's own instructions say all bots report to Chief.

### Active bots (37)
| Bot | Agent ID | Title | Business | Reports to | Job (short) |
|---|---|---|---|---|---|
| Chief | `ad6690d7-be33-4540-ac42-68eb3059c181` | chief of staff | Fleet | Ryne | Chief of staff. Routes work to every bot, checks results, sends Ryne one clear update. |
| Linus | `5ec70d9b-e978-4b41-8c2f-f2219c13815a` | engineer | IronBlueprint | Chief; Forge on IB work (Linus instructions 2026-10-17) | Lead engineer. Read-only advisory on IronBlueprint (Suffescom devs do all IB coding); also owns local LLMs... |
| Token Officer | `10242c51-88e8-4583-b81d-61c9525bcc8b` | (none) | Fleet | unclear (proposes directly to Ryne) | Watches fleet token spend, flags waste, and applies routine schedule fixes only after Ryne approves. |
| Dr. Eggbot | `f38722d3-a9d5-4d98-b294-ee15f3361f11` | bot maker | Fleet | unclear | Designs and creates new Grok Bots. |
| Distill anyone | `f9154cb1-6362-4907-85f4-12d50f99279c` | (none) | Fleet | unclear | Builds and refreshes the distilled persona bots (the advisors). |
| Scout | `620dd6ee-1975-442b-be2a-a64a7a88c07b` | research | Fleet | unclear (Atlas and Forge both coordinate Scout on brand work) | General researcher for anything outside S&C (products, people, tools, business, health, places). |
| Penny | `163cd8df-275e-47c1-a5a2-e10e304a671a` | admin | Personal | Chief (Administrative room) | Personal assistant: email, calendar, Quo, Numa and admin across Ryne's Google accounts. |
| Tally | `5d07e236-9453-409d-ab6c-58711eae2f09` | crm | Achieve | Chief (Administrative room) | Owns Achieve's prospect book (Prospect Tracking sheet): inbound, gap fill, dashboard. |
| Atlas | `cf4fe585-7bd8-4d68-b32a-67aca0067033` | Achieve | Achieve | Chief | Achieve PM. Owns the Achieve brand and coordinates bots on gym work; files Coach's finished programs. |
| Nova | `6b3492d4-c1d7-448a-bed0-38dbb76b7828` | achieve social | Achieve | unclear (brand from Atlas, strategy briefs from Maya) | Achieve business X and Instagram: owns all Achieve post drafts and captions from Maya's strategy briefs. |
| Eval Brief | `690e65de-c38a-4858-b3cd-831335e62504` | (none) | Achieve | unclear | Turns a newly signed-up client's Drive assessment into a draft Slack #clients coach brief. |
| Coach | `5d64c948-3315-41b3-b9a6-196b4d1e2072` | performance | Achieve | unclear (works 1:1 with Ryne; sends finished programs to Atlas) | S&C coach. Designs athlete programs one-on-one with Ryne (drafts only). |
| Hawkin | `93d38eed-d001-4265-a229-8527e2efa46f` | force plates | Achieve | unclear | Reads Achieve's Hawkin force plates, analyzes tests and trends, writes plate-driven prescriptions. |
| PRI | `e9d0fc7f-22cc-4b14-80a6-4b8361108e36` | (none) | Achieve | unclear | Postural Restoration Institute specialist for Achieve athletes. |
| Darwin | `d38c0d3f-1a03-4e7e-9ca3-b73ac3057287` | s&c research | Achieve | unclear (reports finds to Ryne; routes to Coach and Hawkin) | S&C research: finds applicable evidence and routes it to Coach and Hawkin. |
| TH Exercise Library | `d5ec05e6-1a00-4136-9f89-90c09a3c6e80` | (none) | Achieve | unclear (on-demand from Ryne or Chief) | Exports Achieve's TrainHeroic exercise library to a Google Sheet on request. |
| SEO / AEO Auditor | `87fc5650-543f-4643-9dc1-deebc8ef54e8` | (none) | unclear | unclear | Tracks keyword, technical, AI-prompt and competitor SEO movement (template description). |
| Max | `6404a542-bb7c-48e5-822a-a2afd90ad591` | sales | Achieve + IronBlueprint | Chief (stated); Atlas and Forge coordinate on brand work | Sales lead for Achieve and IronBlueprint, from outreach through expansion. Drafts only. |
| Maya | `c37d4499-a97f-4961-bfcb-9df42e9376a3` | marketing | Achieve + IronBlueprint | Chief (stated); Atlas and Forge coordinate on brand work | Marketing strategy only for both brands; still writes IronBlueprint post drafts. Achieve posts go to Nova. |
| Quill | `aa920346-b0d4-4e99-854d-8d288d0dc1ff` | copywriter | Achieve + IronBlueprint | unclear | Copywriter for Achieve and IronBlueprint. Drafts only. |
| Lark | `bf5d1606-57b1-4b0d-b7f3-c5a52f934a2a` | meta & google ads | Achieve + IronBlueprint | unclear (takes goals from Maya) | Meta Ads and Google Ads platform expert for both brands. |
| Canvas | `567bde28-effb-4c09-bad5-579aa0d6d7ec` | graphic design | Achieve + IronBlueprint | unclear | Graphic designer for Achieve and IronBlueprint (images, PDFs, slides). |
| Forge | `cceeaf4d-4c7b-45fb-b736-9be1fdf15b88` | IronBlueprint | IronBlueprint | Chief | IronBlueprint PM and verifier. Read-only advisory; Suffescom devs do all IB coding. |
| Echo | `05b8df47-d725-4b70-9e11-f865e7f66612` | personal social | Personal | unclear | Ryne's personal X and Instagram posting partner. Drafts only. |
| Midori | `0e8c74eb-4d9c-4850-9c37-e831fccf92a2` | bonsai caretaker | Personal | unclear | Caretaker for Ryne's rainbow dwarf jade bonsai; nightly cold alert. |
| NSCA | `30219af9-fdf8-47e6-abd9-e97a0c953950` | recertification | Personal | unclear | Tracks Ryne's NSCA CSCS recertification (cycle ends Dec 31, 2026). |
| Doc | `4fe8ab9a-957c-48ea-8e12-5cff32e2388a` | naturopath | Personal | unclear | Personal naturopathic health advisor (education, not a physician). |
| Hendrix | `5a0276a8-6560-4018-b4ac-b889ca11cbb3` | music expert | Personal | unclear | Music expert (blues, rock, jazz) plus Spotify account management. |
| Justin | `c7a7b01f-ecbe-41aa-8f5e-73e22419f868` | guitar | Personal | unclear | Personal guitar teacher with a progressive plan. On demand only. |
| Bookmarks | `d3bd8f4b-39f7-4316-8135-a9348be70b87` | (none) | Personal | unclear | Files Ryne's X bookmarks into a searchable Notion database. |
| Show Splitter | `37c3f952-fedd-4331-a78c-ddd39a32104c` | (none) | Personal | unclear | Splits a concert MP3 into per-song files. Disposable, delete after the job. |
| Sage | `99b4a25d-4d82-4a64-b955-4e756140e461` | philosopher | Personal | advisor (no reporting line) | Mentor persona: calm counsel drawn from philosophy. |
| Alex Hormozi | `08182d5e-b9ed-43b0-a15d-2ce55ad75312` | sales & marketing | Personal | advisor (no reporting line) | Distilled persona of Alex Hormozi (sales and marketing). |
| Dan Martell | `79002f98-df78-4d4f-80c7-91e62522560e` | time | Personal | advisor (no reporting line) | Distilled persona of Dan Martell (time). |
| Travis Kalanick | `8ccdb56f-3d72-4b95-aa96-6c104fc56d1f` | operator | Personal | advisor (no reporting line) | Distilled persona of Travis Kalanick (operator). |
| Elon Musk | `a99b37f8-e227-4454-a363-eaf10adbf17a` | builder | Personal | advisor (no reporting line) | Distilled persona of Elon Musk (builder). |
| Robert Greene | `fb65246d-d183-49b8-ac6d-36abf8ec300e` | strategy | Personal | advisor (no reporting line) | Distilled persona of Robert Greene (strategy). |

### Retired bots (7)
Retired by Ryne's 2026-10-17 approval (TEAM.md change log). Lingxi's lane went to Linus; AI Expert folded into Linus.
| Bot | Agent ID | Status | On disk (checked 2026-10-17 10:15 PM CT) | Was |
|---|---|---|---|---|
| Lingxi | `2d09bf74-e02a-4328-9718-b6aba4987c0a` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | Hands-off engineering supervisor. Lane absorbed by Linus 2026-10-17. |
| AI Expert | `51f262cc-37cc-422e-a3ff-b8f61d95a1c8` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | Local LLM picker for the DGX Spark. Lane folded into Linus 2026-10-17. |
| Herald | `2978f1af-afe2-48df-ac8a-480e466dc4cb` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | X product-launch template bot (unused). |
| Bolt | `30467a71-699f-45a6-adb2-8562757bfb0e` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | X API app-building template bot (unused). |
| Warden | `352e16fd-2df6-45de-865b-922f9db74bbb` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | Threat-hunting template bot (unused). |
| Cipher | `43dd7aad-440f-4cf1-b118-2688483617f2` | RETIRED 2026-10-17 | folder gone from disk (looks deleted) | Threat-intel template bot (unused). |
| Bottleneck | `c5d9f0a7-0864-407c-9ae2-7aae48909c69` | RETIRED 2026-10-17 | folder still on disk | Constraint finder. Idle since 9/16; method saved as the Find the constraint skill. |

- **UNCERTAIN:** the six retired bots marked "gone from disk" are not listed in `/home/box/agent-data/deleted-agents.json`, so this file cannot prove they were deleted in the app. Ryne should confirm in the sidebar. Bottleneck is still on disk and waiting for a sidebar delete.
- Agent folders on disk that are not bots or rooms in this table: none.

---

## 2. Group rooms

Source: `A/<room id>/group.json` (members) and `A/<room id>/profile.json`.

| Room | Room ID | Members (from group.json) | Owner bot | Status / notes |
|---|---|---|---|---|
| Administrative | `03ad987e-906d-42bb-98ea-65d016ffc77c` | Tally, Chief, Penny | Chief | LIVE. Shared ops channel for morning briefs (Penny 6:45am, Chief 6:50am priorities). Source: TEAM.md line 4; Tally memory 2026-09-11. |
| IronBlueprint | `8857ae2a-0e5d-4af3-be8a-5ee7f2b04e50` | Forge, Linus | Forge | LIVE. Forge's IB meeting ingest and IB web/mobile tasks post here (Forge, 2026-10-17). **CONFLICT:** FLEET.md lists a 2026-10-17 member plan of Forge, Linus, Scout, Max, Quill, Maya, but group.json has only Forge and Linus. |
| Programming | `7c23ca84-4ef9-4dd7-8421-66e0ab6932ec` | Darwin, PRI, Atlas, Coach, Hawkin | unclear (Atlas or Coach) | **ACTIVE per Ryne (2026-10-17).** **CONFLICT:** TEAM.md still has a pending item "Ryne to archive/delete the Programming room" and FLEET.md marks it RETIRED. Ryne's word wins: keep it. |
| Promote | `447d77a8-9873-4b04-821c-87d82cc8c284` | Lark, Maya, Max, Quill | unclear (likely Maya) | LIVE. No description set. |
| Newsletter | `e30bd05f-c397-44ba-bab7-506ea9f73193` | Quill, Maya, Canvas, Atlas | unclear (likely Quill or Maya) | LIVE. No description set. |
| Advisors | `f4cb7f33-0203-4bc5-a803-b5d8f4483365` | Travis Kalanick, Elon Musk, Alex Hormozi, Dan Martell | none (persona bots) | LIVE. Robert Greene and Sage are not members. |

---

## 3. Old and deleted IDs (do not use)

| ID | What it was | Source | Status |
|---|---|---|---|
| `0382da49-74aa-4f07-9175-22c6e94e2887` | Old IronBlueprint room | `/home/box/agent-data/deleted-agents.json`; FLEET.md line 1447 | **DELETED.** Only appears in stale automation copies. Forge confirmed 2026-10-17 none of his 6 live routines use it. |
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
| Achieve | achievept.slack.com | `user-Slack--achieve` | Ryne is not the workspace owner (Forge memory 2026-08-20; may refer to either workspace, UNCERTAIN). |
| IronBlueprint | ironblueprint.slack.com | `user-Slack--ironblueprint` | Messages to Suffescom go from Ryne's IB Slack, as drafts he approves. |

### Channels
| Channel | ID | Workspace | Used by (owner bot) | Source | Notes |
|---|---|---|---|---|---|
| #ironblueprint | `C09LEBCE40P` | Achieve | Forge (IB 500 daily pace post, IB 500 tally) | Forge 2026-10-17 message; `WS/ib-500-tally-log.md` | LIVE. Not the same as IB Slack #iron-blueprint below. |
| #programming | `C01KHUGT623` | Achieve | Hawkin (SJ/CMJ reports, weekly trends) | `A/93d38eed.../memory/profile.md` lines 11, 14 | LIVE. |
| #clients | `C1J8VTFU4` | Achieve (UNCERTAIN, inferred from Achieve client use) | Eval Brief (weekday 8:15am draft pass) | `A/690e65de.../profile.json`; TEAM.md line 92 | LIVE. Draft-first. |
| #bugs | `C0C8V38T082` | IronBlueprint | Forge (IB Slack bug watcher), Linus (triage) | `WS/ironblueprint-agent-prep/bug-triage-state.json`; `WS/thc/Forge.txt` | LIVE. |
| #web-app | `C06Q30B0UUA` | IronBlueprint | Forge (bug watcher) | `WS/thc/Forge.txt` (bug card "Source: IronBlueprint Slack #web-app") | LIVE. Name matched from one bug card. |
| #nexus-ai | `C06Q5DUACKE` | IronBlueprint | Forge (bug watcher) | `WS/agent-tools/*.txt` Basecamp card permalinks | **UNCERTAIN:** name inferred from nearby "#nexus-ai" mentions, not confirmed. |
| #mobile-app | not found | IronBlueprint | Forge (bug watcher) | Forge 2026-10-17 message (name only) | **MISSING ID.** Ask Forge. |
| #iron-blueprint | `C06LPV4C6P3` | IronBlueprint | Forge (Suffescom messages, as drafts) | `WS/agent-tools/b75a4930-....txt` (Chief brief to Forge) | LIVE. Easy to confuse with Achieve #ironblueprint. |

### Slack user IDs (Achieve workspace, for IB 500 tally)
Source: `WS/ib-500-tally-log.md`. Owner: Forge.
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
| Prospect Tracking (Achieve CRM sheet) | `1x8KurT1AJOPYLca6Jz9f_zBqZ3yBUGv8-isf8pctv4g` | Achieve work Google account | Tally (writes); Eval Brief (reads Sign-Up) | Tally memory line 6; Tally and Eval Brief profile.json; `W/achieve-prospect-tracking` | LIVE. |
| Prospect Tracking, 2026 tab | worksheet `502533256` | same | Tally | Tally memory line 7; Tally profile.json | LIVE. New rows go at the top. |
| SCDD Instant Form leads sheet | `1mASw_Y5-jRy6ccBSnLdQQAfA33IYGZjkrw0lOj8Q1HE` | same | Tally | Tally memory line 6 | Form watch RETIRED 2026-09-15; existing rows still get gap-fill. |
| Clients folder (eval Assessments) | `1o_k6aDUbkWcSJGYXwYbmI9wF-Hi78VAF` | Achieve Drive | Eval Brief | Eval Brief profile.json; TEAM.md line 90 | LIVE. |
| NTA / Jeremy Meserole Gemini meeting notes folder | `1RoZsVphbmcbv3RO6ds-BDokuqbDQFc0P` | Achieve Drive | Atlas | Atlas memory lines 28, 30 | LIVE. |
| Achieve TrainHeroic Exercise Library sheet | `1UnQjlyH_wbVGWDIHTU0BbXJlcNwkarQF9nTECDaQuW8` | Achieve Drive | TH Exercise Library | TH Exercise Library memory line 8 | LIVE. |
| Achieve TrainHeroic Exercise Progressions sheet | `1Sjn2AxfGor3jwkCybvtrf12lC5E0zZttY6ztLladk38` | Achieve Drive | TH Exercise Library | TH Exercise Library memory line 10 | LIVE. |
| IronBlueprint Stock Exercise Progressions sheet | `1kveJElUB335NQ_7zGqPbElJhxkmo2boJdH20R7qge1g` | IB Drive | TH Exercise Library (read-only template) | TH Exercise Library memory line 9 | READ-ONLY. Never edit. |
| IronBlueprint 500 Program Feedback Tracker | `1nGFHBgUfoDInpSnwfBTGBa5y-cG9eFCfWv5zniAax5E` | IronBlueprint Google account | Forge (IB 500 tally) | `WS/thc/Forge.txt` | LIVE. Forge's tally routine writes here. |
| IB "Web & Mobile Tasks" sheet (Suffescom-owned) | not pinned on purpose | IB Drive (owned by Suffescom / Gaurav) | Forge (weekday 9:00am check) | Forge automation prompt | The routine searches by title each run and must not trust a stale file ID. |
| Google Doc "Reviews" (Achieve Google reviews) | `1TBqWHIV0rm1mhvE-nKgepOwfc3005Bd02Q7f9rx6Hfg` | Achieve Drive | unclear (Maya / Max) | `WS/achieve-review-mining.md` | UNCERTAIN owner. |
| IB Athlete Design Guidelines (ADG) doc | `1MpY-3Js6F1_k0w57sNpfwfxQTcJtLn2vuclolg7n0oM` | IB Drive | Forge | `WS/ib-doc-conflicts.md` | Reference doc. |
| IB "V&I" doc | `1l3wefb5HybCGVWcmdoVY_SmmreIUxQRQk3o98slb5cU` | IB Drive | Forge | `WS/ib-doc-conflicts.md` | Reference doc. Full title not recorded. |
| Staff Meeting 2026-06-01 notes | `1b4trwYNmUx_XBUNTnrKxmLBlKT8cUclsXxBUnmf1OoI` | Achieve Drive | Penny (Staff Meeting template owner) | `WS/nta-jeremy-brief.md` (Drive doc index) | UNCERTAIN whether this is the template or one meeting's notes. |
| NTA Contract (unsigned template) | `1-A99TRyc6fekjPON_Kq4lBLY6hebPUGugCyPRraEUTk` | Achieve Drive | Atlas | `WS/nta-jeremy-brief.md` (Drive doc index) | Reference. |
| NTA meeting notes (9 docs, 2025-07-31 to 2026-05-08) | see the Drive doc index table in `WS/nta-jeremy-brief.md` | Achieve Drive | Atlas | same | Reference. Not repeated here. |
| Achieve Mindbody calendar | `c_fef09087722dbbc1c9f8fbd060f8fedd345c3837388c858758268befb6126ca4@group.calendar.google.com` | Google Calendar | Penny (morning brief) | `W/morning-brief` line 28 | LIVE. |
| IronBlueprint calendar | primary calendar of the IronBlueprint Google account (connector `user-Gmail--ironblueprint`; address not stored here) | Google Calendar (IB) | Penny (morning brief) | `W/morning-brief` line 29 | LIVE. Missing from `list_calendars`, so call it by the account. |

---

## 6. Basecamp

Account and projects: Forge memory profile.md line 13; Forge profile.json; `W/morning-brief`. Owner: Forge (reads only). Linus may note items on the engineering boards. Bots never create, comment, complete or post unless Ryne names the item.

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

### IronBlueprint code repos (Suffescom writes; Linus and Forge read only)
Source: `WS/ironblueprint-agent-prep/repo-map.md` (read-only audit 2026-10-17). Owner: Linus (review), Forge (PM).
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
| SEO AEO Auditor Data | `bc-2714e58d-28d0-57ae-9361-c731932df50e` | SEO / AEO Auditor | |
| Ads Performance Data | `bc-d90d9738-ac10-52df-8d72-4443fdbb0386` | Lark | |
| Achieve Programming Data warehouse | `bc-354df073-adf9-554e-aa92-46cfa180c48d` | Programming room (Coach, Atlas) | |
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

| Inbox | What | Connector | Who uses it | Source |
|---|---|---|---|---|
| Achieve work Gmail | Achieve work (primary). Address not stored here. | `user-Gmail--work` | Penny, Tally, Max, Atlas | `W/achieve-mail`; Forge memory line 15 |
| Achieve contact inbox | Public CTA inbox. Address not stored here. | `user-Gmail--contact` | Penny, Tally | `W/achieve-mail` |
| IronBlueprint Gmail | IronBlueprint Google account, calendar, and Drive. Address not stored here. | `user-Gmail--ironblueprint` | Forge, Penny | `W/achieve-mail`; Forge memory |
| Second IronBlueprint address | Not mapped to a connector. Address not stored here. | not mapped to a connector | Forge, Quill, Maya (copy context) | Scout, Quill, Maya memory; Forge profile.json |
| Personal Gmail | Personal. Address not stored here. | `user-Gmail--personal` | Penny, NSCA | `W/achieve-mail`; NSCA profile.json |
| Grok Bot inbox | Receive and read; parent agent sends. Address not stored here. | Grok Bot inbox | Chief | ListEmailInboxes 2026-10-17 |
| Staff BCC | BCC on account changes (Kara). Address not stored here. | n/a | Penny | `W/achieve-writing-style` |
| Achieve business text line | Public business number in signatures. Digits not stored here. | Quo (Numa until cutover) | Penny | `W/achieve-mail`; Nova profile.json |

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
| Zapier connection: Google Sheets (Achieve work account) | `02ca3905-95d2-80e0-b57c-e02585a27d1c` | Tally | Tally memory line 14 | Used for Prospect Tracking writes. |
| Ryne's Mac (registered machine) | `7d3c49a4-3b83-48f1-a860-c3821e2c2fff` | Linus (Passport drive staging) | Linus memory `local-llm-lane-from-ai-expert.md` | |
| Firebase project (IB web push) | `ironblueprint-faff9` | Forge / Linus | repo-map.md | Ryne-owned. |
| Firebase project used by backend push | `suffescom-mobiles` | Forge / Linus | repo-map.md; Ryne 2026-10-17 | **FLAG:** created by Suffescom, not Ryne. Ryne says he owns all accounts; this one needs an ownership check. |
| Nexus API host (prod) | `nexus-api.iron-blueprint.com` | Linus | repo-map.md | Host only. Secrets live in AWS SSM, never here. |
| USPTO serials | `99550047` (IRON BLUEPRINT, Ryne individually), `99383569` (IRONBLUEPRINT, Iron Blueprint LLC) | Forge | Forge memory line 7; IB decisions log | 99550047 examination suspended 2026-10-07. |
| Chief routine folders | `5a9f4a41-dbcf-5bdb-bcdf-f3cf132a4689` (6:50am priorities), `weeknight-evening-debrief`, `friday-evening-debrief`, `unfinished-promises-watch`, `weekly-brain-repo-update` | Chief | TEAM.md lines 46-49; Chief chat 2026-10-17 | Live routine IDs, not the stale on-disk copies. |
| Hawkin Dynamics integration key | location only: Hawkin bot and Atlas `secrets/` folders | Hawkin | Atlas memory line 42 | Secret. Value never copied anywhere. |

---

## 11. Conflicts and open questions

1. **36 skills point to a deleted agent.** Skills such as `exercise-progressions-and-selections`, every `*-progressions` ladder, `guide-to-tapering`, `program-design-basics`, `athlete-program-design-guidelines`, `adult-program-design-guidelines`, `isometrics-programming-guide`, `frc-progressions-and-prescriptions` and several `pri-*` skills cite `/home/box/agent-data/agents/0c56f311-.../memory/reference/...`. That folder is gone. The PRI manuals survive under PRI (`A/e9d0fc7f.../memory/reference/`), and `program-design-basics.txt` survives at `WS/uploads/`. The exercise progressions CSV and the tapering guide were not found anywhere on disk; the Achieve Programming Data Cursor project may hold copies. Highest priority fix.
2. **Programming room:** active per Ryne, but TEAM.md (pending archive) and FLEET.md (RETIRED) disagree. Update both.
3. **IronBlueprint room members:** on disk only Forge and Linus. FLEET.md's 2026-10-17 list adds Scout, Max, Quill, Maya.
4. **Retired bots:** six are gone from disk but not in deleted-agents.json. Confirm in the sidebar. Bottleneck still needs a sidebar delete. TEAM.md's pending list leaves out Lingxi.
5. **Tally memory has two stale IDs:** old Personal Assistant `8b769a17-...` (line 8) and a room description that still names CRM Watch and PA Schedules (line 28).
6. **Basecamp board name:** "Code Changes" (Linus instructions, FLEET.md) vs "Improvements" (Basecamp API).
7. **Slack names that look alike:** Achieve `#ironblueprint` `C09LEBCE40P` vs IronBlueprint `#iron-blueprint` `C06LPV4C6P3`.
8. **Missing IDs:** IB Slack `#mobile-app`, Quo inboxes, full Personal PR cloud agent ID, which account `user-Gmail` is.
9. **Asana:** "never Asana" in briefs vs the October marketing plan living in Asana.
10. **Midori's forecast location** is Aurora, IL (the gym is in Aurora). Ads now target Naperville (Ryne 2026-10-17). Both are correct for their own jobs; noted so nobody "fixes" one to match the other.

Sources: listed per row. Scan covered `A/*/profile.json`, `A/*/group.json`, `A/*/memory/*.md`, `/home/box/agent-data/workflows/*/SKILL.md`, `/home/box/agent-data/deleted-agents.json`, Chief TEAM.md, `WS/fleet/FLEET.md`, `WS/*.md`, `WS/ironblueprint-agent-prep/`, `WS/cloud-agent-transcripts/`, `WS/agent-tools/`. Secrets folders, connector secrets and `.env` files were not read.
