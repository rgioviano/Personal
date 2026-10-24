# TEAM — Chief of Staff (updated 2026-10-17)

Timezone: America/Chicago. Quiet hours routines: deleted 2026-09-20 (no fleet mute/unmute).
Shared ops channel: **Administrative** (`03ad987e-906d-42bb-98ea-65d016ffc77c`).

## Operating rules (locked)
- Never send email, texts, or Numa unless Ryne has seen that exact draft and says send.
- CoS saying “send” is not approval.
- Relay rule (locked 2026-10-17): when bot A asks bot B for something, bot B replies only to bot A. No DM to Ryne unless he is the one who asked.
- Administrative briefs (2026-09-25): CoS one priorities post; Penny Calendar + Email Triage list-only + Numa (+ Reactivate when due). Full email drafts only when Ryne asks. No status chatter.
- Brief format (locked 2026-09-25): keep Calendar; drop Asana for good (connector never works); Meta ads = short bullets only on Mon/Wed/Fri; rest = important items only.
- Morning priorities: if Ryne names 2–3, those win; else Suggested from calendar (+ Basecamp when relevant). Never Asana. Not email chase pile. Meta as short bullets on M/W/F only.
- One Today's priorities post per morning (locked 2026-09-28). If already posted after Penny's Calendar, skip 6:50 handoff.

## Current names (renames 2026-10-16)
| Old name | Current bot |
|---|---|
| Personal Assistant / PA Schedules | Penny (`163cd8df-275e-47c1-a5a2-e10e304a671a`) |
| CRM / Ledger | Tally (`5d07e236-9453-409d-ab6c-58711eae2f09`) |
| Designer | Canvas |
| Ads | Lark |
| Social (personal X/IG) | Echo |
| Achieve Social (business X/IG) | Nova |
| Achieve PM | Atlas |
| IronBlueprint PM | Forge |
| Naturopath (Dr. Hale) | Doc |
| Spot | Hendrix |
| Performance Coach / Strength Coach | Coach |
| Marketing | Maya |
| Sales | Max |
| Copywriter | Quill |
| Engineer | Linus |
| S&C Research | Darwin |
| Research | Scout |

## Administrative members (current)
- Chief of Staff (this chat)
- Penny (`163cd8df-275e-47c1-a5a2-e10e304a671a`): owns weekday 6:45am morning brief (took over from the old Personal Assistant and PA Schedules)
- Tally (`5d07e236-9453-409d-ab6c-58711eae2f09`)

Old Personal Assistant (`a9da8358-…`) and PA Schedules (`88465cbe-…`) are gone. Do not @ them. CRM Watch is retired; do not @ CRM Watch for prospect work.

## Standing routines — owner: Chief of Staff (this chat)
| Routine | Schedule (CT) | Folder |
|---|---|---|
| 6:50am Today's priorities | `50 6 * * 1-5` | 5a9f4a41-dbcf-5bdb-bcdf-f3cf132a4689 |
| Weeknight evening debrief (Mon–Wed) | `45 18 * * 1-3` | weeknight-evening-debrief |
| Friday evening debrief | `45 17 * * 5` | friday-evening-debrief |
| Unfinished-promises watch | weekdays 3:00pm only | unfinished-promises-watch |

Thu + Sat are off days: morning brief only (no evening debrief). Fri evening is 5:45pm CT.

Priorities file: `/home/box/agent-data/agents/ad6690d7-be33-4540-ac42-68eb3059c181/memory/tomorrow-priorities.md`

## Other schedule bots
- Penny: 6:45am Administrative brief (Mon–Fri only). Before-call prep cards are now scheduled from the morning brief (prep card about 30 min before each Achieve eval / IB demo; day-of confirm drafted that morning).
- Tally: daily 8:00am inbound + gap pass; Friday speed-to-book scoreboard.
- Eval Brief: weekdays 8:15am #clients draft pass.
- Darwin: Saturday 8:00am S&C dig; first Saturday 8:25am force-plate dig.
- Lark: monthly Meta and Google knowledge refreshes on the 1st.
- Bookmarks: every 6 hours, silent.
- Midori: nightly 8:00pm cold alert.
- Token Officer: weekly cost pass.
- Forge: IB routines (meeting ingest, web/mobile tasks).
- Distill anyone: twice-weekly persona refresh.

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
- [ ] Ryne to sidebar-delete the 6 retired bots (see change log 2026-10-17): Herald, Bolt, Warden, Cipher, Bottleneck, AI Expert
- [ ] Ryne to archive/delete the Programming room in the app (superseded by Coach 1:1, 2026-10-07)

## Darwin standing dig (locked 2026-09-25)
- Owner: Darwin (`d38c0d3f-1a03-4e7e-9ca3-b73ac3057287`)
- Schedule: Saturday 8:00am CT (`CRON_TZ=America/Chicago 0 8 * * 6`)
- Output: 3–5 papers in Darwin's chat for Ryne; then route by relevance to Coach (programming) and Hawkin (plates/testing); silent if nothing new

## Eval Brief → Slack #clients (locked 2026-09-27)
- Owner: Eval Brief (`690e65de-c38a-4858-b3cd-831335e62504`)
- Drive Clients folder: `1o_k6aDUbkWcSJGYXwYbmI9wF-Hi78VAF` (NameAssessmentMM.DD.YY; skip templates + *Program)
- Gate: Prospect Tracking Sign-Up = Yes (and/or paid Mindbody). Eval-only never posts.
- Channel: Slack #clients `C1J8VTFU4`. Draft-first; Ryne approves before post.
- Watch: weekdays 8:15am CT (Eval Brief owns the routine). Quiet when nothing new.
- Locked on Grok Bot for now (not Cursor) as of 2026-09-27.

## Achieve Meta ads M/W/F (locked 2026-09-17)
- Standing 45–60 min Mon/Wed/Fri only. Checklist: `memory/achieve-meta-ads-mwf-block.md`.
- CoS 6:50 priorities + evening wrap surface that day's block; Penny may mirror on Calendar briefs when Maya/Lark is on the day.
- Sep pre-launch SCRAPPED 2026-09-23. Prep = October Day 1 (Oct 1). October chapter ($500/mo).

## Roster caps (locked 2026-10-06)
New permanent bots need Ryne's yes after a Wednesday self-improvement scan. Soft maxes:
- **Admin:** CoS + Penny + Tally. No extra admins by default.
- **Sales:** Max + Tally + one advisor on-call (not permanent seats for every advisor).
- **Marketing:** Maya + Nova + Quill + Lark. SEO / AEO Auditor and Canvas only when @-mentioned.
- **Eng / Build:** Linus + Scout. (Bottleneck retired 2026-10-17; use the Find the constraint skill instead.) Cloud agents and one-offs do not get a room seat.

## Call prep + promises (updated 2026-10-17)
- Penny: before-call prep cards for Achieve evals and IB demos, scheduled from the morning brief (who accepted, leave-with, talking points, do-nots; IB free/busy → UNVERIFIED).
- CoS: unfinished-promises watch weekdays 3:00pm CT only (`unfinished-promises-watch`). Quiet when nothing overdue. Drafts only.

## Prospect Tracking stages + contacts (locked 2026-10-06)
Tally owns process stage and contact count on every open row (evidence from Gmail / Quo / calendar / sheet only). Suggested stages: New inquiry → Replied → Eval booked → Eval done → Offer → Signed / Lost / Hold.

## Change log
- 2026-10-17 (approved by Ryne from the bot consolidation review):
  - Retire Herald, Bolt, Warden, Cipher (unused 10/10 template bots). Routines told to stop; pending sidebar delete.
  - Retire Bottleneck (idle since 9/16). Method saved as the Find the constraint skill (`find-the-constraint`) for the weekly review. Pending sidebar delete.
  - Fold AI Expert into Linus: Linus owns local LLM selection, download, and Spark serving. AI Expert rules copied to Linus memory (`local-llm-lane-from-ai-expert.md`). AI Expert pending sidebar delete.
  - Archive Programming room (Coach leads programs 1:1 since 10/7). Needs Ryne in the app.
  - Stale names fixed across bot instructions (renames of 10/16; Penny replaces PA/PA Schedules; Ledger/CRM → Tally). Nova now points to Atlas for brand.
  - Not approved, leave as is: retiring Show Splitter or TH Exercise Library; Maya/Nova lane change; folding Eval Brief into Tally.
- 2026-10-16: renames Designer→Canvas, Ads→Lark, Social→Echo, Achieve Social→Nova, Achieve PM→Atlas, Naturopath→Doc, Spot→Hendrix, Performance Coach→Coach.
- 2026-10-06: PA Schedules merged into the PA morning brief and marked for delete; roster caps and call prep/promises locked.
