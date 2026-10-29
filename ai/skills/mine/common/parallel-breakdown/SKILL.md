---
name: parallel-breakdown
description: Break bigger work into independent chunks and run them in parallel. Use in the main thread at the start of any bigger task, such as a feature, product build, architecture, test framework or test cases, tooling, verification, or docs, manifests, and rules, and when replanning one.
---

# Parallel breakdown

Mandatory for every main thread. Apply with `orchestration.md` and the `delegation` skill, which set each chunk's owner role, model, and worker contract.

## Steps

1. Size the task. A bigger task has more than one deliverable, module, file group, or check. A task that fits the main thread's bounded allowance stays one chunk.
2. Split along existing seams: module, layer, package, service, test suite, platform, or doc set. Each chunk gets one outcome, its owned files or state, its inputs from other chunks, and its completion check. Merge a chunk into its neighbour when it is too small to repay its contract.
3. Map dependencies. Shared interfaces (types, API contracts, schemas, file layout, fixtures) become the first chunk. For a new feature, the smallest end-to-end path comes before the chunks that build on it.
4. Group chunks into waves. A wave holds every chunk whose dependencies are met, with one writer per shared file or resource.
5. Record the breakdown in the task list: chunk, owner role, dependencies, and check.
6. Dispatch each wave in one batch so its chunks run concurrently. Integrate results as they arrive and start the next wave as soon as its dependencies land.
7. After the last wave, send the combined affected flow to verification under `orchestration.md`.

Done when every part of the agreed scope belongs to exactly one chunk, every chunk has an owner and a check, and every wave was dispatched together.

## Common splits

| Work | Split |
|------|-------|
| Feature or product | Interface contract first, then frontend, backend, data or migrations, and tests in parallel |
| Architecture | One chunk per subsystem or decision; competing designs in parallel only for consequential, hard-to-reverse choices |
| Test framework and cases | Harness and helpers first, then one chunk per module or suite |
| Tooling | One chunk per tool, script, or integration |
| Verification | One chunk per suite, module, platform, or flow |
| Docs, manifests, and rules | One chunk per file or doc set, one writer each |
