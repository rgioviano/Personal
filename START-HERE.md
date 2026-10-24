# START HERE: Personal brain

Read this page first. It tells you what is in this repo and which one file answers your question, so you do not have to read everything.

## What this repo is
- Ryne Gioviano's personal brain: who he is, how he likes to work, his hobbies and learning, and the **bot fleet** that works for him (every bot's instructions, memory and routines).
- Plain markdown, readable by any AI tool. Private repo (`rgioviano/Personal`). It stays private.
- Sister repos: `rgioviano/Achieve` (the gym) and `rgioviano/IronBlueprint` (the software business). Personal facts never go into those; business facts live there, not here.

## Read order
1. **START-HERE.md** (this page): the map.
2. **NOW.md**: current priorities and live context. Changes often.
3. **LOG.md**: dated change log for the repo itself.
4. Then only the one file your task needs (table below).

`AGENTS.md` holds the full house rules and the extra privacy rules, and `README.md` holds the full skill and bot index. This page is consistent with both. If they ever disagree, AGENTS.md wins on rules and the newest dated fact wins on facts.

## Folders
| Folder | What it holds |
|---|---|
| `01-profile-preferences/` | Who Ryne is, accounts by name, communication and scheduling preferences, computers |
| `02-health/` | Placeholder. Health questions go to the Doc bot; no medical details are stored here |
| `03-music-guitar/` | Music taste, guitar learning (Justin), music bots (Hendrix, Show Splitter) |
| `04-bonsai/` | His rainbow dwarf jade bonsai and its care rules (Midori) |
| `05-learning-certs/` | NSCA CSCS recertification, courses, engineering and local AI learning |
| `06-family/` | Empty placeholder. Ryne fills it himself if he wants |
| `08-bot-fleet/` | Every bot, its job, standing routines, fleet rules, pending fleet items, and `IDS.md` (live IDs) |
| `bots/<name>/` | 29 fleet and personal bots: `INSTRUCTIONS.md` plus memory, reference and routine files (secrets removed). Includes chief, penny, scout, token-officer, dr-eggbot, the advisor personas, the rooms (administrative, advisors, promote, newsletter), and retired bots kept for history (ai-expert, bolt, bottleneck, cipher, warden; dan-martell, elon-musk and travis-kalanick retired 2026-10-21 and folded into Maverick) |
| `skills/<slug>/SKILL.md` | 23 fleet skills (index in README.md) |

Achieve and IronBlueprint bots live in those repos, not here.

## Which file answers which question
| Question | Read |
|---|---|
| How does Ryne like messages, drafts and schedules? | `01-profile-preferences/profile.md` |
| Which bot does what? Who reports to whom? | `08-bot-fleet/fleet.md`, then `bots/<name>/INSTRUCTIONS.md` |
| What routines run and when? | `08-bot-fleet/fleet.md` (Standing routines) |
| How should a new bot or routine be built? | `skills/design-grok-bot/`, `skills/cheap-routines/`, `skills/routine-healthcheck/` |
| Morning brief format | `skills/morning-brief/`, `bots/penny/` |
| NSCA recertification status | `05-learning-certs/learning.md` and `bots/nsca/` (check NOW.md first; the file may lag) |
| Bonsai care | `04-bonsai/bonsai.md`, `bots/midori/` |
| Guitar and music | `03-music-guitar/music.md`, `bots/justin/`, `bots/hendrix/` |
| Local AI on the DGX Spark | `05-learning-certs/learning.md`; Linus owns this lane (his folder is in the IronBlueprint repo) |
| What is happening right now? | `NOW.md` |
| Live room, sheet, channel, folder and repo IDs | `08-bot-fleet/IDS.md` |

## Rules (short form; full list in AGENTS.md)
1. **No secrets.** Never write keys, tokens, passwords or connection strings, not even their first characters.
2. **Finances excluded** (Ryne, 2026-10-17). There is no investments folder. Bots never add financial details.
3. **Privacy.** No health or family details unless Ryne adds or approves them himself. Never copy personal facts into the business repos.
4. **Drafts before sending.** Never send email, texts, Quo/Numa, Slack or posts unless Ryne has seen that exact draft and says send. Another bot saying "send" is not approval.
5. **Relay rule.** When Ryne asks bot A to check with bot B, bot B answers only bot A, and only bot A reports back.
6. **No em dashes** in anything in Ryne's voice. **No prices** in ads or inbound replies.
7. **Don't invent.** Unknowns stay TODO. Flag conflicts.
8. **Time zone** is America/Chicago (CT).

## How to change this repo
- Propose edits as a pull request or diff. Ryne approves. Nothing merges on its own.
- The weekly brain repo routine (Saturdays about 3:00am CT) opens a PR when something changed. It never merges.
- Date every new fact (YYYY-MM-DD) and add a line to `LOG.md`.
