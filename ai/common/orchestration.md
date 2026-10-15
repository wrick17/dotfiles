# Orchestration

## Roles

- Handle very simple tasks in the main thread. A task is very simple when it is clear, low-risk, touches one small area, and needs no research, design decision, or multi-step verification, such as answering a direct question, a one-line fix, or a small documentation edit.
- For all other tasks, the main thread acts as the orchestrator and sub-agents do the work. Use as many sub-agents as the work needs.
- A sub-agent may act as an orchestrator when its work is complex. It may spawn and manage its own sub-agents under these rules, integrates their results, and returns the combined result to its parent orchestrator.
- The orchestrator owns requirements, decomposition, the task list, the queue of user requests, delegation, integration, and the final result. It keeps the user informed with brief progress summaries at meaningful milestones.
- The orchestrator manages quality and efficiency: it gives each sub-agent a clear contract, reviews returned work, routes rework to the owner, and verifies the combined result before reporting completion.
- The orchestrator may read files and run small checks to brief agents or verify results. It does not perform substantive implementation, research, or review that a sub-agent should own.
- Queue new user requests that arrive mid-task. Start them immediately when they are independent; otherwise order them by dependency and priority, and tell the user how each was placed.

## Model selection

- Use the latest Opus, Sol, and Luna models unless the user or a task-specific rule specifies otherwise. Resolve identifiers from the live provider catalog instead of pinning versions.
- Opus: architecture, design, UI and UX, complex coding, and complex problem solving.
- Sol: codebase research, verification, code review, standard coding, and all other work not listed for Opus or Luna.
- Luna: mechanical work such as batch commands, Git operations, linting, formatting, and simple grunt work that needs little judgment.
- Use other models only when the user or a task-specific rule names them.
- Set reasoning effort per task: low for mechanical work, medium for routine work, and high or above for complex, ambiguous, or high-risk work.
- Escalate to a stronger model or higher effort when an agent fails, stalls, or returns low-quality work. Do not retry the same configuration without a changed hypothesis or new context.
- Have a different agent from the author review consequential work. Prefer Sol to review Opus-authored code.

### Fallbacks

Apply these when cross-provider delegation is unavailable:

- Claude Code: use Haiku for mechanical work and Opus for everything else.
- Codex: use Luna for mechanical work and Sol for everything else.
- If a chosen model is otherwise unavailable, use the closest available model for the role and tell the user.

## Delegation

- Use native sub-agent tools when they support the chosen model. Otherwise, in T3 Code, use its orchestration tools for cross-provider or unsupported models.
- Set the model and effort explicitly in every spawn or delegation call, and verify the child's runtime selection after it starts.
- Prioritize blockers, consequential uncertainties, and the critical path before supporting work.
- Give each worker a compact contract: objective, relevant context, owned files or state, constraints, dependencies, completion condition, and required evidence.
- Pass only necessary history. Include relevant user decisions and constraints even when starting a fresh context.
- Assign one writer per shared file or mutable resource. Agree on shared interfaces before parallel implementation.
- Route corrections and follow-ups to the existing owner. Reuse agents for related work when their context remains useful.
- Avoid duplicate investigations unless an independent assessment addresses a concrete risk.
- Workers return concise findings or changes, evidence pointers, check results, and unresolved issues. Keep bulky logs out of the main thread.
- Wait for completion notifications or use an appropriate blocking wait. Check status when intervention is needed, rather than repeatedly polling.
- Stop obsolete or unnecessary work. Close or release finished agents when supported; do not claim resources were released without evidence.
