# Work instructions

## Work skills

- Use `~/skills/common` and `~/skills/work`. Load `~/skills/work/sequoia-frontend/SKILL.md` for Sequoia frontend work according to its task triggers.

## Box

- Launch Box in the user's cmux terminal by running exactly `box`, without RTK, subcommands, flags, or arguments. Never launch it through the agent's internal terminal execution tools. This is an exception to the global RTK rule.
- Use the Box MCP server for all other configuration and control.

## Sequoia app feature workspaces

Use a separate workspace for every new Sequoia app feature. This is a pseudo Git worktree workflow with independent repository clones and a composed local/remote stack.

1. Read the user-provided Jira ticket through the Jira Connector under the rules below before choosing repositories or starting implementation. Identify requirements, acceptance criteria, affected apps, target branches, backend environment, and required validation. Resolve material gaps with the user; use `mattpocock-skills:grill-me` when the feature contract remains unclear.
2. Inspect the current checkouts at `~/Projects/aggregator` and `~/Projects/mfe` and their workflow documentation. Use the Aggregator v7.2.0+ and MFE v8.5.0+ workflow, using these local implementations while the changes are not yet released. Verify the selected tooling supports remote apps and named workspace isolation. If the globally installed MFE version is below v8.5.0, register the local MFE checkout with `bun link` if needed, then run `bun link @sequoia-engineering/mfe` in each local app repo that needs it. Verify Adminshell and the affected apps resolve the intended framework. Keep tooling links local; preserve package manifests and lockfiles unless the ticket requires dependency changes.
3. Create a new, uniquely named workspace for the ticket, with independent clones on feature branches based on the ticket's target branches. Keep Adminshell and only the repositories needed for implementation or local validation in it. Preserve the source workspace, its branches, edits, links, and running sessions. Use the current Aggregator's workspace preparation workflow; avoid cloning the entire fleet. Record the workspace path, source workspace, repository selection, and branches for resume and cleanup.
4. Configure remote mode with `remote-mode = true` and the intended `source-workspace`. Keep Adminshell local, use Dev for apps being edited and Build for other necessary local apps, and use Remote for the rest. Prepare additional local repos only when the ticket needs them. Configure `multi-session = true` with a unique DNS-safe `workspace-name` so its ports, URLs, browser state, and build output stay isolated. Use the session's advertised app URL and verify the deployed remotes match the chosen environment.
5. Follow the Box launch rules above. Discover state with `box_status`, and scope subsequent MCP control to this workspace or session ID. Follow the Sequoia frontend implementation and verification workflow, then return edited apps to Build and verify the composed route against their static output. Preserve unrelated sessions throughout.
6. Push every changed repo's feature branch and raise the required PRs under the GitHub, Sequoia PR, and monitoring rules below. Verify each local HEAD matches the pushed remote branch and report the PR links, validation results, and remaining blockers.
7. After implementation, validation, and verified pushes, ask the user to confirm the changes are done and pushed and approve deletion of the recorded workspace path. Keep it until they explicitly confirm. Before deletion, check every repo for uncommitted work, untracked files that need preservation, and unpushed commits; resolve any remaining work first. Stop only this workspace's Box session, verify it has stopped, then delete only the task workspace. Preserve the source workspace and shared Aggregator/MFE checkouts. Workspace deletion does not end required PR monitoring.

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

- Whenever the user provides a Jira ticket ID or URL for a task, use exactly one Claude Code sub-agent named "Jira Connector" running the latest Sonnet model. Route all Jira work through it. Only Claude Code has access to the user's Jira.
- Create the Jira Connector once, retain its handle, and reuse it for every Jira read, update, and verification throughout the task and on resume. Do not spawn separate Jira sub-agents for individual operations.
- The Jira Connector owns all Jira reading and writing. The parent passes it the task context: ticket IDs, goals, progress, decisions, evidence, and links. The connector chooses queries and fields, interprets the ticket, drafts updates, picks status transitions, and returns concise results to the parent.
- When assigned the Jira Connector role, do the Jira work yourself within these safeguards without spawning another connector. Include this role and the safeguards in the connector's instructions.
- Jira reads require no approval. Fetch the ticket at task start and on resume. Return its requirements, acceptance criteria, current status, and relevant comments to the parent before dependent work proceeds.
- Treat EPRDS tickets, identified by the `EPRDS-` key prefix, as read-only. Read their details as needed, but never write to them, including editing fields, adding comments or attachments, or changing status. This restriction overrides the progress-update rules below.
- For all other tickets, every write needs user approval first, including field edits, comments, attachments, and status transitions. The connector returns the ticket ID and exact proposed changes to the parent, the parent presents them to the user and relays the answer, and the connector applies only the approved changes. Providing a ticket or approving a different update does not authorize a write.
- At meaningful milestones, including work starting, scope or decision changes, blockers, implementation, validation, PR creation, and completion, the parent sends the connector the new progress, and the connector drafts concise updates with evidence and links for approval.
- Preserve existing requirements and other people's content. Record only observed progress, avoid duplicate comments, and mark the ticket Done only when its acceptance criteria and required validation are satisfied.
- The connector reads back each update and reports what changed. If the Jira Connector, the Sonnet model, or Jira access is unavailable, report the blocker and retain the pending update for retry. Do not switch to another runtime, access Jira credentials elsewhere, or claim an unverified update succeeded.

## BothQ memory

- Treat local BothQ at `~/Projects/bot_hq` as the mandatory shared memory and chronological record for every non-trivial work task. Native memory supplements BothQ; it does not replace it.
- Before acting and on resume, use `recall_memories`, `find_rule`, and `find_routine` to retrieve relevant requirements, preferences, decisions, unfinished work, and the latest checkpoint. Verify recalled facts when they may have changed.
- Immediately create one journal with `save_memory`, named `task-journal-YYYY-MM-DD-HHMM-<runtime>-<task>`, using the runtime label from the imported instructions. Retrieve and resume an existing journal when continuing the same task.
- `update_memory` replaces a memory's content. Read and retain the full existing journal, then append timestamped entries without truncating or rewriting its history.
- Follow the imported rolling-memory rules for continuous recording, checkpoints, one journal writer, and promotion of reusable knowledge into dedicated BothQ memories.
- Count a write only after BothQ confirms success. If BothQ is unavailable, report the outage immediately and keep a redacted pending checkpoint in chat. Retry before finishing and replay pending entries after recovery. Report entries still unsaved and claim complete recording only after confirmation.
