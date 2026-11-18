# NOW: Personal and fleet (as of 2026-11-18)

Current priorities and live context only. Replace lines as they go stale; history goes in LOG.md.


## Changes since the 2026-11-06 sync (added 2026-11-18)
- **New Chief agent** (`88d94ba3-a54b-42c5-99a1-2b85c442eea6`) since 2026-11-07, set up from the replacement package with its nine routines turned on (Ryne, 2026-11-07 7:07am CT). The old Chief (`ad6690d7`) is retired. Chief is router only, gives each bot one final order, and sends Ryne one consolidated update.
- **Numa retired (Ryne, 2026-11-17).** Quo only. Never check, mention or report Numa.
- **Memory process (Ryne, 2026-11-17):** save rules, not stories (one dated sentence, delete the note it replaces in the same step); "remember this" is saved at once and confirmed in one line; a Decisions log Page is kept (Chief); a Monday tidy-up (routine `monday-memory-tidy-up`, Mondays about 8:30am CT, first run 2026-11-23) proposes deletes and merges and changes nothing until Ryne says yes; before answering about the past, check notes and the Decisions log first.
- **Fleet governance (Ryne, 2026-11-10):** Chief routes work and owns TEAM.md; Alfred (new, `d5abaffd`) is a read-only org design and audit advisor; Token Officer handles cost and approved schedule fixes; Dr. Eggbot builds and edits bots.
- **New bots:** Alfred (fleet audit advisor) and Dewey / Notes (`6c6861fd`, files Ryne's notes into Notion, on demand). Midori now runs under a new agent id (`905a74fc`); its old cold alert was deleted 2026-10-19. **Retired:** Maverick (empty folder deleted 2026-11-10).
- **Names:** profiles use "Name / Title" since 2026-11-06 (replaces "Name · role").
- **Avatars (Ryne, 2026-11-08):** Chief hexagon; business leads square; business specialists blob; personal teardrop. Colors: Achieve red, IronBlueprint blue, shared orange, personal green, other cyan, support violet. Chief should be white, but white is not in the color picker; the current Chief color was not checked.
- **Research:** everything goes to Scout (2026-11-07); Perplexity is Scout only (2026-11-11, trial).
- **Drafts (2026-11-11):** email drafts are saved in Gmail or Spark Drafts by the owner; Spark owns the signature; Quo text drafts stay in chat.
- **Capitalization (Ryne, 2026-11-15):** bots use normal capitalization, never all-lowercase.
- **Brain repo:** this 2026-11-18 sync is the first update since 2026-11-06. The weekly Saturday job now prepares changes and waits for Ryne's yes before pushing (Chief, 2026-11-18).

Sources: Chief notes TEAM.md (2026-11-07 to 2026-11-17); shared Chief TEAM.md (2026-11-17); Decisions log Page; profile.json files on the box (2026-11-18).

## Fleet
- **Chief routes the work** and suggests an owner bot for each ask (2026-10-21). Blue (formerly Forge) is the IronBlueprint PM and verifier. Red (formerly Atlas) is the Achieve PM. Linus is lead engineer. Proactive suggestions go to Ryne one at a time and are applied only after he says yes.
- **Normal working mode** since 2026-10-30, after a reduced-capacity week (2026-10-27 to 2026-10-30) when bots carried ops and batched decisions. Decisions stay batched.
- **Page-based project management** (2026-10-30): a master Projects index plus one Page per project. Owner bots read the Page before work, update it after, and run one weekday morning heartbeat that only tells Ryne about blockers, overdue items, decisions or status changes. Owners: Blue (IronBlueprint launch, USPTO), Tally (Achieve lead pipeline), Maya (Achieve Meta ads, Mon, Wed, Fri), Penny (Quo SMS cutover, Illinois Secure Choice), plus one personal project Page owned by Plaid.
- **Fleet rules added 2026-10-30:** cite or label (only state what was confirmed, never credit a source with more than it said, label guesses); relayed approvals (when Chief, or Dr. Eggbot, quotes Ryne's yes to a bot, that bot treats it as his yes and does not ask again); Chief sends one final order per task and waits until Ryne has finished his thought. Chief is router only and never writes drafts or ops messages itself (2026-10-21).
- Ryne confirms before anything is added: nothing saves until he approves the draft (2026-10-26).
- **Max and Maya report through Red (Achieve) and Blue (IronBlueprint)** since 2026-10-21. Chief steps in only on escalations or cross-brand conflicts.
- **Linus, Blue and Simon are read-only.** Suffescom does all IronBlueprint coding. Only Ryne can lift this.
- **Value target** (2026-10-23): Ryne is on the $200/mo Grok Bot plan and wants the bots to earn $400 to $600 a month. Only evidenced wins count. Chief posts a Friday value update (Fri 9:20am CT, in the Chief 1:1 chat since 2026-11-04); the Friday debrief adds "Value this month" and "Where the week went".
- New bots since 2026-10-17: Maverick (business advisor), Jetson (travel), Splice (video), Plaid (Tesla lease), Forge (nutrition, new bot reusing the name), Simon (IB QA), Metric (data and metric deep dives, profile dated 2026-11-03). Hendrix is now named Spot. See `08-bot-fleet/fleet.md`.
- **Briefs (2026-11-04):** morning brief in Penny's 1:1 chat, evening debriefs and Friday value update in the Chief 1:1 chat. Nothing posts in group chats. No priorities in briefs; Ryne sets his own.
- Retired: Herald, Bolt, Warden, Cipher, Bottleneck, AI Expert (2026-10-17); Elon Musk, Travis Kalanick, Dan Martell (2026-10-21, folded into Maverick); Show Splitter, Echo, Alex Hormozi (into Maverick), Robert Greene and Jim Rohn (into Sage) (2026-11-01). Only Bottleneck's sidebar delete is still open.
- **Retired 2026-11-05 (Ryne):** Charlie (Achieve CFO bot) and Distill anyone (with its twice-weekly persona refresh) are deleted; the Programming and HQ rooms are gone.
- Security audit rule (Ryne, verbatim): "Do not change permissions, disconnect accounts, delete files or revoke access without my approval."
- Script rule (2026-10-21): any bot that adds a script to a skill or routine test-runs it on real data and reports the output before it counts as done. Chief's read-only rule scripts (fleet, brain, draft, promise, value and other checks) live in `shared/scripts/chief/` on the box.
- Rollout from the 2026-10-17 automation course review: brain index files done; fleet ID file is `08-bot-fleet/IDS.md`; routines are moving to plain scripts (Penny's inbox sorting switched 2026-10-23); `fleet_lint.py` checks every bot for a Self-fix line; monthly fleet score runs on the 1st.
- Known fleet issue: 36 skills point to reference files from a deleted Strength Coach agent (`0c56f311-...`). Fix pending.

## Routines worth knowing
- Penny inbox sorting script about 6:15am CT (ran every day including weekends in the 2026-10-24 to 2026-10-30 run files), and 6:45am CT morning brief (Mon to Fri) in her 1:1 chat. Fresh-week score (2026-10-29): 150 of 198 sorted right (about 76%); scheduling mail is the weak spot.
- Weekly encrypted box backup (Chief): Saturdays about 7:00am CT to a private "Bot Backups" folder in the Achieve Drive, keeps 4 weeks, silent on success. First backup and full restore test passed 2026-10-24. Restore test on the first Saturday of each month. Ryne holds the passphrase.
- Chief: evening debriefs Mon to Wed 6:45pm CT and Fri 5:45pm CT, unfinished-promises watch weekdays about 3:00pm CT, changelog watch Mon 8:03am CT, Monday usage check-in about 9:30am CT, Friday value update 9:20am CT, monthly fleet score on the 1st about 9:00am CT. The 6:50am priorities routine was deleted 2026-11-04. Full map: `08-bot-fleet/fleet.md`.
- Weekly brain repo update: Saturdays about 3:00am CT. Since the 2026-11-07 Chief replacement it prepares proposed changes and waits for Ryne's yes before pushing (Chief, 2026-11-18); the 2026-11-04 auto-merge rule is not in use. Earlier note: opens PRs and, since 2026-11-04, merges them into main after `brain_lint.py` passes. Runs so far: 2026-10-24, 2026-10-31, plus a full sync on 2026-11-05 (Ryne asked for the repos to match Grok Bot exactly).
- The MacBook launch check was deleted 2026-10-23 (Ryne). Do not re-propose it.

## NSCA recertification
- Original certification year: the NSCA bot's instructions now say 2024, confirmed by Ryne on 2026-10-21, so the lower 4.0 CEU total applies (the bot rechecks nsca.com before giving final numbers). This replaces the earlier "pre-2024" reading (Oct 4) that meant 6.0.
- CEU count conflict: this file said 5.1 CEUs (done at 4.0, only the recert fee owed), but the NSCA bot's file and `05-learning-certs/learning.md` say 1.4 on file (about 2.6 still needed). Not resolved; see the open question in the PR.
- Free Instructional Techniques quiz (0.2 CEU) was due 2026-10-31. No record found that it was taken.
- CPR/AED is valid until 2028-10-06.

## Personal
- Bonsai: Midori's nightly 8:00pm CT cold alert has been PAUSED since 2026-09-28; Ryne asked to delete it 2026-10-18 (pending his confirm). Nothing automatic checks the 55°F rule right now.
- Travel (Jetson): John Mayer show (Apr 2027) and Wyoming (Jun 2027) are the current trips.

Sources: Chief TEAM.md (updated 2026-10-30: Page-based project management, weekly box backup 2026-10-24); Chief profile.json and Red, Doc profile.json (2026-10-30 fleet rules); NSCA profile.json; Chief memory 2026-10-26 and 2026-10-30; Penny fresh-week report (2026-10-29) and `penny/triage/` run files; Chief TEAM.md change log 2026-10-18 to 2026-10-23; `WS/fleet/IDS.md` (2026-10-21); shared memory 2026-10-21 to 2026-10-23; profile.json for the new bots; Chief chat 2026-10-17 (standing rules, gap answers, NSCA reply, rollout plan); Midori instructions.; Chief TEAM.md (updated 2026-11-04 evening); Chief current routine list (2026-11-05); profile.json for Metric and Spot (2026-11-05).
