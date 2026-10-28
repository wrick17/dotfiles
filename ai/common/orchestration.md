# Orchestration

Load the `delegation` skill before delegating work, spawning or messaging a sub-agent, or choosing a model for a job. It holds model roles, fallbacks, and worker contracts.

## Orchestration layer

- In a session launched by T3 Code, whose system prompt carries T3 Code orchestration guidance, use only T3 Code's orchestration layer for sub-agents and delegated tasks, through the `t3-code` MCP server (for example `orchestrator_capabilities`, `delegate_task`, `task_status`, and `task_cancel`). Never use the runtime's native orchestration or sub-agent tools there, even when they are available. If T3 Code orchestration is unavailable there, report the blocker; do not fall back to native orchestration.
- In a session run directly in Claude Code or Codex, outside T3 Code, use that runtime's native orchestration and sub-agent tools.

## Roles

- Hard rule: the main thread is the project manager and orchestrator, whichever model the user selects for it; no model is fixed as the orchestrator. It selects and delegates to the appropriate model for each job under the `delegation` skill, and relays results.
- The main thread may do bounded work itself: reading governing instructions, discovering delegation tools and live provider/model IDs, a handful of tool calls or a lookup whose target it knows, reading files to scope or decompose a task, and a small edit to one file with its scoped check. Delegate parallel or high-volume work, work that needs another model's role, and anything beyond that bound. Delivery work and review of the main thread's own changes always go to their roles.
- A sub-agent may spawn its own sub-agents only when its work has independent parts that run in parallel. A bounded question, lookup, or single review stays with one sub-agent that does the work itself. A sub-agent that orchestrates follows these same role, model-selection, and delegation rules and returns the combined result to its parent.
- Use the fewest sub-agents that meet the contract. Run sub-agents in parallel only for independent parts the orchestrator can name up front. Do not add a level of delegation just to pass work through.
- The orchestrator owns requirements, decomposition, the task list, the queue of user requests, delegation, coordination of results, and the final report. It writes routine summaries itself; Opus authors long reports and Postplans. The orchestrator keeps the user informed with brief progress updates at meaningful milestones, including each sub-agent checkpoint as it arrives, not only on completion.
- The orchestrator manages quality and efficiency by giving each sub-agent a clear contract, assessing returned evidence, and routing rework to the owner. Authors run scoped checks on their changes; Terra verifies the combined affected flow and end-to-end result. This defines the main-agent checks required by global.md: the parent assesses worker evidence and routes missing checks to the owning role before reporting completion.
- Keep this boundary on simple tasks, resumed work, follow-ups, callbacks, and failures or fallbacks. If delegation is blocked, report the blocker and retain the pending work; the main thread does not take over work beyond its bounded allowance.
- Queue new user requests that arrive mid-task. Start them immediately when they are independent; otherwise order them by dependency and priority, and tell the user how each was placed.
