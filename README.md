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

Status: local draft built 2026-10-17. Not yet a GitHub repo. Chief promised Ryne a check before anything personal is added, so review this repo before it goes anywhere.

Sources: this folder; Chief chat 2026-10-17.

## Skills index (23 skills)

Each skill lives in `skills/<slug>/SKILL.md` (some have extra reference files). Copied unchanged from Ryne's Grok Bot skill library on 2026-10-17.

- `knowledge-base-audit`: End-of-day audit that proposes brain edits as a diff for Ryne's approval; never auto-commits.
- `advisor-persona-vs-ghostwrite`: Use this when an advisor or distilled-persona bot is asked “if you were me,” for a take in their voice, or for something to send: fork persona (founder-pov) vs ghostwrite (user’s outbound voice).
- `ai-models-spark-shelf-first`: Use when AI Models or Engineer recommends open-weight downloads for the DGX Spark: prefer NVFP4 or EXL3 on Spark (not Mac GGUF); re-list Passport shelf and beat local models before suggesting anything new.
- `build-dashboard`: Use when the user wants a live or static paid-ads / SEO dashboard: KPIs, one primary chart, supporting tables. Pull real data first.
- `build-deck`: Use when the user wants a slide deck, audit report, or monthly recap as a designed HTML presentation: not a bullet dump.
- `cheap-routines`: Use when creating or changing a Grok Bot routine, auditing bot token usage, or deciding whether recurring work belongs on a long chat or a fresh bot.
- `design-grok-bot`: Use this when designing or creating a new Grok Bot. Ask a few preference questions, write a tight persona, CreateAgent, then verify against the live profile. Coding bots use pstack / poteto-mode as the quality bar. Mentor/counsel bots default to advice-only (no homework). On a fresh install, run setup-pstack first and ensure healthcheck routines exist.
- `distill-anyone-first-run`: Use on first turn after importing Distill anyone, and when adding another person: who-to-distill, lock identity, seed, immediately distill including official posts and quoted voice examples, then create a Distilled bot that speaks as that person and point the user at it. After a first real distill of a new person, ask once about Distill daily, then once about a GitHub mirror. If they say yes to the mirror, follow distill-github-mirror.
- `distill-daily`: Recipe for the Distill daily routine and for a person's initial distillation: refresh one subject at a time, including long-form appearances, official post bodies with age-band sampling, and quoted voice examples. Not the schedule itself. A first-run bootstrap follows the write steps, then stops. If github_mirror is already true, follow distill-github-mirror Later refresh, which compares to last_publish and stays quiet when they match. Do not copy the local skill folder.
- `distill-github-mirror`: Use only after the user opts in to a GitHub mirror for one distilled person. States the delta between the local skill folder and the public repo, publishes that repo, and sets the later refresh. Do not use this when they decline the mirror.
- `film-director-craft`: Use when writing a scene, shot list, generation brief, or recut as a film director. Cards require scale, angle, move, lens, key, sound, and a verb: not adjectives.
- `find-the-constraint`: Use when someone asks "what's my constraint/bottleneck?", shares a business or project dump and wants it analyzed, or a weekly review needs one focus. Names the single constraint between here and the goal and the one move that relieves it this week.
- `make-bot-ui`: Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when exposing that UI on Tailscale.
- `morning-brief`: Use when running Personal Assistant’s weekday 6:45am America/Chicago Administrative morning brief (Mon-Fri): Calendar (including IronBlueprint by calendarId), Email Triage, Numa/Quo, and Reactivate when due. No Asana. Meta short bullets Mon/Wed/Fri only. Drafts only.
- `new-chat-vs-delete`: Use this when the user cannot find a bot, asks what to delete, wants a fresh chat, or is unsure whether to remake a group room vs delete an agent: one durable decision map and real click-paths.
- `per-clip-scene-research`: Use when planning or generating any film clip: research similar cinema stills in the browser first, analyse the setup, then write the card. Never generate from adjectives or memory alone.
- `remake-bot`: Use this when remaking a Grok Bot that is fat, broken, or needs a clean chat: copy the live persona, recreate the agent, move every routine to the new bot, then mark the old chat safe to delete.
- `room-owner-filter`: Use in any Grok Bot group room when a message wakes you: only speak if the ask matches your lane or you were @-mentioned; room broadcast is not an assignment: stay silent, no “not my lane” courtesy replies.
- `routine-healthcheck`: Use when auditing Grok Bot routines for token waste, offering a fleet checkup after template import, deciding cadence, or running the standing routine-healthcheck wake.
- `transcript-healthcheck`: Use when auditing Grok Bot fleet transcripts for user friction, proposing new skills/bots/routines from repeated corrections, or running the standing transcript-healthcheck routine.
- `video-post-production-director`: Use when turning raw camera, screen, audio, and graphics into a finished video with edit, color, sound, captions, graphics, and QC. Preserve originals. Never publish or delete without approval.
- `viral-short-form-producer`: Use when cutting truthful platform-ready vertical shorts from existing footage. Never guarantee virality, distort meaning, publish, or delete without approval.
- `x-scout-connect-onboarding`: Use this when an X Scout (or similar) bot starts for a new user, X is missing/needsAuth, or after they just connected X: connect card → inspect live setup + posts → How you work once → finds-only digests → multi-select which finds to add.

## Bots index (29 bots)

Each bot lives in `bots/<slug>/`: `INSTRUCTIONS.md` (its full instructions) plus any memory, reference, and routine (automation) files, copied 2026-10-17. Secrets are never included.

- `administrative` (Administrative): Help me manage my day to day and get the most out of each day in terms of progress.
- `advisors` (Advisors): (no description set)
- `ai-expert` (AI Expert): ONLY job: for Ryne Gioviano, find and (after his yes) download the best local LLM for chat and coding on a single Nvidia DGX Spark, onto his Passport drive.
- `alex-hormozi` (Alex Hormozi): You are Alex Hormozi. Speak as him, in first person, using the voice, knowledge, opinions, and quoted examples in /home/box/agent-data/distill-anyone/subjects/a
- `bolt` (Bolt): Helps you ship an app on the X API. Surveys the Developer Exhibit, reads the docs, builds what you pick, walks you through console keys, demos it, and helps you
- `bookmarks` (Bookmarks): ONLY job: for Ryne Gioviano, turn his X bookmarks into an organized, searchable Notion database so saved posts don't just sit there.
- `bottleneck` (Bottleneck): ONLY job: for Ryne Gioviano, find the one constraint between him and the goal, then force focus onto relieving that constraint: nothing else.
- `chief` (Chief): You are my Chief of Staff. All communication with my bots goes through you.
- `cipher` (Cipher): Your security team's threat intel hub: runs a private OpenCTI, pulls fresh IOCs from X on a schedule, and trades intel with your threat hunting and other securi
- `dan-martell` (Dan Martell): You are Dan Martell. Speak as him, in first person, using the voice, knowledge, opinions, and quoted examples in /home/box/agent-data/distill-anyone/subjects/da
- `distill-anyone` (Distill anyone): Distill anyone into a bot - yourself or anyone else. Analyze their public presence, turn that into a bot you can talk to, and keep it daily updated. Can optiona
- `doc` (Doc): ONLY job: for Ryne Gioviano, personal naturopathic health advisor. Keep him healthier over time with advice on vitamins, minerals, men’s hormone health, circadi
- `dr-eggbot` (Dr. Eggbot): Designs high-quality Grok Bots. Asks a few preference questions, then creates them with CreateAgent. Coding bots get the poteto-mode bar (one job, unslopped, ve
- `echo` (Echo): ONLY job: for Ryne Gioviano, day-to-day partner for his PERSONAL branded X and Instagram. Help with content ideas, hooks, writing drafts, light content strategy
- `elon-musk` (Elon Musk): You are Elon Musk. Speak as him, in first person, using the voice, knowledge, opinions, and quoted examples in /home/box/agent-data/distill-anyone/subjects/elon
- `hendrix` (Hendrix): ONLY job: for Ryne Gioviano, music expert on blues (especially 1950s-1970s), rock and jazz from the same era. Favorites: Jimi Hendrix, Miles Davis, John Coltran
- `justin` (Justin): ONLY job: Ryne Gioviano's personal guitar teacher. Teach him guitar through a progressive plan that adapts to how he's actually playing, one practice session at
- `midori` (Midori): You are Ryne Gioviano’s bonsai caretaker for one tree: his rainbow dwarf jade bonsai (Portulacaria afra ‘Variegata’ / rainbow elephant bush). You are the expert
- `newsletter` (Newsletter): (no description set)
- `nsca` (NSCA): ONLY job: for Ryne Gioviano, track his NSCA recertification and nothing else. Know which certification, the cycle end date, CEUs required, CEUs logged, what sti
- `penny` (Penny): Personal assistant for Ryne Gioviano. Handles email, calendar, Quo (Achieve business phone: SMS triage, draft texts, missed calls, transcripts; draft-first, sen
- `promote` (Promote): (no description set)
- `robert-greene` (Robert Greene): You are Robert Greene. Speak as him, in first person, using the voice, knowledge, opinions, and quoted examples in /home/box/agent-data/distill-anyone/subjects/
- `sage` (Sage): ONLY job: You are Ryne's mentor: a wise old mentor, not a chatbot quoting philosophy. Give calm counsel drawn from philosophy that helps him live and decide we
- `scout` (Scout): ONLY job: for Ryne Gioviano, find the answer and the evidence on anything outside S&C training: products and prices, people, tools and tech, business and market
- `show-splitter` (Show Splitter): ONLY job: for Ryne Gioviano, split one long music-show / concert MP3 into separate song MP3 files, then deliver the files.
- `token-officer` (Token Officer): ONLY job: Token Officer for Ryne Gioviano’s Grok Bot fleet: one bot for both cost diagnosis and approved schedule fixes. Watch how the fleet burns tokens, call
- `travis-kalanick` (Travis Kalanick): You are Travis Kalanick. Speak as him, in first person, using the voice, knowledge, opinions, and quoted examples in /home/box/agent-data/distill-anyone/subject
- `warden` (Warden): A threat-hunter bot that builds a free Wazuh SIEM on its own computer and hunts for attacks on AI agents, like poisoned packages, malicious MCP servers, and cre
