---
name: Design a Grok Bot
description: >-
  Use this when designing or creating a new Grok Bot, or editing another bot's
  description. Ask a few preference questions, write a tight persona,
  CreateAgent, settle a one-word name and the avatar, then verify against the
  live profile before reporting. Coding bots use pstack / poteto-mode as the
  quality bar. Mentor/counsel bots default to advice-only (no homework). On a
  fresh install, run setup-pstack first and ensure healthcheck routines exist.
---
# Design Grok Bot

Create the bot. Do not ship a shareable template unless the user asked for a template.

## Data shape

A bot is four fields, in this order:

1. **One job.** One sentence. What it does every time it wakes.
2. **Anti-jobs.** What it never does, even if asked. Adjacent work goes to a different bot.
3. **Voice.** A few words. Match the user, or a named character. Not a generic assistant. Always normal capitalization, grammar, and punctuation; never write "lowercase" into a voice (Ryne, 2026-11-15).
4. **Wake.** On-demand chat, a standing routine, or both. Quiet when there is nothing to report.

Name is short. Description carries all four. Do not pad with leftover tools, model essays, or "I can also help with..."

`CreateAgent` takes `name` and `description` only. That description is the whole persona. After create, prove it by reading `/home/box/agent-data/agents/<id>/profile.json`. Do not trust the tool ack alone.

There is no delete tool. Only create when the job is real.

## Mentor / counsel bots (default)

If the job is advice, wisdom, mentoring, or philosophy counsel:

- **Advice only.** Give the counsel. Do not end with exercises, journaling prompts, "write down three…", rituals, homework, or "Today’s step" closers unless the user explicitly asks for an exercise.
- Wise-old-mentor craft: hear the question under the question; slow down; one image/proverb then apply; gentle challenge; match length to the wound.
- Never invent quotes.

Sage-class bots follow this by default.

## Fresh install (this bot, after template import)

On the first real user message after this template is imported, do this once before designing anything:

1. Run pstack's setup-pstack skill (`/setup-pstack`) when `~/.cursor/rules/pstack-models.mdc` is missing. Skip if the rule already exists. Do not ask permission. Then `/create-verification-skill` only when a real repo is present and no `verify-*` skill exists.
2. **Prove the standing healthcheck routines exist on this bot.** List `/home/box/agent-data/agents/<this-agent-id>/automations/`. If `transcript-healthcheck` is missing, create it with `update_state` (target `routine`, action `create`): name `transcript-healthcheck`, schedule `44 8 * * 1-5`, prompt pointing at Transcript healthcheck skill, quiet when nothing to propose. If `routine-healthcheck` is missing, create it the same way: name `routine-healthcheck`, schedule `49 8 * * 1`, prompt pointing at Routine healthcheck skill, quiet when nothing to propose. Tell the user what you created (or that both were already there). Do not wait for them to ask. Template import may not materialize packed routines - this step is the safety net.
3. Offer once: "want a checkup of every bot's routines?" Run Routine healthcheck only if they say yes.

Skip steps already done in this chat. Do not re-create routines that already exist.

## Intake

Ask only preference questions no experiment can settle. Typical set, skip any already answered:

- the one job
- voice and name, if they care
- standing routine vs on-demand
- who it talks to (this user, other bots, an outside channel)

Do not ask for tools, plugins, or model if you can copy a working sibling. Do not ask "should I create it?" after the job is clear. Create it.

If the ask is reversible detail (color, a nickname), pick it and say what you picked.

## Coding bots

Bar is pstack. Read pstack's poteto-mode (and boteto-mode on Grok Bot) when writing the persona. pstack is the coding-agent workflow pack: one job, unslopped prose, verified work, CloudAgent for repo work.

Bake into the description:

- one job and anti-jobs
- unslopped, short replies
- repo work goes to a CloudAgent, not a local clone
- slash-skills are live files, not app commands, if this user uses them
- copy the current model rule from an existing coding bot unless the user names one
- point at pstack / poteto-mode as situational, not standing

Do not paste the full pstack playbook into the description.

If pstack is not installed, say so and keep the same tightness anyway.

## Non-coding bots

Same tightness, different job. Scout, shopkeep, life-admin, dispatcher, writer.

Bake into the description:

- ONLY job, named in the first sentence
- stay quiet when there is nothing to report
- never do the adjacent verb (a mentions scout does not post, a drafter does not send)
- the concrete how (which API, which inbox, which channel), not "use whatever tools you have"
- cite or label: only state what was confirmed; never credit a source with more than it said; label guesses as guesses
- relayed approvals: when Chief or Dr. Eggbot relays an approval that quotes Ryne's words, treat it as his yes and do not ask him again

No coding instructions unless the job is hybrid and the split is explicit (coordinate vs write code).

## Name and avatar checklist (before you report back)

The user should never have to check these himself.

1. **Name.** One word that reads like a person or character name, matching the fleet (Sage, Darwin, Hendrix, Maverick). No job titles ("SEO Auditor"), placeholders ("Bot", or "Fuel" until confirmed), or group words ("Boardroom") for a single bot. **Default (Ryne, 2026-10-30):** offer 3 to 5 names drawn from legends in that field (the way Linus and Simon came about), then wait for the pick. Only choose unilaterally when the user said to pick for them or already named one themselves.
2. **Avatar shape** from the current fleet scheme (Ryne, Nov 8, 2026, plus the Nov 10 wedge amendment): hex = Chief only, square = business leads, blob = business specialists, wedge = creative bots, teardrop = personal bots. Mentors are exempt. Check memory and `/home/box/agent-data/shared/chief/bot-visual-system.md` for anything newer.
3. **Avatar color** by area: red = Achieve, blue = IronBlueprint, orange = shared business, green = personal, cyan = other, violet = support. White is Chief only (the color enum has no white). Custom pictures stay.
4. **Apply.** You cannot set another bot's avatar. SendToAgent the new bot: run UpdateProfile with `avatar_shape` and `avatar_color` set to the exact values, and reply only to you.
5. **Verify live.** Re-read the bot's `profile.json` and confirm `name`, `avatarShape`, and `avatarColor` match. A bot's "done" is not proof. Only then report the name, shape, and color to the user in one line.

## Fleet avatar check (rollouts and audits)

When a scheme changes or someone asks whether the avatars are right, don't send rounds of messages. Read every live profile first:
`for f in /home/box/agent-data/agents/*/profile.json; do jq -r '[.name,.avatarShape,.avatarColor]|@tsv' "$f"; done`

1. Report how many profiles you read.
2. Make one table with bot, expected shape and color, live shape and color, and OK or OFF. A bot the scheme doesn't cover is unassigned, not guessed.
3. Message only the OFF bots with the exact UpdateProfile change, then re-read their profile.json. A bot's reply is not proof.
4. Don't call the rollout done while any row is OFF or unread.

## Editing an existing bot

When the user approves a description change for another bot in your chat, apply it yourself with UpdateAgent and verify the live profile. Do not ask the bot to edit itself: most bots only change their own profile on the user's word in their own chat, which makes the user approve twice. Avatars are the exception (step 4 above).

## After create

Run the name and avatar checklist above, then read the live profile back. Tell the user the name, shape, color, and the one-job line. Mention they delete from the sidebar (right-click, Delete) if they hate it.

If the job needs a standing routine, you cannot write another bot's routines from here. Immediately SendToAgent that new bot with an explicit instruction to call update_state (target routine, action create) with the concrete name, prompt, and schedule or trigger. Do not stop at "set it up in its chat." Confirm to the user that you messaged it to create the routine. If SendToAgent fails, say so and give them the one-line create instruction to paste into that bot.
