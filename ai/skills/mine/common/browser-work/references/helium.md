# Helium test tabs

Run every Helium test in dedicated tabs on the user's second-monitor window. Use the `devtools` MCP to drive the tabs and keep focus on the user's current app after setup.

## Find the test window

At setup, re-check the current display layout and Helium window bounds. Use those bounds to identify the second-monitor window. Example only, from 2026-11-27: an external 2560x1440 display above the built-in one, with the window near screenX -465, screenY -1440.

## Known failures

These were observed on the user's machine; each one steals focus or lands in the wrong window, which is why the method below exists:

- `new_page`, even with `background: true`, opens in whichever Helium window the user used last.
- `select_page` with `bringToFront: true`, `window.open`, and AppleScript `make new tab` bring Helium to the front.
- AppleScript `move tab` between windows leaves a blank tab and loses the original.

## Set up the tabs once

The orchestrator does this once per task, before any agent drives a tab:

1. Record the frontmost app through System Events.
2. Open 2-3 tabs in the second-monitor window with AppleScript `tell window <n> to make new tab`. This is the single accepted focus steal.
3. Restore the recorded app immediately through System Events, including if tab creation fails.
4. Find the new tabs' `pageId`s with `list_pages`, then mark each tab with `window.name` through `evaluate_script`: `<task>-test`, `<task>-test-2`, `<task>-test-3`.

During setup, record each marked tab's `pageId` for its slot and give each agent the mapping for its DevTools connection.

## Drive a tab

- After setup, use only `navigate_page`, `evaluate_script`, and `take_screenshot`, passing your slot's recorded `pageId` on every call.
- If the assigned tab is missing or cannot be identified, stop and report it.
- `window.name` survives same-site navigations. Restore a cleared `window.name` on the confirmed tab.

## Parallel agents

Each agent claims one slot before it touches a tab. Slot 1 is `<task>-test`, slot N is `<task>-test-N`. Lock directories live in the orchestrator's session temp folder, which the orchestrator names in every agent's brief.

- Claim with `mkdir <dir>/browser.lock.N`; the first agent whose `mkdir` succeeds owns slot N. Try the next slot when it fails.
- Release with `rmdir <dir>/browser.lock.N` when done, including after a failure.
- Break a lock only when it is older than 30 minutes.

## After each check

- Leave the tab on a neutral page, such as the app home.
- Restore any persona or experience you switched.
- Stay signed in: logging out and typing credentials belong to the user.

## Proof screenshots

- Every proof screenshot shows the page URL. The capture has no address bar, so overlay `location.href` on the page with `evaluate_script` before capturing, then remove it.
- `take_screenshot` saves files only inside the `devtools` MCP's workspace roots. Choose a path inside one.
