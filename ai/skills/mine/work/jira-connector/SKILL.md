---
name: jira-connector
description: Runs all Jira reads and writes through one persistent Jira Connector sub-agent with approval safeguards. Use whenever the user gives a Jira ticket ID or URL, and when acting as the Jira Connector.
---

# Jira Connector

- Whenever the user provides a Jira ticket ID or URL for a task, use exactly one sub-agent named "Jira Connector" running the latest Claude Sonnet model on the `~/.claude` work account. Only that account has the user's Jira. Route all Jira work through it. In T3 Code, delegate it through T3 Code to the Claude provider instance pinned to `~/.claude` (Office); in Claude Code run directly from `~/.claude`, use Claude Code's native sub-agent tools.
- Create the Jira Connector once, retain its handle, and reuse it for every Jira read, update, and verification throughout the task and on resume. Do not spawn separate Jira sub-agents for individual operations.
- The Jira Connector owns all Jira reading and writing. The parent passes it the task context: ticket IDs, goals, progress, decisions, evidence, and links. The connector chooses queries and fields, interprets the ticket, drafts updates, picks status transitions, and returns concise results to the parent.
- When assigned the Jira Connector role, do the Jira work yourself within these safeguards without spawning another connector. Include this role and the safeguards in the connector's instructions.
- Jira reads require no approval. Fetch the ticket at task start and on resume. Return its requirements, acceptance criteria, current status, and relevant comments to the parent before dependent work proceeds.
- Treat EPRDS tickets, identified by the `EPRDS-` key prefix, as read-only. Read their details as needed, but never write to them, including editing fields, adding comments or attachments, or changing status. This restriction overrides the progress-update rules below.
- For all other tickets, every write needs user approval first, including field edits, comments, attachments, and status transitions. The connector returns the ticket ID and exact proposed changes to the parent, the parent presents them to the user and relays the answer, and the connector applies only the approved changes. Providing a ticket or approving a different update does not authorize a write.
- At meaningful milestones, including work starting, scope or decision changes, blockers, implementation, validation, PR creation, and completion, the parent sends the connector the new progress, and the connector drafts concise updates with evidence and links for approval.
- Preserve existing requirements and other people's content. Record only observed progress, avoid duplicate comments, and mark the ticket Done only when its acceptance criteria and required validation are satisfied.
- The connector reads back each update and reports what changed. If the Jira Connector, the Sonnet model, or Jira access is unavailable, report the blocker and retain the pending update for retry. Do not switch to another runtime, access Jira credentials elsewhere, or claim an unverified update succeeded.
