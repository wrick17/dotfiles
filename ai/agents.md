# Codex instructions

Read and follow [global.md](global.md) before starting any task. Resolve instruction links relative to the directory containing this file, follow them recursively, and apply the imported rules together with this file. Stop and report a required file that cannot be read.

## Model routing

- Use the live Astra, Sol, and Luna models from the available Codex catalog. Use Sol for substantive implementation, research, debugging, and review; use Luna for clear, bounded tasks and routine verification when it can deliver the required quality.
- Choose a supported context-fork mode that permits explicit model and reasoning-effort overrides. Do not assume a full-history fork preserves those overrides.
- Use native sub-agent tools when they support the chosen provider and model. In T3 Code, use its orchestration tools for cross-provider work or models unsupported by native tools.

## Native memory

- Consult supplied native memory for relevant prior work and search `~/.codex/memories/MEMORY.md` when needed. Use the supported memory mechanism and follow its write restrictions.
- Use `codex` as the runtime label in task-journal names.
