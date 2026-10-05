# Personal instructions for Codex

Read and follow [agents.md](agents.md) before starting any task. Resolve instruction links relative to the directory containing this file, follow them recursively, and apply the imported rules together with this file. Stop and report a required file that cannot be read.

Use `~/skills/common` and `~/skills/personal` for personal tasks.

## Native memory and checkpoints

- When a native memory search is needed, open the relevant records before relying on them.
- For long-running work, keep a concise checkpoint series in the chat named `task-journal-YYYY-MM-DD-HHMM-codex-<task>`. Use it as the rolling task journal required by the shared rules.
- Append checkpoints at material milestones and before handoff or compaction. Record scope, decisions, ownership, current state, verification evidence, blockers, and the exact next action.
- Let the transcript and tool history carry routine commands and intermediate activity. Reference evidence rather than copying logs.
