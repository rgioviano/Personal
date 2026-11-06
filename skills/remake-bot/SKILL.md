---
name: Remake bot
description: >-
  Use this when remaking a Grok Bot that is fat, broken, or needs a clean chat -
  copy the live persona, recreate the agent, move every routine to the new bot,
  then mark the old chat safe to delete.
---
# Remake bot

Use when the user wants a clean chat or a fixed persona for an existing bot (fat CoS, sage redo, hawkin remake, “remake X”), not when they only want a small profile tweak (use UpdateAgent) or a permanent retirement (sidebar Delete only).

There is no archive and no “new chat on same agent.” A remake = new agent + migrated routines + old agent deleted by the user.

## Steps

1. **Lock the source.** Get the old agent’s id (teammates list or `/home/box/agent-data/agents/<id>/`). Read its live `profile.json` (`name`, `description`, `title` if set). Do not invent a thinner persona unless the user asked for a rewrite as part of the remake.

2. **Inventory routines.** List `/home/box/agent-data/agents/<old-id>/automations/` (or the agent’s Current routines / memory of standing jobs). For each routine capture: name, schedule or trigger, and the full prompt text. If the folder is empty, ask the old bot (SendToAgent, priority true) to list its enabled routines with those fields.

3. **Create the replacement.** CreateAgent with the same `name` and full `description` (whole persona, not a one-liner). If the remake includes a persona fix the user already approved, bake that into `description` before create. Read back `/home/box/agent-data/agents/<new-id>/profile.json` and confirm it matches.

4. **Move routines (you cannot write another bot’s routines yourself).** Immediately SendToAgent the **new** bot (priority true) with an explicit create list: for each routine, `update_state` target routine action create with exact name, prompt, and schedule/trigger, plus enabled true. Tell it to reply when all exist. If SendToAgent fails, paste that one-line create list into chat for the user to send the new bot.

5. **Optional memory / skills.** If the old bot held job-critical profile/log facts the new one needs, SendToAgent the new bot to write those facts into its own memory. Do not copy secrets or credentials through chat.

6. **Hand off and retire the old one.** Tell the user: new bot name + id, which routines were requested on it, and that the **old** chat is safe to delete once the new bot confirms routines are live. Delete is user-only: sidebar → right-click the **old** agent’s row → Delete (permanent; confirm). Do not create a second remake while the first is unfinished.

7. **Do not** delete the old agent yourself (no delete tool). Do not leave both running the same schedule without telling the user which to delete. Do not recreate shareable templates unless asked.

## Success

New agent live with verified profile; every inventoried routine requested on the new bot; user told which old row to Delete.
