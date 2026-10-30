---
name: delegation
description: Model roles (Opus, Sol, Terra, Luna), usage-limit fallbacks, and worker contracts. Use before delegating work, spawning or messaging a sub-agent, choosing a model or effort for a job, routing a correction, or handling an unavailable or usage-limited model.
---

# Delegation

Apply with the always-loaded orchestration core (`orchestration.md`), which sets the orchestration layer and the main thread's role.

## Model selection

- Use the latest Opus, Sol, Terra, and Luna models unless the user or a task-specific rule specifies otherwise. Resolve identifiers from the live provider catalog instead of pinning versions.
- Opus: all coding except Sol's merge-conflict resolution, including standard implementation, coding fixes, and follow-ups; design, both visual (UI, UX, and interaction design) and architecture (system, software, and module or interface design); complex problem solving; and long reports and Postplans. Opus does its assigned work itself. Opus runs only scoped checks for the code it changed, such as the tests, type checks, and lint for the touched files or module; it does not run or chase the full suite. A complex task does not give Opus ownership of its full lifecycle. After its contribution, classify remaining work and hand verification and delivery to Terra.
- Sol: codebase research, code review, and merge-conflict resolution. Sol writes code only to resolve merge conflicts, including edits needed to reconcile the conflicting changes.
- Terra: bulk verification and all delivery work. Verification includes full and cross-module test runs, automated UI testing, and checking the combined affected flow. Delivery includes commits, push, and history rewrites; PR creation, updates, monitoring, babysitting, review follow-up triage, CI reruns and triage, retries, and merge; packaging, installation, release, publication, deployment, and their verification. These stay with Terra even within a complex task. The exception is a small-tier task under `orchestration.md`, where the main thread commits and pushes itself when the user asks. Failures that need code changes go to Opus with the failing evidence, and merge conflicts go to Sol. Terra also owns all other non-coding work not assigned to Opus, Sol, or Luna.
- Luna: bounded mechanical supporting tasks such as linting, formatting, or collecting command output that need little judgment, plus batch Git operations across repositories or branches: fetch, pull, syncing or rebasing branches onto their base, and branch cleanup. Luna hands any conflict to Sol. Commits, push, history rewrites, and PR and delivery work belong to Terra, even when mechanical.
- These model roles determine which worker receives each job beyond the main thread's bounded allowance. Bounded workers do their assigned work themselves without an unnecessary delegation level. Apply the roles at every step, including resumed work, CI callbacks, PR and release monitoring, and follow-ups. Task-specific workflows do not expand a model's role without an explicit user-authorized exception.
- Use other models only when the user or a task-specific rule names them.
- Choose reasoning effort per task from its difficulty and risk, up to `xhigh`: low for mechanical work, medium for routine work, and high or `xhigh` for complex, ambiguous, or high-risk work. Never use `max`.
- When an agent fails, stalls, or returns low-quality work, increase effort or reassign to another agent using the same model and role. Delegate a bounded specialist problem to Opus when needed, then return delivery to Terra. Failure does not authorize Opus to take over Terra's or Sol's work; only the usage-limit exception under Fallbacks does. Do not retry the same configuration without a changed hypothesis or new context.
- Have a different agent from the author review consequential work. Prefer Sol to review Opus-authored code.

## Fallbacks

- If the required model is unavailable or cannot complete its work, report the blocker and ask before changing the role or model unless the user already explicitly authorized that exception. Keep pending work with its assigned role; never expand Opus's scope implicitly because Terra or Sol is unavailable or fails.
- Partners: Opus and Sol cover for each other, Sonnet covers for Terra, and Luna and Haiku cover for each other.
- Usage limits are the authorized exception. When a model's provider reaches its session or weekly usage limit, reassign all of that model's in-flight and pending work to its partner. The partner takes over the full role, including work the limited role would normally own. Switch only after the limit is actually reached, never preemptively. Tell the user when a switch happens, and return to normal role assignment when the limit resets.
- Native orchestration outside T3 Code reaches only its own provider's models. There, assign each role whose model it cannot reach to that model's partner.

## Worker contracts

- Inside T3 Code, delegate every sub-agent through T3 Code's orchestration layer, including same-provider work, and discover provider and model IDs with `orchestrator_capabilities`. Outside T3 Code, use the runtime's native sub-agent tools.
- Set the model and effort explicitly in every spawn or delegation call, and verify the child's runtime selection after it starts.
- Prioritize blockers, consequential uncertainties, and the critical path before supporting work.
- Give each worker a compact contract: objective, relevant context, owned files or state, constraints, dependencies, completion condition, and required evidence. Mention that the worker may spawn its own sub-agents only when the task has independent parts worth splitting. For Opus, Sonnet, or Haiku, spell out the contract in the task itself: the instruction file paths, skills, and specific rules that apply, prohibited actions where material, and the verification evidence to return. Do not rely on inherited context or generic "follow the rules" wording. This applies to initial tasks and follow-ups.
- Pass only necessary history. Include relevant user decisions and constraints even when starting a fresh context.
- Assign one writer per shared file or mutable resource. Agree on shared interfaces before parallel implementation.
- Start a new sub-agent for every independent review or re-check. While a worker is available and the work still fits its role, send it corrections and follow-ups on its own output, and its next ready chunk when that chunk touches the same module or files so its context carries over (in T3, `t3_thread_send` to its thread). For any other task, start a fresh worker, and pass the needed history when it replaces a worker that is gone or out of context.
- Queue each review or test finding behind the author's current chunk (in T3, `t3_thread_send` mode `queue`). Steer it in at once (mode `steer`) only when it blocks a pending chunk that depends on it, or when it is a security or data-loss problem. Classify corrections and follow-ups by model role before routing them; return delivery work to Terra after an Opus specialist contribution.
- Avoid duplicate investigations unless an independent assessment addresses a concrete risk.
- Workers report each checkpoint to their parent as they reach it, such as diagnosis done, implementation done, checks passing or failing, PR opened, or a blocker, in a line or two.
- Workers return concise findings or changes, evidence pointers, check results, and unresolved issues. Keep bulky logs out of the main thread. The orchestrator checks that evidence against the delegated rules and routes corrections before accepting completion.
- When the pipeline in `orchestration.md` has nothing to dispatch or route, wait for completion notifications or use an appropriate blocking wait. Check status when intervention is needed, rather than repeatedly polling. Relay checkpoint events to the user as they arrive.
- Stop obsolete or unnecessary work. Close or release finished agents when supported; do not claim resources were released without evidence.
