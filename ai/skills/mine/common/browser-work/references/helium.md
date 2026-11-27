# Helium test tabs

Test only in Helium. Each agent opens its own background tabs through the `browse` MCP, works only in them, and closes them when its checks end. Follow the browse rules in [browser-work](../SKILL.md#the-users-browser). browse opens agent tabs in the background, so the user's current app keeps focus.

## Open your tab

1. Run `status` and confirm that Helium (`office-helium` on the work machine) is listed with `connected: true`. Otherwise, ask the user to open Helium and enable the browse extension, then wait.
2. When your check starts, call `browse.navigate` inside `execute` without a `tab`, passing the start `url`, the Helium `browser` id, and a `group` of your own: the task slug plus your role, such as `<slug>-px`. Apply the browser-work retry when the first navigation times out.
3. Record the numeric tab id it returns and use it for every later call, following the tab-id rule in browser-work.

Open the tab when the check starts. browse closes idle agent tabs after the user's idle setting, 10 minutes by default. If your tab is gone mid-check, open a new one the same way.

## During each check

- Work only in tabs you opened, including popups they open.
- Restore any persona or experience you switched.
- Stay signed in: logging out and typing credentials belong to the user.

## Close your tabs

When your checks end, including after a failure, list your group with `tabs`. Close your tab ids and any popups in that group with `tabs` action `close`, passing the ids as `tabs`, and skip any tab the user asked to keep. Confirm with `tabs` list that they are gone.

## Proof screenshots

- Every proof screenshot shows the page URL. The capture has no address bar, so overlay `location.href` on the page with `browse.eval` before capturing, then remove it.
- `browse.screenshot` saves to `path` only inside browse's file roots: temp folders and `OPENCODE_BROWSER_FILE_ROOTS`. Use a private subfolder of the session temp folder.
