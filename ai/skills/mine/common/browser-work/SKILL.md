---
name: browser-work
description: Rules for any browser work, including research on public pages, Postplan checks, and work in the user's own browser (Helium or Chrome). Use before opening, navigating, or inspecting any web page.
---

# Browser work

- Use the T3 Code browser through the `t3-code` MCP `preview_*` tools by default. This includes normal research, public pages, Postplans, and any browser work that does not explicitly require the user's browser.
- "Built-in browser" means the T3 Code browser. Do not use the cmux browser or cmux browser tools. If T3 browser tools are unavailable, report the limitation instead of switching to cmux.
- Use the user's browser only when the user explicitly says to use it or asks to check something in it. Once selected, keep all browser work for that task in the user's browser unless the user explicitly asks to switch.
- If the user's browser is required but unavailable, report the limitation or request the required user action. Do not silently fall back to the built-in/T3 browser or Computer Use.

## The user's browser

- Helium is the user's browser unless they name Chrome.
- Drive the user's browser through the `browse` MCP. Claude Code and Codex get three tools: `execute`, `status`, and `tabs`. Call every other browse tool, such as `navigate`, `eval`, `screenshot`, and `handoff`, as `browse.<tool>()` inside `execute` (OpenCode exposes them as plain tools).
- Run `status` first and find the wanted browser in `extension.browsers`. If it is missing or its `connected` is false, ask the user to open that browser profile and enable or pair the browse extension, then wait. `nextStep` can be empty in that state.
- When more than one browser is connected, pass the wanted browser's id as `browser` whenever you open a tab.
- When a login, 2FA, captcha, or other person-only step appears, call `handoff` and wait for the user.
- At the start of the task, pick a slug unique to this task, such as the ticket ID plus a short random suffix. Use it as `group` for every agent tab.
- Open each agent tab with `navigate` without a `tab`, passing the `group`. Record the numeric tab id it returns and pass it as `tab` on every later call. Reuse tabs and keep the count low.
- If opening a tab returns its id with a navigation-timeout warning and the tab is still on `about:blank`, navigate that same tab id once more. If that also fails, stop and report it. In browse 0.1.5 on Helium, the first navigation of a new tab can time out. Drop this retry once a Helium smoke test opens a new tab and loads a page on the first try.
- Use only tabs you opened or tabs the user lent you. Leave all other tabs alone.
- Before finishing, close the tab ids you recorded with `tabs` action `close`, passing the ids as `tabs`, skipping any tab the user explicitly asked to keep. Confirm with `tabs` list that they are gone.

### Helium

- On the work machine, Helium is paired with browse as `office-helium`. Elsewhere, read its id from `status`.
- For testing in Helium, read [the Helium test-tab workflow](references/helium.md) before setup or browser calls.

### Chrome

- browse reaches Chrome only after its extension is installed and paired in Chrome. If `status` lists no connected Chrome browser, ask the user to install the extension in Chrome and pair it with `browse pair`. Do not fall back to Helium.
