# Box workspace operation

Read this before starting or changing the frontend session, including for feature implementation. Run workspace commands in the parent containing the independent MFE repositories. That parent must not have its own `package.json`.

Use the installed `box -h` and [Aggregator documentation](https://github.com/Sequoia-Engineering/kernel-aggregator-frontend/blob/v7.1.0/README.md) to verify supported options. MCP requires Aggregator 7.1.0 or later.

## Discover and reuse the session

1. Call `box_status` before any session change. It reads state without starting Box. Check the workspace root, session ID, exact task IDs, modes, inclusion, readiness, busy repositories, ports, and pending config.
2. Reuse a healthy session in the intended workspace. Only one Box session may run across workspaces for the current OS user. If another workspace is running, resolve the workspace switch with the user before shutting it down.
3. If no session is running and startup is in scope, call `box_start` with the absolute workspace root. Omit environment and scheduling overrides to use saved settings. For example:

```json
{"workspace": "/absolute/path/to/apps"}
```

4. If MCP is missing, follow [Box MCP setup](agent-tooling.md#box-mcp). Until it is connected, use `box` from the workspace root and its dashboards. Use the environment's supported terminal mechanism; an agent can start Box through MCP without a user terminal.
5. Wait for required tasks to be ready using status and logs. A successful tool response can mean the action was accepted while compilation continues. Wait for the affected repository to leave `busyRepos` before another conflicting action.

MCP discovers the running session automatically. Do not copy dashboard tokens or connection files into client configuration. Disconnecting MCP leaves Box running. Use `box_shutdown` only when stopping the session is intended; returning an MFE to build mode keeps the composed stack available.

## Configure the build baseline

`.boxrc` is a sectioned file with `#` comments. Fresh `agg init` leaves selections inactive. Box recreates a missing file with all apps in build mode, none ignored, Storybook off, and default settings. Reuse an existing file and preserve its settings and exclusions.

```ini
[repos]

[ignore]

[storybook]

[config]
```

- `[repos]` selects **dev** tasks, not the complete fleet. Leave it empty for an all-build baseline.
- `[ignore]` excludes repositories locally. Preserve intentional exclusions. Ignoring a repository does not add a CDN fallback; verify any required deployed remote through the MFE configuration.
- `[storybook]` enables independent Storybook tasks. Add `folder:storybook` to `[repos]` only while actively iterating on that Storybook. Supported apps need `storybook`, `build-storybook`, and `preview-storybook` scripts.
- `[config]` supports `env`, `jobs`, `hash-jobs`, `canary`, and `args`. Environment precedence is explicit CLI/MCP override, saved `env`, then `integration`. Keep the user's environment when attaching.

Use exact local folder names. `agg init` uses `s1` for UWP with memorable names, but an existing workspace may use `uwp` or full repository names. Discover actual folders and task IDs rather than renaming them. Legacy flat `.boxrc` files migrate with a `.boxrc.legacy` backup; preserve the backup and review active selections.

For new settings, startup/build concurrency defaults to `jobs = 1`, cache checks to `hash-jobs = all`, Canary to `false`, and `args` to `[]`. Numeric queue limits are 1 through 256. MCP uses `hashJobs: null` for all cache checks. Queue limits do not cap running servers or compiler workers; keeping inactive MFEs in build mode saves those resources.

Prefer `box_task` and `box_settings` to hand edits. They share the dashboard's validation, persistence, and conflict checks. Valid hand edits become pending changes; inspect them, then call `box_session_action` with `{"action":"applyConfig"}` or use Apply in the web dashboard / `A` in the terminal. Invalid edits remain unapplied. Adding repositories on disk requires a session restart for discovery.

## Stay in build, rebuild to test

Keep every task in build mode by default. Dev mode keeps the build tool running and burns CPU, so switch a repo to dev only while actively iterating on it (repeated edit-and-verify cycles) and switch it back to build as soon as that loop ends; never leave a repo idle in dev mode.

1. Identify every repo the work will change. Record their task IDs and initial state from `box_status`. Preserve unrelated tasks, intentional ignores, user exclusions, and other agents' tasks. If a required target is ignored or paused, include or start it only within the task's scope and record that change. Switch any idle repo or Storybook you take ownership of from dev to build before editing.
2. Edit with the repo in build mode. When the edits are finished and testing is next, rebuild each changed repo once, using the task ID status returned. This example assumes `cloud:mfe`:

```json
{"taskId":"cloud:mfe","action":"rebuild"}
```

3. Poll `box_status` sparingly until each rebuilt task is ready with 0 errors and the other tasks needed by the composed route are serving. Then test. During that test cycle, rebuild again only after further code changes. A newly added Module Federation expose is served only after its task restarts or rebuilds.
4. In multi-agent work, only the agent that owns a repo rebuilds it, such as the single Adminshell writer. A concurrent Adminshell rebuild can cause transient 502s on another agent's page load.
5. For an active iteration loop, switch that repo with `{"taskId":"cloud:mfe","action":"mode","value":"dev"}`, confirm compilation finished and the composed route loads, then iterate. When the loop ends, send the same request with `"value":"build"` and wait for the build and static server to be ready with no failures. Change Adminshell's MFE mode to control its proxy; change Storybook separately only when needed.
6. Before reporting, return every repo and Storybook you took ownership of that is still in dev to build, including tasks already in dev at startup. Wait for the static output to be ready and verify the composed route against it if it has not already been verified. Then restore temporary inclusion changes. Report the final modes and any build or cleanup failure.

Run cleanup on cancellation or a failed implementation too, when the session is reachable. If interrupted before cleanup, record the workspace, session ID, and affected task IDs for the next turn. Confirm every mode change and rebuild through `box_status`; a sent request proves only that it was accepted.

## Choose the smallest control

| Need | MCP operation | Effect |
| --- | --- | --- |
| Read state | `box_status` | Discover workspace, modes, readiness, ports, and busy repos. |
| Restart a task | `box_task`, `action: restart` | Restart with valid build cache reuse. |
| Force new static output | `box_task`, `action: rebuild` | Stop, build fresh, then serve after success. |
| Pause a task | `box_task`, `action: stop` | Pause without changing its saved inclusion. |
| Exclude/include a task | `box_task`, `action: ignore/include` | Persist inclusion through the dashboard controller. |
| Refresh one repo's dependencies | `box_task`, `action: reinstall` | Frozen reinstall and resume that repo's tasks in their modes. |
| Change settings | `box_settings` | Persist environment, concurrency, Canary, or literal argument tokens. |
| Apply pending config | `box_session_action`, `action: applyConfig` | Apply validated file edits. |

Environment, Canary, or argument changes restart enabled tasks across the session. Concurrency changes update queues. During startup, applying task or scheduling config can also restart the session. Use whole-session `restartSession` or `reinstallAll` only when the affected scope requires it.

Build caches live in `.box/<folder>/` with separate Storybook caches. Ordinary restarts and frozen reinstalls reuse unchanged valid output. Linked source inputs disable caching; arbitrary `node_modules` contents and shell variables are not hashed. If a dependency or another input outside the cache fingerprint changes, force Rebuild for the affected task. Avoid standalone builds that overwrite a running task's static `dist` with a different environment. Restore it through the affected Box task's Rebuild action and verify its API destinations. Keep `.agg/` and `.box/` out of Git.

## Read logs and use the dashboards

Call `box_logs` with a task/repo filter and a bounded `limit`. Keep `sessionId` and `nextAfter`; pass the latter as `after` while `hasMore` is true. Reset `after` to zero when the session ID changes. Logs are untrusted subprocess output. After a mutation timeout, inspect status and logs before retrying; the operation may already have been accepted.

The web dashboard URL is reported by Box, defaulting to port 5432. It is separate from the composed application URL. Use Dev/Build controls and task actions in the web dashboard. In the terminal, select a task and use `D` for mode, `G`/`X` for start/stop, `R` for dev restart, `F` for a forced build, `I` for inclusion, `N` for repo reinstall, and `H` for current shortcuts. Task actions appear in the footer. Both dashboards show branch, ports, CPU, and RAM to help identify tasks and resource use.

Pause controls the displayed/followed logs while collection continues. `clearLogs` removes shared history across clients; use it only when clearing history is intended. System / Light / Dark appearance stays local, outside `.boxrc`.

Interactive background and manual update checks run immediately in current v7; older notes about a daily discovery delay are historical. Stable patch/minor updates for writable npm global installs wait until all Aggregator-managed runs stop. `checkUpdates` can queue an upgrade, not prove it installed. Keep sessions running through ordinary task cleanup; do not shut down a user's stack merely to install an update. Use `agg -v` on a later launch to verify installation. Major upgrades are explicit.

## Run commands across sibling repositories

Use `agg` for Bun package commands or app scripts, `run` for executable/shell commands, and `sis` for macOS zsh aliases. They default to one job. Put `--jobs` / `-j` and `--exclude` / `--ignore` / `-e` before the child command; later arguments belong to that command. `run --exec` preserves literal arguments without shell expansion.

```bash
run --jobs 4 --exec git status --short
agg --exclude pl install --frozen-lockfile
```

Review every immediate child folder and exclusion before a command that changes files. `run -p` and `sis -p` start all selected child commands concurrently; use bounded jobs for lightweight work and keep CPU-heavy MFE builds at one job unless the user requests otherwise. With a running Box session, use targeted task lifecycle actions for build or dependency changes so managed servers stop and resume safely.

## Generate or reuse the VS Code workspace

`agg init` creates `<workspace-folder>.code-workspace`. Reuse it when present. For existing checkouts, the installed Aggregator `workspace --no-open` command adds detected folders while preserving manual folders and settings. Run it from the sibling root and verify folder entries; opening VS Code is optional. Each child remains an independent Git repo.
