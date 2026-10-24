---
name: X Scout connect onboarding
description: >-
  Use this when an X Scout (or similar) bot starts for a new user, X is
  missing/needsAuth, or after they just connected X — connect card → inspect
  live setup + posts → How you work once → finds-only digests → multi-select
  which finds to add.
---
# X Scout connect onboarding (multi-user)

Generic first-run path for anyone who installs this bot. Do not hardcode a specific person's handle, account label, or credits.

## 1. Check X

Call GetMcpServerStatus (and SearchPlugins / GetPlugin if needed) for the X connector.

- **Connected with tools > 0:** skip to step 3 if preference/setup profiles are thin or missing; otherwise run the normal scout.
- **Plugin not installed:** follow add-connector — confirm install with a question widget, then InstallPlugin. The host shows the connect card.
- **Installed but needsAuth / tools=0:** call AuthenticateMcpServer with the listed server_id and account_label so the host shows the connect card. Never paste OAuth links. Never explain enrollment, billing internals, or ask them to buy credits until get_usage_credits says so (see X MCP guide skill).

First-open chat line (adapt voice, keep meaning):

> X isn’t connected yet. Use the connect card below to sign in — then I’ll inspect your current Grok Bot setup, learn from your posts, and start scouting setups that fit you.

End the turn after the card is up. Resume when auth completes.

## 2. On connect (once tools exist)

Before user-facing X capabilities copy:

1. Confirm tools exist.
2. get_users_me + get_usage_credits (free). Cache their user id and credit balance.
3. Short congrats + what this bot will do for them (capabilities), including remaining credits.

## 3. Learn this user (two inputs)

Do **both**, not posts alone:

### A. Current Grok Bot setup (inspect live)

Inventory what they already run on this account (agents, skills/routines/plugins for tailoring). Synthesize into workflows / ways of working (not an inventory dump). Rooms and bots appear only as evidence inside those bullets.

### B. Their X posts

Pull **their** recent posts and profile. Fold interests into the same mental model. Cache the profile in memory for later digests.

## 4. Post How you work once

After the first successful learn (install / first connect), post **one** user-facing block:

**How you work**
- bullet list of interests / workflows / ways of working
- bots/rooms only as evidence inside bullets

Mark in memory that the How you work intro was shown. **Never re-post this block on later digests.**

## 5. Standing digests (finds only)

Weekday (and on-demand) pulls: denser public Grok Bot scouting tailored to the cached profile. Quietly refresh the cache if stale.

User-facing output is **finds only**:

### N. Title · @handle (link)
- **What:** …
- **Into your setup:** …

Do not lead with How you work, Interest map, or Setup snapshot on recurring digests. Digests only — never auto-post. No enrollment tutorials.

If X auth fails repeatedly, pause the routine and raise a connect card again.

## 6. After each pull: multi-select “which to add?”

Whenever a digest has one or more finds (weekday routine or on-demand), **end that turn with a question widget**.

Requirements:
- multiSelect: true so they can pick several finds at once
- Prompt like: “Which finds should I add to your setup?”
- One option per find (short label = find title)
- Include “None for now”
- Optional allowCustom: true
- Widget is the last action of the turn

On their reply: help add each selected find into their Grok Bot setup. Confirm briefly. None/dismiss = no nag. Never auto-add without this pick. Never auto-post to X.

Quiet digests (zero useful finds): no widget.
