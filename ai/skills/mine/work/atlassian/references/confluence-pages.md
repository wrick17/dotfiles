# Confluence pages

Rules for creating and editing Confluence pages through the Atlassian plugin. Every write still needs user approval under the main skill.

## Structure

- Start a plan page with a header table (owner, Jira epic link, status, date), then a TL;DR info panel.
- Then use these sections in order: Problem statement, Implementation plan, QA plan, Rollout plan, Blast radius and impact, Open questions, and a collapsed Evidence appendix.
- The page carries the detailed engineering version. A Postplan, when one exists, is the user's lighter technical overview, not a copy of the page.

## Location

- Create the page under the same parent as the user's related design docs. Find them by searching the user's existing pages on the topic, or the docs linked from the related epics.
- If no related docs exist, use the user's personal space and tell the user.
- Link the page on the Jira epic as a web link.

## Style

- Follow the report readability rules in the `visual-reports` skill: a takeaway first in each section, inline code only for exact identifiers, no large code blocks, tables and diagrams in place of code.
- Use info, note, and warning panels for the TL;DR, key decisions, and risks.

## Page width

- Set the page width to "wide". Full width reads too wide; fixed reads too narrow.
- The plugin's page-update width setting takes `narrow`, `wide`, or `max`; use `wide`.
- The plugin cannot set content properties (`content-appearance-*`).
- Sequoia site fact: the content column on a wide page is 1800px.

## Tables

- Set table layout `center` and table `width` to the content column width.
- Size columns by content, computed with a small script rather than by eye:
  1. Weight each column as 0.6 × average cell text length + 0.4 × longest cell length, using the header length as a floor.
  2. Scale the weights to the content column width.
  3. Raise each column to at least 120px and at least the width of its longest header word, then scale the other columns down to keep the total.
  4. Round to integers that sum exactly to the content column width.
- Send `colwidth` in the text form the plugin accepts; a list value was silently dropped. Setting the first row's widths applies them to the whole column.
- Remove leftover large `width` values from earlier layouts. A 4000px width left from a full-width page made tables overflow after the switch to wide.

## Diagrams and images

- Sequoia site fact: no draw.io, Gliffy, or Mermaid macro is available through this plugin. Embed diagrams as PNG images.
- PNG at 2x is the default. SVG can change the fonts of HTML/CSS diagrams when Confluence renders it.
- Export each diagram alone on a blank page with headless Chromium, using Playwright from a repo that already has it installed, with no changes to that repo. Use the light theme, a white background, 2x device scale, about 1200px CSS width, and crop to the diagram with about 24px padding. Keep the export files in the session's temp folder.
- Upload with `createConfluenceAttachment` (inputs `contentId`, `localFilePath`). It returns a curl command to run locally. Write its auth token to a temp file, pass it from there, and delete the file after the upload. Never print or keep the token.
- Embed each image as an ADF `mediaSingle` with `layout: "center"`, `width: <content column px>` (1800 on a wide Sequoia page), and `widthType: "pixel"`. Give the media node the image's real pixel `width` and `height`.
- Pixel width is the only setting that sizes reliably. `width: 100` as a percentage is stored as 680px, `layout: "full-width"` is stored as 960px, and Confluence does not shrink an oversized pixel width, so it overflows.
- Place each image directly above the table or section it illustrates, with a caption and alt text.

## Plugin limits

- The plugin cannot delete Jira web links. Ask the user to remove them by hand.
- Figures have no IDs. To move or resize one, remove it and insert it again, then confirm no empty figure remains.
- Do a dry run first whenever the tool offers one.

## After every save

- Read back the stored structure: tables, figures, widths, and page version. Report any mismatch with what was sent.
- Ask the user to check the rendered page. The agent cannot view rendered Confluence pages, because they need the user's login.
