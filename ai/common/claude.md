# Claude Code instructions

@global.md

Apply the imported rules together with this file. Stop and report a required import that cannot be read.

## Instruction adherence

- Follow `global.md` and every other imported rule to the letter. Do not deviate, shorten, or substitute your own preference.
- Follow the user's explicit instructions the same way. These are hard rules, not suggestions.
- If a rule cannot be followed, stop and report the conflict instead of working around it.

## Orchestration

- Use only T3 Code's orchestration layer for sub-agents and delegated tasks, through the `t3-code` MCP server. Never use Claude Code orchestration or sub-agent tools, even when they are available.
- If T3 Code orchestration is unavailable, report the blocker. Do not fall back to Claude Code orchestration.

## Native memory

- Consult available Claude Code native memory for relevant prior work. Use its supported memory mechanism for explicit remember, forget, or update requests.
- Use `claude-code` as the runtime label in task-journal names.
