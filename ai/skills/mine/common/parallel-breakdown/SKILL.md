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
7. As each chunk lands, its author starts its next chunk. Authors run only the build-and-load checks from `global.md`; no chunk gets its own review or test run. The one exception is the shared-interface chunk from step 3: Sol reviews it before dependent chunks start, and its findings go back to its author under the `delegation` skill.
8. After every chunk has landed, run one test phase over the combined scope. Sol reviews the consequential changes for real defects while Terra verifies the combined affected flow. Collect all findings, route them to their authors in one batch under the `delegation` skill, and re-run only the reviews and checks the fixes could invalidate.

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
