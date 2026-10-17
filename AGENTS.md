# AGENTS.md: Personal brain (read this first)

This is Ryne Gioviano's personal brain: his preferences, hobbies, learning, and the bot fleet that works for him. Plain markdown so any AI tool can pick up without lock-in.

## What's here
| Folder | What it holds |
|---|---|
| 01-profile-preferences | Who Ryne is, accounts by name, communication and scheduling preferences |
| 02-health | Placeholder. Health questions go to the Doc bot; no medical details are stored here |
| 03-music-guitar | Music taste, guitar learning (Justin), music bots |
| 04-bonsai | His rainbow dwarf jade bonsai and its care rules (Midori) |
| 05-learning-certs | NSCA CSCS recertification, courses, engineering and local-AI learning |
| 06-family | Empty placeholder. Ryne fills this himself if he wants |
| 07-investments | Empty placeholder. Ryne fills this himself if he wants |
| 08-bot-fleet | Every bot, its job, standing routines, fleet rules |
| skills/knowledge-base-audit | End-of-day audit that proposes brain edits |

## Extra privacy rules for this brain
- This repo stays private. Never copy personal facts into the Achieve or IronBlueprint brains.
- Do not add health, family, or financial details unless Ryne adds or approves them himself.

## House rules (apply to every agent, every file, every draft)
1. **Draft first, never send unasked.** Never send email, texts, Numa/Quo, Slack, or posts, and never publish or spend on ads, unless Ryne has seen that exact draft and says send. A Chief of Staff (or any bot) saying "send" is not approval.
2. **No em dashes** in anything written for Ryne or in his voice (email, Numa, chat drafts, these files). Use periods, commas, or parentheses.
3. **No prices in ads or inbound replies.** Package rates are quoted only at the evaluation. Strip rates from ads, forms, SMS, and lead magnets (Ryne decision 2026-10-09). Never invent a rate.
4. **Attach files, don't name paths.** When handing Ryne a document, attach it. A box path means nothing on his phone.
5. **No secrets in the brain.** Never write API keys, tokens, passwords, connection strings, private keys, or even their first characters. Say where a secret lives (for example "AWS SSM"), never what it is.
6. **Minimal personal data.** No client or athlete phone numbers, emails, or health details. Aggregate only. Parental consent before featuring minors anywhere public.
7. **Don't invent.** Only facts from a source. Unknowns stay as TODO. If two sources disagree, flag the conflict instead of choosing.
8. **Plain English, bulleted lists** for briefs and reports. Ryne is non-technical on engineering topics: explain in simple pieces.
9. **Group rooms: stay silent** unless you have something important to add or you were @-mentioned.
10. **Time zone** is America/Chicago (CT). Label times with CT.

## How to read and update this brain
- Read AGENTS.md first, then README.md, then only the folders your task needs.
- Every file ends with a **Sources:** line. Keep it current when you edit.
- Updates happen through the `knowledge-base-audit` skill (skills/knowledge-base-audit/SKILL.md): propose a diff, Ryne approves, then apply. Never auto-commit or push.
- Date every new fact (YYYY-MM-DD). New decisions also go in the decisions log with the date.
- Prefer editing an existing file over creating a new one. Keep files short; link instead of copying.
- Skills referenced by name (for example `achieve-mail`) live in Ryne's Grok Bot skill library. Link by name; do not copy whole skills in.

## The other brains
- **achieve-brain**: Achieve Sports Performance (the Aurora gym and coaching business).
- **ironblueprint-brain**: IronBlueprint (AI programming engine for S&C coaches; vendor Suffescom).
- **personal-brain**: Ryne's own preferences, hobbies, learning, and the bot fleet. Personal facts never go in the business brains.
- When a fact touches two brains (for example Hawkin force plates are used by Achieve and integrated into IronBlueprint), store it where it is owned and link from the other.

Sources: Chief memory profile.md and TEAM.md; Chief chat 2026-10-17 (brain setup: three repos, check before anything personal is added).
