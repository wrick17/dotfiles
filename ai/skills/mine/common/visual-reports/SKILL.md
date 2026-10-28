---
name: visual-reports
description: Rules for rendered visuals, diagrams, HTML reports, and Postplan uploads. Use when summarizing multi-part work, presenting plans, architecture, or multi-part findings, or creating any HTML report or Postplan.
---

# Visual reports

## Rendered visuals

- Use rendered visuals (`html_render`) for summaries of multi-part work, plans, architecture, and multi-part findings. Use Markdown tables and short lists for small tasks and routine updates.
- When a visual is useful, use the visualization tools exposed by the live `t3-code` MCP catalog. With the current tools, build self-contained HTML, check it with `html_preview`, and present it inline with `html_render` before the final reply. Rendered HTML must fit its container width with no horizontal scrolling; wrap long text and code, and stack or reflow wide tables and diagrams.
- Use diagrams to explain relationships, structure, and flows, and charts to show data, comparisons, and trends. Choose the simplest format that makes the information easy to understand and visualize; use tables or interactive explanations when they fit better. Give every visual report, inline visual, and Postplan a clean, simple, polished design suited to its content: generous whitespace, few colors, clear labels, readable typography, balanced spacing, and accessible contrast. Cut decoration and any element that does not help the reader. Make the visual carry the information; keep accompanying prose brief and add only what the visual does not already say. Follow the Diagrams rules when applicable.
- If the visualization tools are unavailable, state the limitation and provide the information in the clearest available format. Honor any format explicitly requested by the user.

## Diagrams

- Choose the diagram format or visualization pattern that best fits the scenario. Archify is optional; use `$archify` when its diagram workflow fits the task, and use other formats or patterns when they fit better.
- For every HTML report, HTML document, or Postplan, assess whether an architecture diagram would help. When it would, include it in the artifact using the chosen format.
- When using Archify, follow its validation and delivery checks. Honor any visualization format explicitly requested by the user.

## Postplans and HTML reports

- When a substantial report or implementation plan needs an artifact, create dark-mode HTML in a temporary directory and upload it with `node ~/Projects/personal/postplan/scripts/upload.mjs <file>.html --folder work` for Work tasks or `--folder personal` for Personal tasks. Choose the folder from the actual task context, regardless of the active machine profile. Always pass the folder for new uploads and updates, including `--draft <ID>` updates. Use lowercase flag values as required by the [Postplan docs](https://github.com/wrick17/postplan#check-publish-and-update); the official CLI has no `--folder` option.
- Constrain the content of every HTML report and Postplan to a max-width of 1400px, centered in the page.
- For every Postplan, load and apply `~/skills/third-party/common/technical-writing/SKILL.md` and `~/skills/third-party/common/unslop/SKILL.md`.
- Every code block in a plan or Postplan must have syntax highlighting for its language. Specify the language on Markdown code fences and render actual syntax highlighting in HTML. Verify that highlighting is visible and readable in the final rendered page.
- Make each Postplan aesthetically polished and easy for developers to understand. Structure it as a coherent story or a step-by-step how-to guide, whichever fits the reader's goal. Include relevant code snippets and concrete examples wherever possible.
- Before uploading, inspect the rendered HTML in the browser chosen under the `browser-work` skill, T3 Code by default. Check visual hierarchy, typography, spacing, contrast, overflow, and code-block readability at desktop and narrow widths.
- Do not use `file://` links.
