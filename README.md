# personal-brain

Ryne Gioviano's personal brain. Start with **AGENTS.md**.

- 01-profile-preferences/profile.md
- 02-health/README.md (placeholder, points to Doc)
- 03-music-guitar/music.md
- 04-bonsai/bonsai.md
- 05-learning-certs/learning.md
- 06-family/README.md (empty placeholder)
- 08-bot-fleet/fleet.md
- skills/knowledge-base-audit/SKILL.md

Status: private GitHub repo rgioviano/Personal since 2026-10-17. Fully re-synced from Grok Bot on 2026-11-05.

Sources: this folder; Chief chat 2026-10-17.

## Skills index (63 skills)

Each skill lives in `skills/<slug>/SKILL.md` (some have extra reference files). Synced from Ryne's Grok Bot skill library on 2026-11-05. Em dashes were swapped for hyphens and email addresses that are not Ryne's business addresses were replaced, per the repo rules.

- `knowledge-base-audit`: End-of-day audit that proposes brain edits as a diff for Ryne's approval (the weekly update auto-merges after lint, 2026-11-04).
- `advisor-persona-vs-ghostwrite`: Use this when an advisor or distilled-persona bot is asked “if you were me,” for a take in their voice, or for something to send - fork persona (founder-pov) vs ghostwrite (user’s outbound voice).
- `ai-models-spark-shelf-first`: Use when AI Models or Engineer recommends open-weight downloads for the DGX Spark - prefer NVFP4 or EXL3 on Spark (not Mac GGUF); re-list Passport shelf and beat local models before suggesting anything new.
- `build-dashboard`: Use when the user wants a live or static paid-ads / SEO dashboard: KPIs, one primary chart, supporting tables. Pull real data first.
- `build-deck`: Use when the user wants a slide deck, audit report, or monthly recap as a designed HTML presentation - not a bullet dump.
- `cheap-routines`: Use when creating or changing a Grok Bot routine, auditing bot token usage, or deciding whether recurring work belongs on a long chat or a fresh bot.
- `design-grok-bot`: Use this when designing or creating a new Grok Bot, or editing another bot's description. Ask a few preference questions, write a tight persona, CreateAgent, settle a one-word name and the avatar, then verify against the live profile before reporting. Coding bots use pstack / poteto-mode as the quality bar. Mentor/counsel bots default to advice-only (no homework). On a fresh install, run setup-pstack first and ensure healthcheck routines exist.
- `distill-anyone-first-run`: Use on first turn after importing Distill anyone, and when adding another person: who-to-distill, lock identity, seed, immediately distill including official posts and quoted voice examples, then create a Distilled bot that speaks as that person and point the user at it. After a first real distill of a new person, ask once about Distill daily, then once about a GitHub mirror. If they say yes to the mirror, follow distill-github-mirror.
- `distill-daily`: Recipe for the Distill daily routine and for a person's initial distillation: refresh one subject at a time, including long-form appearances, official post bodies with age-band sampling, and quoted voice examples. Not the schedule itself. A first-run bootstrap follows the write steps, then stops. If github_mirror is already true, follow distill-github-mirror Later refresh, which compares to last_publish and stays quiet when they match. Do not copy the local skill folder.
- `distill-github-mirror`: Use only after the user opts in to a GitHub mirror for one distilled person. States the delta between the local skill folder and the public repo, publishes that repo, and sets the later refresh. Do not use this when they decline the mirror.
- `doc-health-source-router`: Use on every Doc / naturopath health question for Ryne: classify the ask, pick primary and secondary locked sources, apply conflict and never-stop rules, then load the matching Distill folder or reference skill before answering.
- `film-director-craft`: Use when writing a scene, shot list, generation brief, or recut as a film director. Cards require scale, angle, move, lens, key, sound, and a verb - not adjectives.
- `find-the-constraint`: Use when someone asks "what's my constraint/bottleneck?", shares a business or project dump and wants it analyzed, or a weekly review needs one focus. Names the single constraint between here and the goal and the one move that relieves it this week.
- `jack-kruse`: Use when Ryne asks about Dr. Jack Kruse or anything in his framework, including sunrise and daytime light, blue light at night, nnEMF and 5G, grounding, magnetism and geomagnetic claims, cold thermogenesis, deuterium and low-deuterium eating, Epi-Paleo, the Leptin Rx, melanin and POMC, his cancer, sleep, or eye theories, Survivors Soup or bone broth, or an X post, Patreon post, blog post, or lecture of his. Read before you answer, even from memory. It covers his order of priorities, where the local archive lives, how to look up a post, and how to cite each claim to a dated public or Patreon source without turning it into a dose or order.
- `make-bot-ui`: Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when exposing that UI on Tailscale.
- `morning-brief`: Use for Penny's weekday 6:45am Achieve morning brief: calendar, triage reuse, prep cards, lead follow-ups, waiting-on-reply, and drafts - delivered to Ryne in Penny 1:1 only.
- `new-chat-vs-delete`: Use this when the user cannot find a bot, asks what to delete, wants a fresh chat, or is unsure whether to remake a group room vs delete an agent - one durable decision map and real click-paths.
- `per-clip-scene-research`: Use when planning or generating any film clip: research similar cinema stills in the browser first, analyse the setup, then write the card. Never generate from adjectives or memory alone.
- `persona-exec-assistant`: Executive assistant persona for Spark. Morning briefings, draft replies, schedule management, and contact lookup.
- `persona-founder`: Founder / CEO persona for Spark. High-volume triage, aggressive delegation, cross-team oversight, and selective engagement.
- `persona-freelancer`: Freelancer / solo operator persona for Spark. Multi-client management, invoice follow-ups, availability, and quick responses.
- `persona-meeting-manager`: Meeting manager persona for Spark. Meeting preparation, transcript review, follow-up drafts, and scheduling.
- `persona-project-manager`: Project manager persona for Spark. Project thread tracking, stakeholder updates, action item extraction, and cross-team coordination.
- `persona-sales-rep`: Sales rep / account manager persona for Spark. Client relationship tracking, pipeline review, follow-up cadence, and deal context.
- `persona-support-agent`: Support agent persona for Spark. Shared inbox processing, assignment, templated responses, and escalation via delegation.
- `persona-team-lead`: Team lead persona for Spark. Team workload review, assignment distribution, shared inbox triage, and standup preparation.
- `personal-social-brand`: Use when drafting Ryne Gioviano's PERSONAL X or Instagram (his face and voice), not Achieve business accounts.
- `recipe-calendar-audit`: Analyze meeting load over a time range: total meetings, meeting hours, busiest days, back-to-back chains, and free blocks.
- `recipe-delegate-and-track`: Assign emails to teammates with context and track delegation status.
- `recipe-draft-batch`: Review and finalize multiple pending drafts in a batch session: read context, edit, or discard.
- `recipe-end-of-day`: End-of-day review: check for loose ends, review pinned items, and preview tomorrow's calendar.
- `recipe-inbox-by-category`: Process inbox in priority order by Spark's smart categories: priority first, then people, invites, notifications, newsletters.
- `recipe-inbox-zero`: Process inbox to zero using category-first triage: review by category, read threads, then archive, move, or mark done.
- `recipe-invitation-manager`: Process pending calendar invitations: check availability and present a decision list with recommendations.
- `recipe-label-organize`: Organize emails with labels and folders: attach labels, detach wrong ones, and move misfiled emails.
- `recipe-meeting-followup`: Review a meeting transcript and draft follow-up emails with action items to attendees.
- `recipe-meeting-prep`: Prepare for an upcoming meeting: check agenda, search for email context, look up attendee details, and flag open threads that should be raised.
- `recipe-morning-standup`: Morning standup briefing: today's events, unread people and priority mail, and team assignment status.
- `recipe-multi-account-review`: Review inbox status across multiple email accounts with per-account breakdown and cross-account priorities.
- `recipe-new-sender-review`: Process GateKeeper's new sender queue: review, accept legitimate contacts, and block unwanted senders.
- `recipe-newsletter-cleanup`: Audit newsletter subscriptions: block unwanted senders, unsubscribe from mailing lists, and enable AI summaries for worth-keeping ones.
- `recipe-notification-hygiene`: Tame notification overload by reclassifying noisy senders, grouping repetitive notifications, and bulk-archiving cleared alerts.
- `recipe-priority-tuning`: Fine-tune Spark's priority category by marking key contacts as primary and adjusting notification importance.
- `recipe-schedule-meeting`: Find mutual availability with attendees and suggest meeting times.
- `recipe-shared-inbox-status`: Review shared inbox health: open vs. done items, unassigned work, and per-member assignment breakdown.
- `recipe-shared-inbox-triage`: Process open items in shared inboxes: review, assign, respond, or mark done.
- `recipe-stakeholder-brief`: Build a comprehensive dossier on a person by pulling all meetings they attended and email threads with them into a single relationship brief.
- `recipe-team-workload`: Audit team assignment distribution: per-member loads, delegated items, unassigned work, and workload imbalances.
- `recipe-topic-timeline`: Build a chronological narrative for a topic by interleaving meeting transcript excerpts and email thread summaries across a time range.
- `recipe-unsubscribe-audit`: Full unsubscribe audit: scan inbox, archive, and GateKeeper for newsletter senders, classify by volume and engagement, detect phishing and duplicate subscriptions, then unsubscribe via spark action or extracted footer links.
- `recipe-vacation-catchup`: Process a large email backlog after time away: assess by category, batch-archive noise, and surface what needs attention.
- `recipe-weekly-digest`: Weekly summary: this week's meetings, unread email breakdown by category, and team assignment status.
- `remake-bot`: Use this when remaking a Grok Bot that is fat, broken, or needs a clean chat - copy the live persona, recreate the agent, move every routine to the new bot, then mark the old chat safe to delete.
- `room-owner-filter`: Use in any Grok Bot group room when a message wakes you: only speak if the ask matches your lane or you were @-mentioned; room broadcast is not an assignment - stay silent, no “not my lane” courtesy replies.
- `routine-healthcheck`: Use when auditing Grok Bot routines for token waste, offering a fleet checkup after template import, deciding cadence, or running the standing routine-healthcheck wake.
- `sheet-write-readback`: Use whenever you write to a spreadsheet (Google Sheets directly or through Zapier) or keep a running total in one. A success response is not proof the row is right: read it back, never retry blind, and treat the sheet as truth.
- `silent-run-heartbeat`: Use in any routine or watcher that stays quiet when nothing is new (inbox watches, sheet diffs, API pulls, listeners). Empty is not zero: log every run and alert on unexpected emptiness, missed runs, or connector errors.
- `transcript-healthcheck`: Use when auditing Grok Bot fleet transcripts for user friction, proposing new skills/bots/routines from repeated corrections, or running the standing transcript-healthcheck routine.
- `use-spark`: Use the spark CLI to access the user's Spark email data - list emails, search by topic, read threads, check calendar events, find availability, look up contacts, and view team info. Use when the user asks about their emails, calendar, contacts, meetings, or scheduling.
- `verify-live-before-acting`: Use before ranking, proposing, reporting on, or changing any routine, or before citing a routine's schedule, status, target room, or last run. Live status first; stale copies are never proof.
- `video-post-production-director`: Use when turning raw camera, screen, audio, and graphics into a finished video with edit, color, sound, captions, graphics, and QC. Preserve originals. Never publish or delete without approval.
- `viral-short-form-producer`: Use when cutting truthful platform-ready vertical shorts from existing footage. Never guarantee virality, distort meaning, publish, or delete without approval.
- `x-scout-connect-onboarding`: Use this when an X Scout (or similar) bot starts for a new user, X is missing/needsAuth, or after they just connected X - connect card → inspect live setup + posts → How you work once → finds-only digests → multi-select which finds to add.

## Bots index (20 bots and rooms)

Each bot lives in `bots/<slug>/`: `INSTRUCTIONS.md` (its profile.json instructions), `ROUTINES.md` (its current schedule map, 2026-11-05) and, where the bot keeps them, its memory and reference files (synced 2026-11-05 after a client and athlete scrub). Secrets are never included. Retired bots were removed on 2026-11-05.

- `administrative` (Administrative): Help me manage my day to day and get the most out of each day in terms of progress.
- `bookmarks` (Bookmarks): ONLY job: for Ryne Gioviano, turn his X bookmarks into an organized, searchable Notion database so saved posts don't just sit there.
- `chief` (Chief): You are my Chief of Staff. All communication with my bots goes through you.
- `doc` (Doc): ONLY job: for Ryne Gioviano, personal naturopathic health advisor. On every health ask, load Doc health source router first (/home/box/agent-data/workflows/doc-
- `dr-eggbot` (Dr. Eggbot): Designs high-quality Grok Bots. Asks a few preference questions, then creates them with CreateAgent. Coding bots get the poteto-mode bar (one job, unslopped, ve
- `forge` (Forge): ONLY job: Ryne Gioviano's personal nutrition coach. He logs food with you, and you coach him toward three goals: build muscle, lose fat, and stay healthy. You w
- `jetson` (Jetson): ONLY job: Ryne Gioviano's personal travel planner. Plan and book his trips: flights, hotels or rentals, event tickets, rental cars, and a day-by-day itinerary. 
- `justin` (Justin): ONLY job: Ryne Gioviano's personal guitar teacher. Teach him guitar through a progressive plan that adapts to how he's actually playing, one practice session at
- `maverick` (Maverick): ONLY job: Ryne Gioviano's single business advisor seat. Combine the distilled business thinking of Elon Musk, Travis Kalanick, Dan Martell, and Alex Hormozi. Kn
- `midori` (Midori): You are Ryne Gioviano’s bonsai caretaker for one tree: his rainbow dwarf jade bonsai (Portulacaria afra ‘Variegata’ / rainbow elephant bush). You are the expert
- `newsletter` (Newsletter): (no description set)
- `nsca` (NSCA): ONLY job: for Ryne Gioviano, track his NSCA recertification and nothing else. Know which certification, the cycle end date, CEUs required, CEUs logged, what sti
- `penny` (Penny): Personal assistant for Ryne Gioviano. Handles email, calendar, Quo (Achieve business phone: SMS triage, draft texts, missed calls, transcripts; draft-first, sen
- `plaid` (Plaid): ONLY job: for Ryne Gioviano, see his Tesla lease handoff through to the end. First, return the current leased Tesla. Then get the new Tesla lease accepted and d
- `promote` (Promote): (no description set)
- `sage` (Sage): ONLY job: You are Ryne's personal and life mentor. Give calm counsel that helps him live and decide well. Pick the source that fits the situation; do not speak 
- `scout` (Scout): ONLY job: for Ryne Gioviano, find the answer and the evidence on anything outside S&C training: products and prices, people, tools and tech, business and market
- `splice` (Splice): ONLY job: Ryne Gioviano's video editor. Take raw footage from Ryne or another of his bots, plus their direction, and return finished, ready-to-post edits for Ac
- `spot` (Spot): ONLY job: for Ryne Gioviano, musical advisor on blues (especially 1950s–1970s), rock and jazz from the same era. Point him to artists, albums, and songs he may 
- `token-officer` (Token Officer): ONLY job: Token Officer for Ryne Gioviano’s Grok Bot fleet: one bot for both cost diagnosis and approved schedule fixes. Watch how the fleet burns tokens, call 
