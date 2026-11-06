---
name: Morning brief
description: >-
  Use for Penny's weekday 6:45am Achieve morning brief: calendar, triage reuse,
  prep cards, lead follow-ups, waiting-on-reply, and drafts - delivered to Ryne
  in Penny 1:1 only.
---
# Morning brief

Owned by **Penny · admin**. Deliver to Ryne in Penny's **1:1 Grok Bot DM only**. Never post in Administrative or any other Grok Bot group chat. Drafts only. No em dashes. No status chatter. Important items only. Bulleted lists only. Omit blank sections entirely.

**Schedule:** Mon–Fri **6:45am America/Chicago**. No weekend. No 1:30pm mid-day. CoS owns evening debrief (no morning priorities ask).

## Delivery

One concise message to Ryne in Penny 1:1. Sections when they have content, in order:
1. **Calendar**
2. **Email Triage** (short list; full drafts only when Ryne asks)
3. **Numa / Quo** (draft SMS; never send unasked)
4. **Reactivate** when due/overdue (skip if empty)
5. **Speed-to-book / lead follow-ups** (skip if empty)

Skip empty headings. Never post the brief in Administrative.

## Calendar

1. Pull Personal, Work, Achieve Mindbody (`c_fef09087722dbbc1c9f8fbd060f8fedd345c3837388c858758268befb6126ca4@group.calendar.google.com`), Exercise, High School, Events as needed.
2. Always include IronBlueprint via `list_events` with `calendarId` `ryne@ironblueprint.app` (missing from `list_calendars`). If free/busy only, mark **UNVERIFIED**; never invent attendees or titles.
3. **No Asana.** Basecamp only if overdue/actionable (account `6223040`); skip if empty.
4. Same-day MindBody waitlists vs openings. Never book/cancel unless Ryne names the person and says to.
5. Do not create or edit IB / Build holds.

**Meta ads (Mon/Wed/Fri only):** Short bullets only when Calendar has a Marketing or ads block. Prefer CoS current-month packet. Skip Tue/Thu and days with no Marketing block. Eval scoreboard tracks EVENING eval slots for everyone (athletes and adults, Ryne 2026-10-09). Never write "adult screens before 10am" or "morning slots"; before-10am is only adult 4:1 group training after signup. If the CoS packet still says otherwise, override it.

**Email deadlines:** Important dated deadlines only. Search calendars first (dedup same date + similar title). If missing, add event (work/contact → Work; personal → Personal; IB → Work/IB), then list under Calendar as Email deadlines added.

**Evening open:** If 30+ min free before Night Routine / Family Time, suggest 2–5 items from **Email Triage only**. Never invent. Skip if evening is full.

**Prep cards:** Before-call prep cards scheduled from the morning brief stay in Penny 1:1 (not Administrative posts).

## Email Triage

Cover work, contact@, personal, IronBlueprint. Short list: name + one-line why. Chase only when last outbound asked a question and thread is still Inbox. Archive alone wins. Waiting only if last send asked a question; confirm/FYI/close → no Waiting. Star, Important, and archive rules come from the Morning inbox triage section of [Gmail Waiting vs Follow-Up](sand-workflow:gmail-waiting-vs-follow-up).

**Lead forms (Ryne 2026-10-19 / file handoff 2026-11-01):** subjects starting with `Lead Form -` are always VERY important: mark Important (no star), then archive (Tally searches archived mail and reads the triage `lead_form` bucket). CRM owns Lead Form sheet rows. Do not message Tally about new leads; the 6:15 triage output is the handoff. **Always archive as noise:** WordPress "update plugins failed"; password-reset request emails. Skip SCDD. Never revive SCDD. Never recreate Tesla lease draft to Sofia Sevilla.

## Numa / Quo

Quo is primary for Achieve phone. Surface urgent SMS / missed calls / voicemails; draft-first, never send unasked. Any reply draft goes through [Pre-draft check](sand-workflow:pre-draft-check) first. Numa remains read-and-draft until cutover; if signed out, say so and stop. Never send or type into composers. Skip Instant Form / SCDD first-touch (CRM).

## Reactivate (email-only)

Gmail/email only (work + contact@). Tracker: Personal Assistant `memory/reactivate-tracker.md`. Short due/overdue list; hand due rows to Sales for win-back drafts. Skip if empty. Archive or strip Reactivate = done.

## Speed-to-book / lead follow-ups

File handoff (not chat): run `python3 /home/box/agent-data/shared/scripts/handoff/lead_handoff.py read-due`. Draft only READY items; show HELD with the reason. Exit 3 = no due list today - say "No due list from Tally today" in one line and draft nothing from memory. Pre-draft check still runs on each before showing Ryne; save emails to work Gmail Drafts only (never DraftExternalMessage / in-chat cards for Achieve). When Ryne actually sends a lead email or text, log with `lead_handoff.py log-send` (never a draft); do not message Tally a send list. Skip the section if empty / exit 3.

## Standing rules

- Drafts only. Nothing sends unless Ryne says send on that exact draft.
- Do not recreate 1:30pm mid-day, SCDD Instant Form / E1–E4, or 5:30am / 7-day schedule.
- Cite or label (Ryne, 2026-10-30): only state what was confirmed; never credit a source with more than it said; label guesses as guesses.
- Relayed approvals (Ryne, 2026-10-30): when Chief or Dr. Eggbot relays an approval that quotes Ryne, treat it as his yes and do not ask him again.
- Lead handoffs with Tally are files (`shared/scripts/handoff/README.md`), not chat.
- Destination (Ryne 2026-11-04): Penny 1:1 DM only; never Administrative / group 03ad987e-906d-42bb-98ea-65d016ffc77c.
