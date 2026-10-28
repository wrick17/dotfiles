# Personal instructions for Claude Code

@../common/claude.md

Apply the imported rules together with this file. Stop and report a required import that cannot be read.

Use `~/skills/mine/common`, `~/skills/mine/personal`, `~/skills/third-party/common`, and `~/skills/third-party/personal` for personal tasks.

## Native memory and checkpoints

- When a native memory search is needed, open the relevant records before relying on them.
- For long-running work, keep a concise checkpoint series in the chat named `task-journal-YYYY-MM-DD-HHMM-claude-code-<task>`. Use it as the rolling task journal required by the shared rules.
- Append checkpoints at material milestones and before handoff or compaction. Record scope, decisions, ownership, current state, verification evidence, blockers, and the exact next action.
- Let the transcript and tool history carry routine commands and intermediate activity. Reference evidence rather than copying logs.
