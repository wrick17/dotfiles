---
name: visual-reports
description: Rules for rendered visuals, diagrams, HTML reports, and Postplan uploads. Use when summarizing multi-part work, presenting plans, architecture, or multi-part findings, or creating any HTML report or Postplan.
---

# Visual reports

## Rendered visuals

- Use rendered visuals (`html_render`) when the output is complex or carries a lot of information, such as summaries of multi-part work, plans, architecture, and multi-part findings. Use text, Markdown tables, and short lists for simpler output and routine updates.
- When a visual is useful, use the visualization tools exposed by the live `t3-code` MCP catalog. With the current tools, build self-contained HTML, check it with `html_preview`, and present it inline with `html_render` before the final reply. Rendered HTML must fit its container width with no horizontal scrolling; wrap long text and code, and stack or reflow wide tables and diagrams.
- Use diagrams to explain relationships, structure, and flows, and charts to show data, comparisons, and trends. Choose the simplest format that makes the information easy to understand and visualize; use tables or interactive explanations when they fit better. Give every visual report, inline visual, and Postplan a clean, simple, polished design suited to its content: generous whitespace, few colors, clear labels, readable typography, balanced spacing, and accessible contrast. Cut decoration and any element that does not help the reader. Make the visual carry the information; keep accompanying prose brief and add only what the visual does not already say. Follow the Diagrams rules when applicable.
- If the visualization tools are unavailable, state the limitation and provide the information in the clearest available format. Honor any format explicitly requested by the user.

## Diagrams

- Choose the diagram format or visualization pattern that best fits the scenario. Archify is optional; use `$archify` when its diagram workflow fits the task, and use other formats or patterns when they fit better.
- For every HTML report, HTML document, or Postplan, assess whether an architecture diagram would help. When it would, include it in the artifact using the chosen format.
- When using Archify, follow its validation and delivery checks. Honor any visualization format explicitly requested by the user.
- In HTML reports and Postplans, build diagrams with inline SVG or HTML/CSS that use the theme's CSS variables. Keep them readable at 390px wide, stacking parts on narrow screens. Route every line and arrow clear of the labels, and confirm that in the preview.

## Postplans and HTML reports

- When a substantial report or implementation plan needs an artifact, create HTML in a temporary directory and upload it with `node ~/Projects/personal/postplan/scripts/upload.mjs <file>.html --folder work` for Work tasks or `--folder personal` for Personal tasks. Choose the folder from the actual task context, regardless of the active machine profile. To revise a Postplan, re-upload with `--draft <ID>` so its URL stays the same. Always pass the folder, for new uploads and `--draft` updates alike. Use lowercase flag values as required by the [Postplan docs](https://github.com/wrick17/postplan#check-publish-and-update); the official CLI has no `--folder` option.
- Read the Postplan API key only from the global `POSTPLAN_API_KEY` environment variable. Never take it from `~/.postplan`, key files, repository config, CLI flags, chat, or memory, and never copy it anywhere else. If the variable is unset, stop and ask the user to set it.
- Share Postplan links only with the user, in chat. Never put a Postplan link or a mention of a Postplan in Jira or Confluence.
- The session scratchpad can be cleared mid-task. If the HTML source disappears, recover it from the `html_render` attachment copy (`~/.t3/userdata/attachments/*-html.html`) or re-fetch the live Postplan page.

### Audience and structure

- A Postplan is technical and reads well for non-engineers too: engineers, PMs, EMs, and QA all use it. Keep the technical substance: the approach, the main components and how they interact, key decisions with their reasons, risks, and trade-offs. Explain it in plain language and define each piece of jargon once.
- Pitch the depth between a light overview and a full spec. An engineer can judge the plan from it; a non-engineer can follow every section. Cut padding and repetition, but leave no gap the reader must fill in.
- Keep file paths out of the main text, as the Details rule below describes. Leave `file:line` evidence, runtime internals, and full engineering detail to the Confluence page or a separate detailed report.
- Structure each Postplan as a coherent story or a step-by-step how-to guide, whichever fits the reader's goal, with concrete examples.
- Open each section with a one-line plain takeaway, then bullets, a small table, or steps. Use inline code only where the exact identifier matters. Put paths, SHAs, error codes, and hook names in a muted "Details" line or a collapsed `<details>` block.

### Layout, color, and code

- Constrain the content of every HTML report and Postplan to a max-width of 1400px, centered in the page. Prose, lists, and callouts span the same full content width as tables and diagrams.
- Use one small semantic palette, defined as CSS variables in both themes: green for outcomes and safe paths, amber for risks and fallbacks, blue for decisions. Mark Takeaway, Key decision, and Risk with left-border callouts in those colors. Color only one or two key facts per section. Keep evidence tags (Observed, Inference, Assumption) small and muted.
- Show code as diagram pseudo-code in place of large code blocks: box diagrams for data shapes, flowcharts for decisions, step diagrams for processes, and color-coded tables. Any code that remains is short pseudo code of about 6 to 10 lines, highlighted for its language and readable in the rendered page; specify the language on Markdown code fences.
- Make every HTML report and Postplan follow the system light/dark theme automatically. Declare `<meta name="color-scheme" content="light dark">`, define colors as CSS custom properties on `:root` for light mode, override them under `@media (prefers-color-scheme: dark)`, and give `body` an explicit background. Code highlighting, diagrams, and charts must switch with the theme without a reload; scripts that draw with theme colors read `matchMedia("(prefers-color-scheme: dark)")` and redraw on its `change` event. Never hard-code a single theme.
- For every Postplan, load and apply `~/skills/third-party/common/technical-writing/SKILL.md` and `~/skills/third-party/common/unslop/SKILL.md`. Where they conflict with the audience rules above, such as on writing real paths, the audience rules win.
- Before uploading, inspect the rendered HTML in the browser chosen under the `browser-work` skill, T3 Code by default. Check visual hierarchy, typography, spacing, contrast, overflow, diagram labels, and code readability at desktop and 390px widths, in both light and dark system themes.
- Do not use `file://` links.
