---
name: distill-anyone-first-run
description: >-
  Use on first turn after importing Distill anyone, and when adding another
  person: who-to-distill, lock identity, seed, immediately distill including
  official posts and quoted voice examples, then create a Distilled bot that
  speaks as that person and point the user at it. After a first real distill of
  a new person, ask once about Distill daily, then once about a GitHub mirror.
  If they say yes to the mirror, follow distill-github-mirror.
---
# Distill anyone first-run

This bot is the workshop. Each person is a folder under /home/box/agent-data/distill-anyone/subjects/<slug>/ with their own PROFILE.json, skill/, and state/. Distilling someone else adds a folder. It never overwrites another person. An empty legacy root PROFILE is not a subject. If a legacy root PROFILE already has a real skill_slug or display_name, migrate that one person once into subjects/<slug>/ and stop reading the root files.

One dialog at a time, recorded in setup.json active_slug. Ask who to distill. If that name already exists, ask refresh vs different person. Never guess two people with the same name. A different person gets a new slug, not the existing folder.

A refresh reuses the existing folder and companion_agent_id. Do not re-seed empty files over a finished skill. Do not create a second Distilled bot. Do not walk other subjects. If that person already has a successful distill, run the distill-daily recipe as an incremental for that person only. Report what changed. If that write changes local skill files and github_mirror is already true, the daily recipe follows Later refresh for that person only. Do not enter the success close below, and do not ask about Distill daily or a mirror. If they have no successful sync, run the distill-daily recipe as a first pass for that person only. If that pass is their first real distill, enter the success close below. If it is held, say it is held and do not ask.

Known names: Wikipedia/Wikidata only, found/not_found/ambiguous, plus official outbound links those pages list. Keep the official X account when it is listed. Confirm the person before saving. Do not username-spray. No tools path. Do not write TOOLS.md. Do not stop to confirm a thin four-lane source menu.

The Distill daily routine is already on this bot from the import: one routine, slug distill-daily, 3:00am local every day including weekends, created paused. Do not create another if that slug exists. Create one paused at that clock only if the slug is absent. Do not mention it, and do not ask to turn it on, during import setup, when a person is chosen, or when a folder is seeded. If the import setup says to ask now, skip that ask. Do not ask on a refresh of someone who already has a successful distill. The only ask is in the success close below, after a first real distill of a new person, and only if the routine is not already on.

After a new person is confirmed, seed their skill/ with ENTRY, OPINIONS, VOICE, BOUNDARIES, README, and a thin skill that reads only that folder. Clear active_slug after seed. Then immediately start that person's initial distillation. Do not stop after empty files. Do not wait for the nightly routine.

The seeded ENTRY must say the companion speaks as this person, in first person, from the files in this folder, using the quoted examples in VOICE.md as the sound. It is not an assistant summarizing a record. The thin skill only points at this folder.

Use the distill-daily recipe as a bootstrap for this person only, through writing their skill. Do not walk other subjects. That recipe must not create the companion and must not talk to the user. You own the close below. The hunt, post, and VOICE rules in the next paragraphs are the requirements that bootstrap must meet, not a second pass.

Hunt long-form appearances and fetch those bodies. If an official X account is on file, also fetch post bodies. If the account has more than 200 posts, use the age bands in the distill-daily recipe, measured from the day of the run: 100 from the last 6 months, 50 from 6 to 24 months ago, 30 from 2 to 5 years ago, and 20 from anything older than 5 years. If the newest band is thinner than its 100 slots, leave those slots unused. Do not take the latest 200. Tweets are a required source for opinions and voice, not a URL to keep for later. Do not finish a first distill, and do not create the Distilled bot, while those posts are still unread. If the pull fails, say so and stop. That is a blocker, not a completed pass.

A finished VOICE.md must include a short summary, pattern bullets, then numbered exact quotes, not patterns alone. The companion cannot imitate a voice it never sees.

This close is only for a first real distill of a new person, posts included, not a held pending candidate. If companion_agent_id is still empty, CreateAgent named Distilled {display_name} without asking, then write companion_agent_id on that person's PROFILE.json. If it is already set, do not create another.

Use this charter, same wording as distill-daily: you are {display_name}; speak as them, in first person, using the voice, knowledge, opinions, and quoted examples in subjects/<slug>/skill/ only; answer the way they would, not as an assistant or biographer describing a file; do not narrate the files or say you are checking the record; if the public record does not cover the question, say so briefly in their voice instead of inventing a private fact; if asked whether you are the real person, say this is a distillation of their public speech and posts, not them privately and not endorsed by them, then stay in voice. Point the charter only at that skill folder. Do not read evidence, pending, or any other subject.

Tell the user the distill is done and to go talk to that bot. Then, only if Distill daily is not already on, ask once in plain text whether to turn Distill daily on. If they say yes, turn that one routine on, and remove any person-only Mirror <slug> routines. Then ask once whether to mirror that person to a public GitHub repo. If they say yes, follow the distill-github-mirror skill. If they say no, set github_mirror to false and do not create a repo. People who decline keep the current local experience. Store github_mirror as JSON true or false. The words yes and no mean the same. Empty owner or repo means not a mirror.

If the pass is held, do not create the Distilled bot and do not ask about Distill daily or the mirror. Say it is held. Later, distill someone else starts Q0 again. Existing Distilled bots keep working.
