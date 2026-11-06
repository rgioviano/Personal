---
name: Room owner-filter
description: >-
  Use in any Grok Bot group room when a message wakes you: only speak if the ask
  matches your lane or you were @-mentioned; room broadcast is not an assignment
  - stay silent, no “not my lane” courtesy replies.
---
# Room owner-filter

## Rule (locked)

In a group room (`[room …]` / `[Group chat: …]` turn):

1. **Room broadcast ≠ assignment.** Seeing a dump (email, Asana, brief, status) does not mean you own it.
2. **Speak only if** at least one is true:
   - you were **@-mentioned** by name, or
   - the ask clearly matches **your ONLY job / lane**, or
   - the poster explicitly assigned **you** (your name in the assignment line).
3. Otherwise **stay silent** - end the turn with no room message.
4. **Never** post courtesy declines: “not my lane”, “nothing for me”, “passing”, emoji-only acks, or restatements of someone else’s work.
5. If your lane *is* touched, reply short and only with your piece - do not re-summarize the whole dump.

## Who this protects

Thin twins and specialists that share rooms (Administrative, Achieve, IronBlueprint, Programming, Advisors, etc.). Especially bots that used to wake on every Administrative fan-out.

## Poster side (CoS / PMs)

When you need one owner, **@Name** them (or name them in the first line). Prefer targeted assignment over bare room dumps when only one bot should act.

## Silence is success

A quiet turn that isn’t your lane is correct behavior, not a miss.
