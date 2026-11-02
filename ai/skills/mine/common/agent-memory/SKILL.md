---
name: agent-memory
description: Agent Memory (MCP connection `agent_memory`) is the primary memory and task journal for work and personal tasks. Use at the start of every non-trivial task, on resume, when writing a journal entry, checkpoint, or memory, and for explicit remember, forget, or update requests.
---

# Agent Memory

- Agent Memory, MCP connection `agent_memory` at `https://memory.wrick17.com/mcp`, is the primary memory and chronological record for every non-trivial task. Native Claude Code or Codex memory is the backup.
- Pick the profile once per task and pass it as `profile` on every call that has no `memory_id`:
  - `work`: repos owned by `Sequoia-Engineering`, `Sequoia-US`, or `pratyush-poddar_seq`, and work-setup tasks outside any repo.
  - `personal`: every other repo, and every task in a personal setup.
  - With `memory_id`, omit `profile`; the id routes to its owning profile.
  - Passing only `repo` misroutes when the remote uses an SSH host alias such as `git@personal:`; the explicit `profile` avoids that.
- Write to `me` only when the user explicitly asks, with `profile: "me"` and `company_free: true`, after checking the content is company-free.
- Before acting and on resume, call `recall_memories` with the profile and a task `keyword` to retrieve requirements, decisions, unfinished work, and the latest checkpoint. Recall rules with `type: "feedback"`, preferences with `type: "user"`, and routines with `type: "procedural"`. Read full content and revisions with `get_memory` (`memory_id`, optional `history: {limit}`). Verify recalled facts when they may have changed.
- Immediately create one journal with `save_memory`: the profile, `name` `task-journal-YYYY-MM-DD-HHMM-<runtime>-<task>` using the runtime label from the imported instructions, `type: "project"`, `kind: "journal"`, a one-line `description`, the initial checkpoint as `content`, and `request_id: "<journal name>#create"`. Keep the returned `memory_id`.
- To continue a task, find its journal with `recall_memories` (the profile, `keyword` = journal name or task, `kinds: ["journal"]`) and resume it by `memory_id`. Migrated BothQ records and journals keep their IDs in Work.
- Append each timestamped entry with `append_memory` (`memory_id`, `content`, `request_id: "<journal name>#<entry number>"`). Replace journal content with `save_memory` (`memory_id`, `content`, `expected_revision`, a new stable `request_id`) only after reading and retaining the full existing journal; on `revision_conflict`, reread first.
- Save reusable knowledge and explicit remember requests as dedicated memories with `save_memory`; retire them with `retire: true` on a forget request.
- Give every write its own stable `request_id`. After an uncertain result, retry with the same `request_id` and the identical payload.
- Count a write only after Agent Memory confirms success. If Agent Memory is unavailable, report the outage immediately, keep a redacted pending checkpoint in chat with its intended `request_id`, and write the entry to native memory when the runtime allows. Retry before finishing; after recovery, replay pending entries to Agent Memory with the same `request_id`. Report entries still unsaved and claim complete recording only after confirmation.
- Native memory may also hold a supplementary copy. Agent Memory stays the source of truth: recall from it first and save every durable entry there.
- BothQ (`~/Projects/bot_hq`, connection `bothq`) is a read-only legacy archive, reached only through its separate inspection context. Every memory and journal write goes to Agent Memory; an outage falls back to native memory, never to BothQ.
