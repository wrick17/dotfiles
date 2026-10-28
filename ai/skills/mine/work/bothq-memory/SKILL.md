---
name: bothq-memory
description: BothQ is the mandatory shared memory and task journal for work tasks. Use at the start of every non-trivial work task, on resume, and whenever writing a journal entry or checkpoint on a work task.
---

# BothQ memory

- Treat local BothQ at `~/Projects/bot_hq` as the mandatory shared memory and chronological record for every non-trivial work task. Native memory supplements BothQ; it does not replace it.
- Before acting and on resume, use `recall_memories`, `find_rule`, and `find_routine` to retrieve relevant requirements, preferences, decisions, unfinished work, and the latest checkpoint. Verify recalled facts when they may have changed.
- Immediately create one journal with `save_memory`, named `task-journal-YYYY-MM-DD-HHMM-<runtime>-<task>`, using the runtime label from the imported instructions. Retrieve and resume an existing journal when continuing the same task.
- Append timestamped journal entries with `append_memory`. `update_memory` replaces a memory's content; use it only after reading and retaining the full existing journal.
- Follow the `task-journal` skill for continuous recording, checkpoints, one journal writer, and promotion of reusable knowledge into dedicated BothQ memories.
- Count a write only after BothQ confirms success. If BothQ is unavailable, report the outage immediately and keep a redacted pending checkpoint in chat. Retry before finishing and replay pending entries after recovery. Report entries still unsaved and claim complete recording only after confirmation.
