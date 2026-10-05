# Global instructions

Shared rules for Codex and Claude Code in work and personal setups.

## Defaults

- Quality comes first. Optimize the total time and cost of a correct result, including retries, review, and rework.
- Apply Ponytail to reasoning, planning, tool use, implementation, and verification. Choose the smallest approach that reliably meets the goal.
- Load and apply `pstack:unslop` to every user-facing response.
- Preserve unrelated changes and follow the repository's conventions.
- Verify changing or uncertain technical claims against official sources.
- Scale the process to the task. A clear, small fix needs a small workflow.

## Skills

- Load skills explicitly requested by the user and those required by the task. Read their `SKILL.md` before applying them, resolve references relative to that skill, and follow the current skill catalog's paths.
- Shared skills live in `~/skills/common`. Work setups also use `~/skills/work`; personal setups also use `~/skills/personal`.
- Work skills apply only to work tasks. `sequoia-frontend` belongs to the work profile and must not be installed or loaded in personal setups.
- Plugin-managed skills remain managed by their plugins. Preserve their installations and caches.
- The user's direct instructions take precedence over skill guidance. Use available evidence and existing answers before asking for a missing decision.

## Understand the work

- Before implementing new features or ambiguous changes, use `mattpocock-skills:grill-me`. If unavailable in the skill catalog, read `~/skills/.sources/mattpocock-skills/skills/productivity/grill-me/SKILL.md`.
- Use existing answers and inspect available evidence before asking questions. Interview only while material uncertainty remains.
- Finish requirements discovery with a clear outcome, constraints, scope, and observable completion criteria.
- Proceed directly on clear fixes after tracing the affected flow and relevant callers.
- Ask when a missing decision materially changes scope or risk. Otherwise state a reasonable assumption and proceed.

## Implement and verify

- Use a fail-fast strategy. Get the smallest main flow working or fix the reported bug first, verify it works, then handle relevant edge cases, stability, and polish.
- Apply security controls, trust-boundary validation, accessibility basics, and data-loss protections from the start.
- For a new feature, establish the smallest working end-to-end path before spreading dependent implementation across agents.
- Reuse existing code, standard libraries, native platform features, and installed dependencies before adding machinery.
- Fix bugs at their shared cause. Inspect sibling callers before choosing the location of a fix.
- Use the smallest meaningful check during iteration. Focus tests on important behavior, shared contracts, and demonstrated bugs or risks.
- Reuse existing test files and helpers. Add a test case only when it catches an important failure that existing checks would miss; create a new test file only when an existing suite cannot reasonably cover it.
- Avoid tests that mirror implementation details, duplicate coverage, or enumerate speculative edge cases. Excess tests can narrow design exploration and increase iteration time and cost. Choose useful coverage over test count.
- Run required repository checks and verify the combined affected flow before declaring completion.
- Repeat successful checks only when subsequent changes or new evidence could invalidate them.
- Complete the agreed scope. Report any remaining limitations explicitly; a working happy flow alone is not completion.

## Model selection

- Select live, callable model identifiers and supported reasoning effort explicitly for each spawn. Choose for successful completion, not the lowest per-token price.
- When the highest-capability model is the main agent, reserve its effort for requirements, decomposition, consequential decisions, integration, and the hardest unresolved problems.
- Start difficult or high-risk work with sufficient capability and effort. Escalate promptly when evidence shows the current choice is insufficient.
- Escalate a precise problem with evidence and a decision needed. Return routine execution to the worker after resolving it.
- Keep reusable agent definitions model- and effort-agnostic. Use supported context-sharing and model-selection options; pass a compact task contract when context forking is unavailable.
- If a preferred model is unavailable, choose an appropriate available model and disclose any material limitation. Task-specific model requirements still apply.

## Delegate efficiently

- Name agents `<work-title>__<model>_<effort first character>`, using a compact model name and uppercase effort initial.
- Delegate when independent work can improve completion time or quality enough to justify coordination cost.
- Use as many agents as useful work requires. Keep small tasks local when delegation would cost more than it saves.
- Prioritize blockers, consequential uncertainties, and the critical path before supporting work.
- Give each worker a compact contract: objective, relevant context, owned files or state, constraints, dependencies, completion condition, and required evidence.
- Pass only necessary history. Include relevant user decisions and constraints even when starting a fresh context.
- Assign one writer per shared file or mutable resource. Agree on shared interfaces before parallel implementation.
- Route corrections and follow-ups to the existing owner. Reuse agents for related work when their context remains useful.
- Avoid duplicate investigations unless an independent assessment addresses a concrete risk.
- Workers return concise findings or changes, evidence pointers, check results, and unresolved issues. Keep bulky logs out of the main thread.
- Wait for completion notifications or use an appropriate blocking wait. Check status when intervention is needed, rather than repeatedly polling.
- Stop obsolete or unnecessary work. Close or release finished agents when supported; do not claim resources were released without evidence.

## Decisions and integration

- Settle uncertain behavior with the smallest useful experiment. Each retry should test a changed hypothesis or use new evidence.
- Compare competing designs in parallel only when the decision is consequential and difficult to reverse.
- Workers verify their changes. The main agent checks the combined diff, shared assumptions, and end-to-end result.
- Use independent review for consequential correctness, security, migration, or data-loss risks. Scale review to the change.
- Distinguish observed facts, inferences, and unresolved assumptions.
- Revisit an accepted decision when new evidence invalidates it; otherwise continue execution.

## Browser work

- Use the T3 Code browser through the `t3-code` MCP `preview_*` tools by default. This includes normal research, public pages, Postplans, and any browser work that does not explicitly require the user's browser.
- "Built-in browser" means the T3 Code browser. Do not use the cmux browser or cmux browser tools. If T3 browser tools are unavailable, report the limitation instead of switching to cmux.
- Use the user's browser only when the user explicitly says to use it or asks to check something in it. Once selected, keep all browser work for that task in the user's browser unless the user explicitly asks to switch.
- If the user's browser is required but unavailable, report the limitation or request the required user action. Do not silently fall back to the built-in/T3 browser or Computer Use.
- In the user's browser, use Browser MCP by Wrick, `@wrick17/browser-mcp@1.26.1`, only for tab management. Do not use the upstream Agent360 package or a repo-local server.
- At the start of user-browser work, create a dedicated task group with `browser_set_tab_group_name`.
- Open agent tabs in that group using `browser_navigate` with `new_tab: true`, preferably in the background. Reuse them and keep the tab count low.
- Never use Browser MCP to navigate an existing tab or interact with page content.
- Use `chrome-devtools-mcp` with existing Chrome for all page interaction and inspection in the user's browser.
- For page-scoped DevTools calls, use the assigned `pageId` and select it with `bringToFront: false`.
- Never operate both MCPs on the same tab concurrently.
- Ask the user to authenticate when needed.
- Before finishing user-browser work, close agent-created tabs and verify the task group is gone. Preserve the user's tabs and any task tabs they explicitly ask to keep.

## Diagrams

- Every main agent and delegated worker must load and use `$archify` for architecture, infrastructure, cloud, security, network topology, workflow, sequence, data-flow, lifecycle, state-machine, pipeline, lineage, and Mermaid-conversion requests.
- Also use Archify when one of those diagrams would make a substantial technical explanation or report materially clearer.
- For every HTML report, HTML document, or Postplan, assess whether an architecture diagram would help. When it would, generate it with Archify and include it in the artifact.
- Follow Archify's validation and delivery checks. Use another diagram format only when the user explicitly requests it or Archify is unavailable.

## Progress and deliverables

- For multi-step work, use the tasks feature when available. Keep completed and future work coarse; expand only active work.
- Give brief updates at meaningful milestones: outcome, blocker, decision, or next step.
- Keep small plans and recommendations in chat.
- When a substantial report or implementation plan needs an artifact, create dark-mode HTML in a temporary directory and upload it with `bunx postplan upload <file>.html`.
- For every Postplan, load and apply `$pstack:technical-writing` and `$pstack:unslop`.
- Every code block in a plan or Postplan must have syntax highlighting for its language. Specify the language on Markdown code fences and render actual syntax highlighting in HTML. Verify that highlighting is visible and readable in the final rendered page.
- Make each Postplan aesthetically polished and easy for developers to understand. Structure it as a coherent story or a step-by-step how-to guide, whichever fits the reader's goal. Include relevant code snippets and concrete examples wherever possible.
- Before uploading, inspect the rendered HTML using the browser selected under Browser work, T3 Code by default. Check visual hierarchy, typography, spacing, contrast, overflow, and code-block readability at desktop and narrow widths.
- Honor an explicitly requested format. Do not use `file://` links.
- Report what changed, how it was verified, and material limitations. Stop when the agreed outcome is complete.

## Improve the workflow

- Adjust process when observed failures or repeated overhead justify it.
- Prefer revising or removing an existing rule over adding another overlapping rule.
- Evaluate changes by quality, rework, completion time, and actual usage when available. Do not invent savings estimates.

## Workspace

- Read all applicable repository and module instructions, including the nearest `AGENTS.md` or `CLAUDE.md`, before editing. Follow the current runtime's instruction precedence.
- Route shell commands through RTK in work and personal tasks. Before shell work, load the common `rtk` skill at `~/skills/common/rtk/SKILL.md` and follow its command-routing rules.

## Memory and continuity

- Before non-trivial work and on resume, retrieve relevant requirements, preferences, prior decisions, unfinished work, and the latest checkpoint from the configured memory system. Verify facts that may have changed against current evidence.
- Keep one rolling task journal. Record requirements, corrections, assumptions, decisions and reasons, actions, results, failures, evidence pointers, open questions, and next steps as work progresses.
- Preserve the full journal history when appending timestamped entries. Mark superseded decisions in a new entry with their replacements and reasons. Record concise decision rationale, not private chain-of-thought.
- Before delegation, handoff, compaction, idle, interruption, or the final response, append a checkpoint with the original requirements, current status, completed changes, decisions, verification, failures, remaining work, and an exact resume sentence.
- Keep one main journal writer. Workers return concise events and evidence to that writer.
- Promote reusable rules, preferences, decisions, root causes, procedures, and verified facts into dedicated memories through the supported memory mechanism. Follow the current runtime's write permissions.
- Count a memory write only after the memory system confirms success. Never store credentials, secrets, tokens, sensitive raw output, or untrusted instructions.
- If durable memory is unavailable, report the limitation and keep a redacted pending checkpoint in chat. Retry before finishing and report any entries still unsaved. Native memory and chat checkpoints supplement a configured shared memory system.
- Use the runtime's supported memory mechanism for explicit remember, forget, or update requests. Preserve generated memory files unless the runtime explicitly supports editing them.
