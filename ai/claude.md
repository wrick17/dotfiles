# Claude Code instructions

@global.md

Apply the imported rules together with this file. Stop and report a required import that cannot be read.

## Model routing

- Use live Claude Code model identifiers from the available catalog. Use Opus for the hardest unresolved decisions, Sonnet for substantive implementation, research, debugging, and review, and Haiku for clear, bounded tasks when it can deliver the required quality.
- Select supported effort and context-sharing options. Pass a compact task contract when context forking is unavailable.
- Use native sub-agent tools when they support the chosen provider and model. In T3 Code, use its orchestration tools for cross-provider work or models unsupported by native tools.

## Native memory

- Consult available Claude Code native memory for relevant prior work. Use its supported memory mechanism for explicit remember, forget, or update requests.
- Use `claude-code` as the runtime label in task-journal names.
