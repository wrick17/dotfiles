# Orchestration

## Orchestration layer

- Use only T3 Code's orchestration layer for sub-agents and delegated tasks, through the `t3-code` MCP server (for example `orchestrator_capabilities`, `delegate_task`, `task_status`, and `task_cancel`).
- Never use Claude Code or Codex orchestration or sub-agent tools, even when they are available.
- If T3 Code orchestration is unavailable, report the blocker. Do not fall back to Claude Code or Codex orchestration.

## Roles

- Hard rule: the main thread is the project manager and orchestrator, whichever model the user selects for it; no model is fixed as the orchestrator. It only orchestrates, manages tasks, and relays results, including Opus-authored reports. It selects and delegates to the appropriate model for each job under Model selection below.
- The only exception is a direct one-line conversational reply that requires no substantive task or tool work. Delegate every actual task, including one-line edits, commands, file inspection, research, reviews, verification, and delivery. A short task or answer does not qualify for the exception.
- A sub-agent of any model may orchestrate when its work can be broken into parts that justify it. Orchestration is optional, not required: a bounded question, lookup, or single review stays with one sub-agent that does the work itself. A sub-agent that orchestrates follows these same role rules and returns the combined result to its parent.
- Use the fewest sub-agents that meet the contract. Run sub-agents in parallel only for independent parts the orchestrator can name up front. Do not add a level of delegation just to pass work through.
- The orchestrator owns requirements, decomposition, the task list, the queue of user requests, delegation, coordination of results, and relaying the final report. Opus authors reports. The orchestrator keeps the user informed with brief progress updates at meaningful milestones, including each sub-agent checkpoint as it arrives, not only on completion.
- The orchestrator manages quality and efficiency by giving each sub-agent a clear contract, assessing returned evidence, and routing rework to the owner. Workers inspect diffs, check shared assumptions, and verify the combined affected flow and end-to-end result. This defines the main-agent checks required by global.md: the parent assesses worker evidence and delegates missing checks before reporting completion; it does not perform verification itself.
- Necessary orchestration bootstrap is allowed: reading governing instructions and their required imports, discovering delegation tools and live provider/model IDs, and managing delegated tasks. This permission covers orchestration only. Delegate task-specific file reads and all other read-only checks; integration means coordinating worker results, with workers performing edits and delivery actions.
- Keep this boundary on simple tasks, resumed work, follow-ups, callbacks, and failures or fallbacks. If delegation is blocked, report the blocker and retain the pending work; the main thread never takes over task execution.
- Queue new user requests that arrive mid-task. Start them immediately when they are independent; otherwise order them by dependency and priority, and tell the user how each was placed.

## Model selection

- Use the latest Opus, Sol, Terra, and Luna models unless the user or a task-specific rule specifies otherwise. Resolve identifiers from the live provider catalog instead of pinning versions.
- Opus: all coding except Sol's merge-conflict resolution, including standard implementation, coding fixes, and follow-ups; design, both visual (UI, UX, and interaction design) and architecture (system, software, and module or interface design); complex problem solving; and report writing. Opus does its assigned work itself. A complex task does not give Opus ownership of its full lifecycle. After its contribution, classify remaining work and hand delivery back to Terra.
- Sol: codebase research, code review, and merge-conflict resolution. Sol writes code only to resolve merge conflicts, including edits needed to reconcile the conflicting changes.
- Terra: all verification and delivery work. Verification includes running test cases, automated UI testing, and checking the combined affected flow. Delivery includes commits, push, and history rewrites; PR creation, updates, monitoring, babysitting, review follow-up triage, CI reruns and triage, retries, and merge; packaging, installation, release, publication, deployment, and their verification. These stay with Terra even within a complex task. Other code needed during CI, review, or delivery goes to Opus, and merge conflicts go to Sol. Terra also owns all other non-coding work not assigned to Opus, Sol, or Luna.
- Luna: bounded mechanical supporting tasks such as linting, formatting, or collecting command output that need little judgment, plus batch Git operations across repositories or branches: fetch, pull, syncing or rebasing branches onto their base, and branch cleanup. Luna hands any conflict to Sol. Commits, push, history rewrites, and PR and delivery work belong to Terra, even when mechanical.
- These model roles determine which worker receives each job; they never authorize main-thread task execution. Bounded workers do their assigned work themselves without an unnecessary delegation level. Apply the roles at every step, including resumed work, CI callbacks, PR and release monitoring, and follow-ups. Task-specific workflows do not expand a model's role without an explicit user-authorized exception; the main-thread boundary still applies.
- Use other models only when the user or a task-specific rule names them.
- Set reasoning effort per task: low for mechanical work, medium for routine work, and high or above for complex, ambiguous, or high-risk work.
- When an agent fails, stalls, or returns low-quality work, increase effort or reassign to another agent using the same model and role. Delegate a bounded specialist problem to Opus when needed, then return delivery to Terra. Failure does not authorize Opus to take over Terra's or Sol's work; only the usage-limit exception under Fallbacks does. Do not retry the same configuration without a changed hypothesis or new context.
- Have a different agent from the author review consequential work. Prefer Sol to review Opus-authored code.

### Fallbacks

- If the required model is unavailable or cannot complete its work, report the blocker and ask before changing the role or model unless the user already explicitly authorized that exception. Keep pending work with its assigned role; never expand Opus's scope implicitly because Terra or Sol is unavailable or fails.
- Usage limits are the authorized exception. When a model's provider reaches its session or weekly usage limit, reassign all of that model's in-flight and pending work to its partner: Opus and Sol cover for each other, Sonnet covers for Terra, and Luna and Haiku cover for each other. The partner takes over the full role, including work the limited role would normally own. Switch only after the limit is actually reached, never preemptively. Tell the user when a switch happens, and return to normal role assignment when the limit resets.

## Delegation

- Delegate every sub-agent through T3 Code's orchestration layer, including same-provider work. Discover provider and model IDs with `orchestrator_capabilities`.
- Set the model and effort explicitly in every spawn or delegation call, and verify the child's runtime selection after it starts.
- Prioritize blockers, consequential uncertainties, and the critical path before supporting work.
- Give each worker a compact contract: objective, relevant context, owned files or state, constraints, dependencies, completion condition, and required evidence. For Opus, Sonnet, or Haiku, spell out the contract in the task itself: the instruction file paths and specific rules that apply, prohibited actions where material, and the verification evidence to return. Do not rely on inherited context or generic "follow the rules" wording. This applies to initial tasks and follow-ups.
- Pass only necessary history. Include relevant user decisions and constraints even when starting a fresh context.
- Assign one writer per shared file or mutable resource. Agree on shared interfaces before parallel implementation.
- Start a new sub-agent for every task, follow-up, and correction. Reuse an existing sub-agent only when the work cannot be done without its prior context and still fits its role, or when a task-specific rule requires a persistent agent. Classify corrections and follow-ups by model role before routing them; return delivery work to Terra after an Opus specialist contribution.
- Avoid duplicate investigations unless an independent assessment addresses a concrete risk.
- Workers report each checkpoint to their parent as they reach it, such as diagnosis done, implementation done, checks passing or failing, PR opened, or a blocker, in a line or two.
- Workers return concise findings or changes, evidence pointers, check results, and unresolved issues. Keep bulky logs out of the main thread. The orchestrator checks that evidence against the delegated rules and routes corrections before accepting completion.
- Wait for completion notifications or use an appropriate blocking wait. Check status when intervention is needed, rather than repeatedly polling. Relay checkpoint events to the user as they arrive.
- Stop obsolete or unnecessary work. Close or release finished agents when supported; do not claim resources were released without evidence.
