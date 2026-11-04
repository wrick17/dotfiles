---
name: writing
description: Format and wording rules for anything an agent posts or sends for the user, where other people read it. This covers tickets, issues, PRs, and comments on GitHub, Jira, or any tracker; Slack or chat messages; emails; docs and pages in Notion or Google Docs; status, forecast, and release updates; review replies; and calendar or task notes. Use before writing, editing, or proposing any of them.
---

# Writing

Anything you post for the user goes out in their name. Write for a reader who has never seen the agent session. They should get the point, the status, and what's needed from them in about ten seconds. Then they can drill into detail.

## Writer

- Claude Sonnet or Claude Opus writes this text, at the latest version in the live catalog. Use Sonnet for routine posts such as comments, chat messages, emails, and status updates. Use Opus for long docs, reports, and Postplans.
- Any other model, including the main thread and Sol, Terra, or Luna, delegates the draft to a Sonnet or Opus writer under the `delegation` skill. Pass it the facts, the surface, and the audience. Then post the returned text verbatim.
- If neither Sonnet nor Opus is available, such as when both have hit usage limits, a GPT model writes the text under this skill. Tell the user it did. Switch back to Claude once it is available again.
- Commit messages are out of scope; their author writes them under `technical-writing`.

## Shape

1. **Headline first.** Open with one line that carries the point: the outcome, the status, or the ask. Examples: `**Released to production.**`, `**Blocked: waiting on DB access.**`, or an email subject that states the point.
2. **Sections, not paragraphs.** In anything longer than a few lines, use short headings or bold labels, such as *Status*, *What changed*, *Next*, *Risks*, *Evidence*. Leave out any section that has nothing in it.
3. **One fact per bullet.** If a sentence holds three facts joined by commas, split it into three bullets.
4. **Tables for fields.** Use a table for several values with the same shape: dates, owners, checks, versions, or before and after. On a surface with no tables, such as Slack or plain email, use a short `Label: value` list.
5. **Fold the proof.** Put long evidence, such as hashes, logs, or test lists, in a collapsible block where the surface has one, like `<details>` on GitHub. Otherwise put it at the end or behind a link.
6. **Code formatting for identifiers.** Put SHAs, IDs, paths, commands, and versions in code formatting. Shorten a SHA to 7 characters unless the full hash is the evidence.
7. **Fit the surface.** Size the length to where it lands:

| Surface | Length |
|---|---|
| Chat message | a few lines |
| Comment or email | one screen |
| Ticket body or doc | as long as it needs, with headings |

## Wording

- **Plain words.** Write in the reader's terms. Leave out agent-internal vocabulary: model and role names such as Terra, Opus, or Luna, worker or slot counts, task IDs such as `MG0`, orchestration steps, and the agent's own checkpoints. Name the owner as a person or team.
- **The user's voice.** Write as the user would, in first person where the surface expects it. Leave out any mention of agents unless the user asks for it.
- **Absolute times.** Write `4 Nov, 10:17 IST`, not `T+3-5h` relative to an anchor the reader has to look up. Give a range only when the uncertainty matters.
- **Every detail, once.** Keep every number, date, ID, and result. State each one once. Say a caveat such as "estimate, not a commitment" once, next to the value it qualifies.
- **Positive verdicts.** Write `569/569 worker tests passed`. Don't write "no failures were observed in the worker suite".
- **Ask clearly.** Put any request to the reader in its own **Needs from you** line, with the name and the deadline.

## One living update

- When a status or forecast changes, edit the earlier post or reply in its thread. Don't post another near-copy at the top level.
- If you must post again, start the new post with `Supersedes <link>` and edit the old one to point forward.
- Post a new top-level update only for a real milestone: started, blocked, ready for review, shipped.

## Surface markup

- **GitHub:** GitHub-flavored Markdown. Link issues and PRs as `#123`. Use `<details>` for folded proof.
- **Jira:** Through the Jira Connector, use the markup the connector's API takes, whether wiki markup or ADF.
- **Slack and chat:** Use the app's own markup, such as Slack mrkdwn (`*bold*`, `<url|text>`). Its headings and tables don't render. Put the headline in the first line, since that's what previews show. Reply in threads.
- **Email:** A subject that states the point. A one-line opener, then the same headline-and-bullets shape. Sign off as the user.
- **Docs and pages (Notion, Google Docs):** Use the editor's native headings, lists, and tables.
- **Anything else:** Use whatever native structure the surface offers. Plain text with line breaks beats one dense paragraph.

## Before posting

Check the draft against every item. Each one must pass.

- [ ] The headline alone gives the point.
- [ ] No paragraph is longer than three lines. Lists and tables carry the rest.
- [ ] No agent-internal term is left. Every acronym is defined or replaced.
- [ ] Every number, date, and ID from the source is still there.
- [ ] Nothing is repeated, including within the thread.
- [ ] The draft is previewed or rendered once if the tool allows it.
- [ ] `unslop` is applied.

## Example

Before, a single dense block:

> Released to canonical as Worker 839a7f15-… Runtime source 5097672; deployed bundle matched the fixture-verified SHA-256 a1968910…. Canonical test, work, personal and me synthetic save, read, history and replay passed. Profile generations, export inventories, Work import totals and deployment controls were preserved; no export rotated. … Worker tests passed 569/569 and local tests 222/222; an unresolved Vitest teardown warning remains documented.

After:

```markdown
**Released to production (canonical).** Profile selection is live; existing data is unchanged.

**Verified**
- Save, read, history and replay pass for all four profiles (test, work, personal, me)
- Tests: worker 569/569, local 222/222
- Preserved: profile generations, export inventories, Work import totals, deploy controls; no export rotated

**Known issue**
- Vitest teardown warning, unresolved (documented)

<details><summary>Evidence</summary>

| Item | Value |
|---|---|
| Worker version | `839a7f15-900e-409f-b44a-9d3180de530f` |
| Source commit | `5097672` |
| Bundle SHA-256 | `a1968910ca301046ee68c93428acf53d58f3bda58c3dae695bb9066d89631d6b` (matches the fixture-verified build) |
| master / release | `07fb1f4` |
| Details | [import-verification.md](docs/import-verification.md#profile-selection-canonical-verification-2026-11-04) |

</details>
```
