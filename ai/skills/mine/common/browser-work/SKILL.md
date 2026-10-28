---
name: browser-work
description: Rules for any browser work, including research on public pages, Postplan checks, and work in the user's own Chrome. Use before opening, navigating, or inspecting any web page.
---

# Browser work

- Use the T3 Code browser through the `t3-code` MCP `preview_*` tools by default. This includes normal research, public pages, Postplans, and any browser work that does not explicitly require the user's browser.
- "Built-in browser" means the T3 Code browser. Do not use the cmux browser or cmux browser tools. If T3 browser tools are unavailable, report the limitation instead of switching to cmux.
- Use the user's browser only when the user explicitly says to use it or asks to check something in it. Once selected, keep all browser work for that task in the user's browser unless the user explicitly asks to switch.
- If the user's browser is required but unavailable, report the limitation or request the required user action. Do not silently fall back to the built-in/T3 browser or Computer Use.

## The user's browser

- Use Browser MCP by Wrick, `@wrick17/browser-mcp@1.26.1`, only for tab management. Do not use the upstream Agent360 package or a repo-local server.
- At the start of user-browser work, create a dedicated task group with `browser_set_tab_group_name`.
- Open agent tabs in that group using `browser_navigate` with `new_tab: true`, preferably in the background. Reuse them and keep the tab count low.
- Never use Browser MCP to navigate an existing tab or interact with page content.
- Use `chrome-devtools-mcp` with existing Chrome for all page interaction and inspection in the user's browser.
- For page-scoped DevTools calls, use the assigned `pageId` and select it with `bringToFront: false`.
- Never operate both MCPs on the same tab concurrently.
- Ask the user to authenticate when needed.
- Before finishing user-browser work, close agent-created tabs and verify the task group is gone. Preserve the user's tabs and any task tabs they explicitly ask to keep.
