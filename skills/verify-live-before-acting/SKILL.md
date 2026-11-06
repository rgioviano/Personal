---
name: Verify live before acting
description: >-
  Use before ranking, proposing, reporting on, or changing any routine, or
  before citing a routine's schedule, status, target room, or last run. Live
  status first; stale copies are never proof.
---
# Verify live before acting

On-disk routine files (`automations/*/automation.json`), TEAM.md, bot memory, and any cached or copied file can be out of date. They are leads, not proof.

## Rule
1. Before you decide anything from a routine's schedule, enabled/paused state, target room, prompt, or last run, get it live: `automation_status` for your own routines, or ask the owning bot for theirs.
2. Quote what you got: schedule (with time zone), enabled or paused, last run time, and where it posts.
3. If you cannot get live status, label the item **UNVERIFIED (stale copy)** and propose nothing for it. Do not count it in savings, rankings, or "done" claims.

## Stop condition
- Live status and a copy disagree: stop, report both side by side, and change nothing until the owner or the user settles it.
- A room or bot id comes only from a stale copy: do not post to it or hand work to it.

## After you verify
If a shared file (TEAM.md, a roster, a fleet doc) is wrong, tell its owner the exact line and the live value, with the date you checked.
