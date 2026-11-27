# Helium test tabs

Run every Helium test in dedicated slot tabs on the user's second-monitor window. Drive them through the `browse` MCP, following the browse rules in [browser-work](../SKILL.md#the-users-browser). browse opens agent tabs in the background and never takes focus from the user's current app.

## Find the test window

At setup, re-check the current display layout and note the second monitor's bounds. Example only, from 2026-11-27: an external 2560x1440 display above the built-in one, with the Helium window near screenX -465, screenY -1440.

## Set up the tabs once

The orchestrator does this once per task, before any agent drives a tab. `<slug>` is the task's unique slug from browser-work.

1. Run `status` and confirm that Helium (`office-helium` on the work machine) is listed with `connected: true`. Otherwise, ask the user to open Helium and enable the browse extension, then wait.
2. Open 2-3 slot tabs. For each one, call `browse.navigate` inside `execute` without a `tab`, passing a start `url` such as the app home, the Helium `browser` id, `group` `<slug>-test`, and `keepOpen: true`, so idle cleanup does not close a slot mid-task. Apply the browser-work retry when the first navigation times out. Record the numeric tab id it returns as slot 1, slot 2, and slot 3.
3. In each slot tab, read `screenX` and `screenY` with `browse.eval`. If any slot sits outside the second monitor's bounds, set a distinct title in each misplaced slot with `browse.eval`, such as `document.title = "<slug>-test-N"`. Ask the user once to move the tabs with those titles to the second-monitor window. Re-check every slot after the user confirms.

Give each agent its slot number and tab id.

## Drive a tab

- Pass your slot's tab id as `tab` on every `execute` call. Use `browse.navigate`, `browse.eval`, `browse.screenshot`, and the `page` APIs only on that tab.
- If your slot's tab is missing from `tabs` list, stop and report it to the orchestrator. The orchestrator reopens it with step 2, re-checks its window with step 3, and sends the new tab id.

## Parallel agents

Each agent claims one slot before it touches a tab. Lock directories live in the orchestrator's session temp folder, which the orchestrator names in every agent's brief.

- Claim with `mkdir <dir>/<slug>.browser.lock.N`; the first agent whose `mkdir` succeeds owns slot N. Try the next slot when it fails.
- Release with `rmdir <dir>/<slug>.browser.lock.N` when done, including after a failure.
- Break a lock only when it is older than 30 minutes.

## After each check

- Leave the tab on a neutral page, such as the app home.
- Restore any persona or experience you switched.
- Stay signed in: logging out and typing credentials belong to the user.

## Finish the task

Popups a slot opened inherit `keepOpen` and survive closing the slot. The orchestrator lists the `<slug>-test` group with `tabs`, then closes the recorded slot ids and any popup ids in that group with `tabs` action `close`, passing the ids as `tabs`, skipping any tab the user asked to keep. It confirms with `tabs` list that they are gone.

## Proof screenshots

- Every proof screenshot shows the page URL. The capture has no address bar, so overlay `location.href` on the page with `browse.eval` before capturing, then remove it.
- `browse.screenshot` saves to `path` only inside browse's file roots: temp folders and `OPENCODE_BROWSER_FILE_ROOTS`. Use a private subfolder of the session temp folder.
