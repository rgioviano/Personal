---
name: New chat vs delete
description: >-
  Use this when the user cannot find a bot, asks what to delete, wants a fresh
  chat, or is unsure whether to remake a group room vs delete an agent - one
  durable decision map and real click-paths.
---
# New chat vs delete

Use when the user says they cannot find a bot, asks “what can I delete?”, wants a clean slate, or confuses agent chats with group rooms.

## Ground truth (do not invent other paths)

- Each agent has **one** in-app chat. There is no separate “New Chat” control that wipes a transcript while keeping the same agent.
- **Delete agent:** sidebar → right-click that agent’s row → **Delete** (permanent; removes agent + transcript; confirm). Not in Settings. No archive.
- **Hide from sidebar:** per-agent settings can hide the row; the agent still works and is reachable via Cmd-K / Hidden chats. Hiding ≠ delete and ≠ clean transcript.
- **Group / channel rooms:** separate from 1:1 agent chats. Create or edit membership with CreateChannel / UpdateChannel. Deleting a member agent is not how you fix a room; remaking the room or updating members is.
- Per-agent info pane: click the agent’s name in the chat header (or Cmd+Shift+I) for routines, computer preview, members (in groups).

## Decision map

| User want | Do this | Do not |
| --- | --- | --- |
| Clean transcript, same job | **Remake bot** (see [Remake bot](sand-workflow:remake-bot)): new agent, move routines, user Deletes the old row | Promise a “new chat” on the same agent; leave duplicate routines on both |
| Small persona / title fix | UpdateAgent (or tell that bot to update_state profile) | Remake or Delete |
| Bot is retired / duplicate / wrong job forever | User Deletes from sidebar | Remake “just in case” |
| Cannot find a bot in the sidebar | Check Hidden chats / Cmd-K; check for a remake twin with the same name; link [sidebar](grokbot://app/v1/sidebar?agent=<id>&tab=overview) when you know the id | Create another copy before searching |
| Wrong people in a group room | UpdateChannel members or CreateChannel a corrected room | Delete the project-manager agent |
| Noise from a bot they still need | Hide from sidebar or tighten its wake/anti-jobs | Delete without migrating routines |

## What to tell the user

1. Say which case they are in (clean slate / retire / find / fix room) in one sentence.
2. Give the exact next click or the remake plan.
3. If remaking, run Remake bot end-to-end; if deleting, name the **exact** sidebar row and warn Delete is permanent.
4. If two bots share a name after a remake, say which id is the keeper before they Delete.

## Anti-patterns

- Inventing Settings paths or a “New Chat” button.
- Deleting an agent that still owns standing routines without migrating them first.
- Remaking a whole group room when UpdateChannel membership would fix it.
- Creating a third twin because the second remake was hard to find.
