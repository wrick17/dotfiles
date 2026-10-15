# Codex instructions

Read and follow [global.md](global.md) before starting any task. Resolve instruction links relative to the directory containing this file, follow them recursively, and apply the imported rules together with this file. Stop and report a required file that cannot be read.

## Instruction adherence

- Follow `global.md` and every other imported rule to the letter. Do not deviate, shorten, or substitute your own preference.
- Follow the user's explicit instructions the same way. These are hard rules, not suggestions.
- If a rule cannot be followed, stop and report the conflict instead of working around it.

## Orchestration

- Use only T3 Code's orchestration layer for sub-agents and delegated tasks, through the `t3-code` MCP server. Never use Codex orchestration or sub-agent tools, even when they are available.
- If T3 Code orchestration is unavailable, report the blocker. Do not fall back to Codex orchestration.

## Native memory

- Consult supplied native memory for relevant prior work and search `~/.codex/memories/MEMORY.md` when needed. Use the supported memory mechanism and follow its write restrictions.
- Use `codex` as the runtime label in task-journal names.
