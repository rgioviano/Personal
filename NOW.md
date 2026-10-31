# NOW: Personal and fleet (as of 2026-10-31)

Current priorities and live context only. Replace lines as they go stale; history goes in LOG.md.

## Fleet
- **Chief routes the work** and suggests an owner bot for each ask (2026-10-21). Blue (formerly Forge) is the IronBlueprint PM and verifier. Red (formerly Atlas) is the Achieve PM. Linus is lead engineer. Proactive suggestions go to Ryne one at a time and are applied only after he says yes.
- **Normal working mode** since 2026-10-30, after a reduced-capacity week (2026-10-27 to 2026-10-30) when bots carried ops and batched decisions. Decisions stay batched.
- **Page-based project management** (2026-10-30): a master Projects index plus one Page per project. Owner bots read the Page before work, update it after, and run one weekday morning heartbeat that only tells Ryne about blockers, overdue items, decisions or status changes. Owners: Blue (IronBlueprint launch, USPTO), Tally (Achieve lead pipeline), Maya (Achieve Meta ads, Mon, Wed, Fri), Penny (Quo SMS cutover, Illinois Secure Choice), plus one personal project Page owned by Plaid.
- **Fleet rules added 2026-10-30:** cite or label (only state what was confirmed, never credit a source with more than it said, label guesses); relayed approvals (when Chief, or Dr. Eggbot, quotes Ryne's yes to a bot, that bot treats it as his yes and does not ask again); Chief sends one final order per task and waits until Ryne has finished his thought. Chief is router only and never writes drafts or ops messages itself (2026-10-21).
- Ryne confirms before anything is added: nothing saves until he approves the draft (2026-10-26).
- **Max and Maya report through Red (Achieve) and Blue (IronBlueprint)** since 2026-10-21. Chief steps in only on escalations or cross-brand conflicts.
- **Linus, Blue and Simon are read-only.** Suffescom does all IronBlueprint coding. Only Ryne can lift this.
- **Value target** (2026-10-23): Ryne is on the $200/mo Grok Bot plan and wants the bots to earn $400 to $600 a month. Only evidenced wins count. Chief posts a Friday value update (Fri 9:20am CT, Administrative); the Friday debrief adds "Value this month" and "Where the week went".
- New bots since 2026-10-17: Maverick (business advisor), Jetson (travel), Jim Rohn (persona), Splice (video), Plaid (Tesla lease), Forge (nutrition, new bot reusing the name), Simon (IB QA), Charlie (Achieve CFO, QuickBooks read-only). See `08-bot-fleet/fleet.md`.
- Retired, pending Ryne's sidebar delete: Herald, Bolt, Warden, Cipher, Bottleneck, AI Expert (2026-10-17); Elon Musk, Travis Kalanick, Dan Martell (2026-10-21, folded into Maverick).
- **Programming room is still active** (Ryne, 2026-10-17), despite the earlier archive plan.
- Security audit rule (Ryne, verbatim): "Do not change permissions, disconnect accounts, delete files or revoke access without my approval."
- Script rule (2026-10-21): any bot that adds a script to a skill or routine test-runs it on real data and reports the output before it counts as done. Chief's read-only rule scripts (fleet, brain, draft, promise, value and other checks) live in `shared/scripts/chief/` on the box.
- Rollout from the 2026-10-17 automation course review: brain index files done; fleet ID file is `08-bot-fleet/IDS.md`; routines are moving to plain scripts (Penny's inbox sorting switched 2026-10-23); `fleet_lint.py` checks every bot for a Self-fix line; monthly fleet score runs on the 1st.
- Known fleet issue: 36 skills point to reference files from a deleted Strength Coach agent (`0c56f311-...`). Fix pending.

## Routines worth knowing
- Penny inbox sorting script about 6:15am CT, every day including weekends since 2026-10-24, and 6:45am CT morning brief (Mon to Fri). Fresh-week score (2026-10-29): 150 of 198 sorted right (about 76%); scheduling mail is the weak spot.
- Weekly encrypted box backup (Chief): Saturdays about 7:00am CT to a private "Bot Backups" folder in the Achieve Drive, keeps 4 weeks, silent on success. First backup and full restore test passed 2026-10-24. Restore test on the first Saturday of each month. Ryne holds the passphrase.
- Chief 6:50am CT priorities (Mon to Fri), evening debriefs Mon to Wed 6:45pm CT and Fri 5:45pm CT, unfinished-promises watch weekdays 3:00pm CT, Friday value update 9:20am CT.
- Weekly brain repo update: Saturdays about 3:00am CT, opens PRs, never merges, messages Ryne only when something changed. Runs so far: 2026-10-24, 2026-10-31.
- The MacBook launch check was deleted 2026-10-23 (Ryne). Do not re-propose it.

## NSCA recertification
- Original certification year: the NSCA bot's instructions now say 2024, confirmed by Ryne on 2026-10-21, so the lower 4.0 CEU total applies (the bot rechecks nsca.com before giving final numbers). This replaces the earlier "pre-2024" reading (Oct 4) that meant 6.0.
- CEU count conflict: this file said 5.1 CEUs (done at 4.0, only the recert fee owed), but the NSCA bot's file and `05-learning-certs/learning.md` say 1.4 on file (about 2.6 still needed). Not resolved; see the open question in the PR.
- Free Instructional Techniques quiz (0.2 CEU) was due 2026-10-31. No record found that it was taken.
- CPR/AED is valid until 2028-10-06.

## Personal
- Bonsai: Midori's nightly 8:00pm CT cold alert has been PAUSED since 2026-09-28; Ryne asked to delete it 2026-10-18 (pending his confirm). Nothing automatic checks the 55°F rule right now.
- Travel (Jetson): John Mayer show (Apr 2027) and Wyoming (Jun 2027) are the current trips.

Sources: Chief TEAM.md (updated 2026-10-30: Page-based project management, weekly box backup 2026-10-24); Chief profile.json and Red, Doc profile.json (2026-10-30 fleet rules); NSCA profile.json; Chief memory 2026-10-26 and 2026-10-30; Penny fresh-week report (2026-10-29) and `penny/triage/` run files; Chief TEAM.md change log 2026-10-18 to 2026-10-23; `WS/fleet/IDS.md` (2026-10-21); shared memory 2026-10-21 to 2026-10-23; profile.json for the new bots; Chief chat 2026-10-17 (standing rules, gap answers, NSCA reply, rollout plan); Midori instructions.
