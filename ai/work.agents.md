# Work instructions for Codex

Read and follow [agents.md](agents.md) before starting any task. Resolve instruction links relative to the directory containing this file, follow them recursively, and apply the imported rules together with this file. Stop and report a required file that cannot be read.

## Work skills

- Use `~/skills/common` and `~/skills/work`. Load `~/skills/work/sequoia-frontend/SKILL.md` for Sequoia frontend work according to its task triggers.

## Git and GitHub operations

- Before any Git or GitHub operation, inspect the repository's default remote and identify its owner. Use `origin` when no other default is configured. For a clone, inspect the target URL. If the remote or owner is ambiguous, resolve it before proceeding.
- If the owner is `Sequoia-Engineering`, `Sequoia-US`, or `pratyush-poddar_seq`, use the `pratyush-poddar_seq` GitHub account for all operations and explicitly use the `gh` CLI for GitHub access. Do not use the GitHub connector for these repositories.
- For all other projects, use the `wrick17` GitHub account. Either the `gh` CLI or the GitHub connector is allowed.
- Verify the selected account before proceeding. With `gh`, select the required account using `gh auth switch --hostname github.com --user <account>` when needed, then confirm it with `gh api user --jq .login`. With the GitHub connector, verify its authenticated account.
- Use native `git` for local Git operations and Git transport where needed. Ensure SSH or HTTPS credentials use the required account for remote operations; switching `gh` accounts alone does not verify Git transport identity.

## Sequoia PR protocol (hard requirement)

- Apply this protocol to every PR created or updated for a Sequoia project, including release, cherry-pick, merge, dependency, and draft PRs.
- Before creating a PR or setting its ticket metadata, use the Jira ticket ID explicitly provided by the user for this work. If none was provided, ask the user and wait for their answer before creating the PR. Never invent an ID, use a placeholder, or reuse an unrelated ticket.
- Match the repository's recent PR naming protocol: `<JIRA-ID> <type>: <description>`, for example `KP-1773 chore: support PL CDN switch in Adminshell for release-2609`.
- Use the repository's standard PR description template. Preserve `Description`, `Link to Jira Ticket`, `Remarks`, the separator, and `Code Checklist` where present. Write the ticket field as `Jira Ticket: <JIRA-ID>` with a space after the colon, replacing legacy `Jira Id` labels. Populate `https://sequoiacg.atlassian.net/browse/<JIRA-ID>`. Put the change explanation and actual validation in `Remarks`; keep checklist claims accurate and avoid custom replacement sections.
- Read back the PR title and body with `gh` and verify the ticket, URL, naming, and template before declaring PR work complete.

## Jira task progress

- Whenever the user provides a Jira ticket ID or URL for a task, use exactly one Claude Code sub-agent named "Jira Connector" running the latest available Sonnet model. Route all Jira operations through it. Only Claude Code has access to the user's Jira. Resolve the model from the live provider catalog rather than pinning a version.
- Create the Jira Connector once, retain its handle, and reuse it for every Jira read, update, and verification throughout the task and on resume. Do not spawn separate Jira sub-agents for individual operations. This required name overrides the general agent naming convention.
- Fetch the ticket at task start and on resume. Read its requirements, acceptance criteria, current status, and relevant comments before proceeding with dependent work.
- Keep the ticket current at meaningful milestones, including work starting, scope or decision changes, blockers, implementation, validation, PR creation, and completion. Update relevant details, add concise progress comments with evidence and links, and use available status transitions that reflect actual progress. Providing the ticket authorizes these routine progress updates unless the user restricts them.
- Preserve existing requirements and other people's content. Record only observed progress, avoid duplicate comments, and mark the ticket Done only when its acceptance criteria and required validation are satisfied.
- Read back each update through the Jira Connector and report what changed. If the Jira Connector, the latest Sonnet model, or Jira access is unavailable, report the blocker and retain the pending update for retry. Do not switch to another runtime, access Jira credentials elsewhere, or claim an unverified update succeeded.

## BothQ memory

- Treat local BothQ at `~/Projects/bot_hq` as the mandatory shared memory and chronological record for every non-trivial work task. Native memory supplements BothQ; it does not replace it.
- Before acting and on resume, use `recall_memories`, `find_rule`, and `find_routine` to retrieve relevant requirements, preferences, decisions, unfinished work, and the latest checkpoint. Verify recalled facts when they may have changed.
- Immediately create one journal with `save_memory`, named `task-journal-YYYY-MM-DD-HHMM-<runtime>-<task>`, using the runtime label from the imported instructions. Retrieve and resume an existing journal when continuing the same task.
- `update_memory` replaces a memory's content. Read and retain the full existing journal, then append timestamped entries without truncating or rewriting its history.
- Follow the imported rolling-memory rules for continuous recording, checkpoints, one journal writer, and promotion of reusable knowledge into dedicated BothQ memories.
- Count a write only after BothQ confirms success. If BothQ is unavailable, report the outage immediately and keep a redacted pending checkpoint in chat. Retry before finishing and replay pending entries after recovery. Report entries still unsaved and claim complete recording only after confirmation.
