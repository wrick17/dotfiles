# Orchestration

## Orchestration layer

- Use only T3 Code's orchestration layer for sub-agents and delegated tasks, through the `t3-code` MCP server (for example `orchestrator_capabilities`, `delegate_task`, `task_status`, and `task_cancel`).
- Never use Claude Code or Codex orchestration or sub-agent tools, even when they are available.
- If T3 Code orchestration is unavailable, report the blocker. Do not fall back to Claude Code or Codex orchestration.

## Roles

- Handle very simple tasks in the main thread only when they fit the current model's role below. A task is very simple when it is clear, low-risk, touches one small area, and needs no research, design decision, or multi-step verification. Even one command, a one-line fix, or a small documentation edit must respect model roles; delegate work outside the current model's role.
- For all other tasks, the main thread acts as the orchestrator and sub-agents do the work.
- A sub-agent may orchestrate when its work can be broken into parts that justify it. Orchestration is optional, not required: a bounded question, lookup, or single review stays with one sub-agent that does the work itself. A sub-agent that orchestrates follows these same role rules and returns the combined result to its parent.
- Use the fewest sub-agents that meet the contract. Run sub-agents in parallel only for independent parts the orchestrator can name up front. Do not add a level of delegation just to pass work through.
- The orchestrator owns requirements, decomposition, the task list, the queue of user requests, delegation, integration, and the final result. It keeps the user informed with brief progress summaries at meaningful milestones.
- The orchestrator manages quality and efficiency: it gives each sub-agent a clear contract, reviews returned work, routes rework to the owner, and verifies the combined result before reporting completion.
- The orchestrator may read files, run small nonmutating checks, and handle orchestration bookkeeping, requirements, and user communication. It delegates substantive implementation, research, review, verification, and delivery operations to the assigned model. Integration means coordinating results; edits and delivery actions still follow model roles.
- Queue new user requests that arrive mid-task. Start them immediately when they are independent; otherwise order them by dependency and priority, and tell the user how each was placed.

## Model selection

- Use the latest Opus, Sol, and Luna models unless the user or a task-specific rule specifies otherwise. Resolve identifiers from the live provider catalog instead of pinning versions.
- Opus: orchestration and specifically assigned specialist work in architecture, design, UI and UX, complex coding, and complex problem solving. A complex task does not give Opus ownership of its full lifecycle. After its specialist contribution, classify remaining work and hand delivery back to Sol. An Opus orchestrator, main thread or sub-agent, delegates delivery operations and routes follow-ups to Sol.
- Sol: codebase research, verification, code review, standard implementation, and actual delivery work. Sol owns Git operations including commits, push, history rewrites, and branch operations; PR creation, updates, monitoring, babysitting, review follow-ups, CI fixes, retries, and merge; packaging, installation, release, publication, deployment, and their verification. These operations stay with Sol even within a complex task. Sol also owns all other work not assigned to Opus or Luna.
- Luna: bounded mechanical supporting tasks such as linting, formatting, or collecting command output that need little judgment. Git operations and delivery work belong to Sol, even when mechanical.
- Apply these roles to main threads and workers at every step, including resumed work, CI callbacks, PR and release monitoring, and follow-ups. Task-specific workflows do not expand a model's role without an explicit user-authorized exception.
- Use other models only when the user or a task-specific rule names them.
- Set reasoning effort per task: low for mechanical work, medium for routine work, and high or above for complex, ambiguous, or high-risk work.
- When an agent fails, stalls, or returns low-quality work, increase effort or reassign to another agent using the same model and role. Delegate a bounded specialist problem to Opus when needed, then return delivery to Sol. Failure does not authorize Opus to take over Sol's work. Do not retry the same configuration without a changed hypothesis or new context.
- Have a different agent from the author review consequential work. Prefer Sol to review Opus-authored code.

### Fallbacks

- If the required model is unavailable or cannot complete its work, report the blocker and ask before changing the role or model unless the user already explicitly authorized that exception. Keep pending work with its assigned role; never expand Opus's scope implicitly because Sol is unavailable or fails.

## Delegation

- Delegate every sub-agent through T3 Code's orchestration layer, including same-provider work. Discover provider and model IDs with `orchestrator_capabilities`.
- Set the model and effort explicitly in every spawn or delegation call, and verify the child's runtime selection after it starts.
- Prioritize blockers, consequential uncertainties, and the critical path before supporting work.
- Give each worker a compact contract: objective, relevant context, owned files or state, constraints, dependencies, completion condition, and required evidence.
- Pass only necessary history. Include relevant user decisions and constraints even when starting a fresh context.
- Assign one writer per shared file or mutable resource. Agree on shared interfaces before parallel implementation.
- Classify corrections and follow-ups by model role before routing them. Reuse the existing owner only when the work still fits that role; return delivery work to Sol after an Opus specialist contribution.
- Avoid duplicate investigations unless an independent assessment addresses a concrete risk.
- Workers return concise findings or changes, evidence pointers, check results, and unresolved issues. Keep bulky logs out of the main thread.
- Wait for completion notifications or use an appropriate blocking wait. Check status when intervention is needed, rather than repeatedly polling.
- Stop obsolete or unnecessary work. Close or release finished agents when supported; do not claim resources were released without evidence.
