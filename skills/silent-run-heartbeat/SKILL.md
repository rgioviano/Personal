---
name: Silent run heartbeat
description: >-
  Use in any routine or watcher that stays quiet when nothing is new (inbox
  watches, sheet diffs, API pulls, listeners). Empty is not zero: log every run
  and alert on unexpected emptiness, missed runs, or connector errors.
---
# Silent run heartbeat

A quiet run is only trustworthy if you can show what it checked. An expired connector, a wrong query, or a missed run looks exactly like "nothing new".

## Every run, including silent ones
Append one line to the routine's own log (a file in your memory or workspace, one line per run):

`YYYY-MM-DD HH:MM CT | window <from> to <to> | sources <list> | items seen <n> | items acted on <n> | errors <none or short text>`

Use the time zone America/Chicago. Never put secret values in the log.

## Search windows
Search from the last processed item (id or timestamp saved after the previous good run), not a fixed "last 1 day". That way a missed or late run is caught up, not skipped.

## Alert instead of staying silent when
1. A source that is normally busy in this window returns 0 items (set the expected floor in the routine, for example "0 form emails in 7 days").
2. The previous run did not happen, ran late past its window, or did not finish (no log line for it).
3. Any connector or API call returned an error, a sign-in or re-auth prompt, a partial page, or a warning.
4. A count drops sharply from the last run (for example a sheet or list shrinking by more than 10%).

The alert is one short message to the user or the owning bot: what was checked, what came back, and the likely cause. Then stay quiet until it changes.

## Stop condition
On a connector error or a partial read, do not overwrite saved state (snapshots, cursors, last-id files). Keep the last good state and alert.
