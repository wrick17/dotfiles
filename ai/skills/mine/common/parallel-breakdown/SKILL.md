---
name: parallel-breakdown
description: Break bigger work into independent chunks and run them in parallel. Use in the main thread at the start of any bigger task, such as a feature, product build, architecture, test framework or test cases, tooling, verification, or docs, manifests, and rules, and when replanning one.
---

# Parallel breakdown

Mandatory for every big-tier task under `orchestration.md`; small-tier tasks skip it. Apply with `orchestration.md` and the `delegation` skill, which set each chunk's owner role, model, and worker contract.

## Steps

1. Size the task. A bigger task has more than one deliverable, module, file group, or check. A big-tier task that has only one deliverable stays one chunk.
2. Split along existing seams: module, layer, package, service, test suite, platform, or doc set. Each chunk gets one outcome, its owned files or state, its inputs from other chunks, and its completion check. Merge a chunk into its neighbour when it is too small to repay its contract.
3. Map dependencies. Shared interfaces (types, API contracts, schemas, file layout, fixtures) become the first chunk. For a new feature, the smallest end-to-end path comes before the chunks that build on it.
4. Mark a chunk ready once its dependencies have landed with no unresolved blocking findings. Hold a chunk whose dependency has a blocking finding until the fix lands and passes its required checks. Keep one writer per shared file or resource.
5. Record the breakdown in the task list: chunk, owner role, dependencies, and check.
6. Dispatch all ready chunks in one batch so they run concurrently, then dispatch each further chunk the moment it becomes ready. Assign each writer's next chunk under the `delegation` skill.
7. As each chunk lands, send it to review and verification while its author starts its next chunk. Sol reviews consequential chunks for real defects. Authors' scoped checks cover the rest; Terra does not verify chunks one by one. Run these checks on a fixed snapshot of the landed chunk and its dependencies, such as a detached worktree of a `git stash create` ref taken after staging the chunk's new files, and name that snapshot in every finding and result. Route findings back to the author under the `delegation` skill. When a fix lands, repeat this step only for the reviews or checks that the fix could invalidate.
8. After every chunk and fix has landed and passed its required review and verification, send the combined affected flow to Terra for final verification.

Done when every part of the agreed scope belongs to exactly one chunk, every chunk has an owner and a check, every chunk was dispatched as soon as it became ready, and final verification ran after the last fix landed.

## Common splits

| Work | Split |
|------|-------|
| Feature or product | Interface contract first, then frontend, backend, data or migrations, and tests in parallel |
| Architecture | One chunk per subsystem or decision; competing designs in parallel only for consequential, hard-to-reverse choices |
| Test framework and cases | Harness and helpers first, then one chunk per module or suite |
| Tooling | One chunk per tool, script, or integration |
| Verification | One chunk per suite, module, platform, or flow |
| Docs, manifests, and rules | One chunk per file or doc set, one writer each |
