# Work instructions

## Work skills

- Use `~/skills/common` and `~/skills/work`. Load `~/skills/work/sequoia-frontend/SKILL.md` for Sequoia frontend work according to its task triggers.

## Box

- Launch Box in the user's cmux terminal by running exactly `box`, without RTK, subcommands, flags, or arguments. Never launch it through the agent's internal terminal execution tools. This is an exception to the global RTK rule.
- Use the Box MCP server for all other configuration and control.

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

## PR checks and monitoring

- Monitor every PR raised for the user until all required checks pass and all the PRs are merged. Continue monitoring after reruns, new commits, and user intervention.
- Inspect failed check logs. For worker or infrastructure failures, rerun the failed checks up to three times per check before reporting a persistent failure to the user.
- Semgrep is optional. Do not report Semgrep failures or treat them as blockers to completion.
- Sonar is mandatory. If Sonar fails, inspect the run logs and extract the Sonar dashboard status link, generally starting with `https://sonar-qa.sequoia-development.com/dashboard`. Give the user the link and wait for them to handle the issue in the dashboard and confirm it is resolved. Do not attempt to fix Sonar findings yourself. If the logs contain no dashboard link, report that along with the run link.
- In T3 Code, use `watch_pull_request` when available and resume monitoring when notified. Follow the retry and Sonar rules on each update until every PR meets the completion condition above.

## Jira task progress

- Whenever the user provides a Jira ticket ID or URL for a task, use exactly one Claude Code sub-agent named "Jira Connector" running the latest available Haiku model. Route all Jira operations through it. Only Claude Code has access to the user's Jira. Resolve the model from the live provider catalog rather than pinning a version.
- Create the Jira Connector once, retain its handle, and reuse it for every Jira read, update, and verification throughout the task and on resume. Do not spawn separate Jira sub-agents for individual operations. This required name overrides the general agent naming convention.
- The parent agent owns all task reasoning, ticket interpretation, planning, implementation, validation, and decisions. It chooses Jira queries and fields, drafts exact write payloads, obtains required user approval, and evaluates the returned results.
- The Jira Connector acts only as the API layer. Give it explicit operations, ticket IDs, read parameters or approved write payloads, and the safeguards below. It executes those operations and readbacks, then returns requested data, API outcomes, and errors. It must not make task decisions, draft or revise ticket content, choose status transitions, or perform substantive task work. Return ambiguous requests or API failures to the parent for a decision.
- When assigned the Jira Connector role, execute the parent's API instructions within these safeguards without spawning another connector. Include this role boundary in the connector's instructions.
- Jira reads require no approval. Fetch the ticket at task start and on resume. Read its requirements, acceptance criteria, current status, and relevant comments before proceeding with dependent work.
- Treat EPRDS tickets, identified by the `EPRDS-` key prefix, as read-only. Read their details as needed, but never write to them, including editing fields, adding comments or attachments, or changing status. This restriction overrides the progress-update rules below and must be included in the Jira Connector's instructions.
- For all other tickets, before any write, present the ticket ID and exact proposed changes, ask the user for approval, and wait for their answer. This applies to every write, including field edits, comments, attachments, and status transitions. Approval covers only the proposed writes; providing a ticket or approving a different update does not authorize them. Include this approval requirement in the Jira Connector's instructions.
- At meaningful milestones, including work starting, scope or decision changes, blockers, implementation, validation, PR creation, and completion, prepare concise progress updates with evidence and links. Apply them only after the user approves the proposed writes.
- Preserve existing requirements and other people's content. Record only observed progress, avoid duplicate comments, and mark the ticket Done only when its acceptance criteria and required validation are satisfied.
- Read back each update through the Jira Connector and report what changed. If the Jira Connector, the latest Haiku model, or Jira access is unavailable, report the blocker and retain the pending update for retry. Do not substitute another model, switch to another runtime, access Jira credentials elsewhere, or claim an unverified update succeeded.

## BothQ memory

- Treat local BothQ at `~/Projects/bot_hq` as the mandatory shared memory and chronological record for every non-trivial work task. Native memory supplements BothQ; it does not replace it.
- Before acting and on resume, use `recall_memories`, `find_rule`, and `find_routine` to retrieve relevant requirements, preferences, decisions, unfinished work, and the latest checkpoint. Verify recalled facts when they may have changed.
- Immediately create one journal with `save_memory`, named `task-journal-YYYY-MM-DD-HHMM-<runtime>-<task>`, using the runtime label from the imported instructions. Retrieve and resume an existing journal when continuing the same task.
- `update_memory` replaces a memory's content. Read and retain the full existing journal, then append timestamped entries without truncating or rewriting its history.
- Follow the imported rolling-memory rules for continuous recording, checkpoints, one journal writer, and promotion of reusable knowledge into dedicated BothQ memories.
- Count a write only after BothQ confirms success. If BothQ is unavailable, report the outage immediately and keep a redacted pending checkpoint in chat. Retry before finishing and replay pending entries after recovery. Report entries still unsaved and claim complete recording only after confirmation.
