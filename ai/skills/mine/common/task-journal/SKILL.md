---
name: task-journal
description: Procedure for the rolling task journal and checkpoints. Use at the start of any non-trivial task, on resume, and before delegation, handoff, compaction, idle, interruption, or the final response.
---

# Task journal

- Keep one rolling task journal per task. Record requirements, corrections, assumptions, decisions and reasons, actions, results, failures, evidence pointers, open questions, and next steps as work progresses.
- Preserve the full journal history when appending timestamped entries. Mark superseded decisions in a new entry with their replacements and reasons. Record concise decision rationale, not private chain-of-thought.
- Before delegation, handoff, compaction, idle, interruption, or the final response, append a checkpoint with the original requirements, current status, completed changes, decisions, verification, failures, remaining work, and an exact resume sentence.
- Keep one main journal writer. Workers return concise events and evidence to that writer.
- Promote reusable rules, preferences, decisions, root causes, procedures, and verified facts into dedicated memories through the supported memory mechanism. Follow the current runtime's write permissions.
- Count a memory write only after the memory system confirms success.
- If durable memory is unavailable, report the limitation and keep a redacted pending checkpoint in chat. Retry before finishing and report any entries still unsaved. Native memory and chat checkpoints supplement a configured shared memory system.
- Preserve generated memory files unless the runtime explicitly supports editing them.
- On work tasks, also load the `bothq-memory` skill; BothQ holds the journal there.
