# Frontend environment setup and operation

Use the live machine, current repositories, and installed Aggregator help as authority. Review [Aggregator v7 setup](https://github.com/Sequoia-Engineering/kernel-aggregator-frontend/blob/v7.1.0/README.md) when installing or initializing a workspace.

## Choose the operating mode

- For help or diagnosis, inspect prerequisites and explain the failing step before applying the smallest authorized fix.
- For a setup or startup request, perform the in-scope tool installation, package access, workspace initialization or repair, MCP registration, and startup steps.
- Pause for authentication, secret entry, required system approval, unavailable company resources, or a change that would overwrite existing work.

## 1. Establish and audit the target

Discover the OS and architecture, sibling workspace root, fresh/setup/repair/startup scope, approved repositories and branches, available tools, dirty checkouts, `.boxrc`, and existing session/listeners. Prefer existing working tools. Do not print `.npmrc`, tokens, or dashboard connection files.

Use `box` by default. Keep an explicit requested environment or saved `.boxrc` environment; use `integration` only when neither exists. Keep every enabled MFE in build mode until work requires its dev server. See [workspace-tooling.md](workspace-tooling.md) for the editing lifecycle.

Workspace commands run in the parent containing child projects, without a parent `package.json`. Aggregator v7 rejects project commands from inside an MFE. Help, version, and upgrade can run from any directory. Check current platform support; macOS is verified, while real Linux and Windows integration validation remains limited in the v7.1.0 documentation.

Before touching an existing checkout, inspect its remote, branch, and status. Preserve dirty work, local links, and running servers. Do not replace existing checkouts as a setup shortcut.

## 2. Install missing prerequisites and package access

Resolve the Node version from current `.node-version`, `.nvmrc`, `package.json`, or approved company guidance. Reuse FNM or NVM when present; install only one manager if needed. Use current [FNM](https://github.com/Schniz/fnm) or [NVM](https://github.com/nvm-sh/nvm) instructions and configure the user's active shell. Verify Git, Node, npm, and the required OS utilities.

Bun must be globally available on `PATH` in a fresh terminal and the agent launch environment. A project's `node_modules/.bin/bun` does not satisfy Aggregator's requirement. If missing, guide the user through [Bun installation](https://bun.com/docs/installation); Aggregator does not install Bun, edit `PATH`, or request administrator access. Avoid automatically substituting a local Bun installation.

Reuse the user's GitHub SSH/HTTPS authentication and Sequoia package registry setup. Verify transport identity separately from GitHub CLI identity. Ask the user to complete organization SSO or enter package credentials through a secure flow when needed. Follow [GitHub's npm registry guidance](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry); installation needs `read:packages`. Never ask for a PAT in chat.

Keep TLS verification enabled. Diagnose the corporate CA, proxy, registry mapping, scope, expiry, and SSO rather than adding TLS bypasses.

Install Aggregator globally through npm using the existing authenticated registry:

```bash
npm install --global @sequoia-engineering/aggregator --registry=https://npm.pkg.github.com
agg -v
box -h
```

Use a writable user-owned npm prefix, without `sudo`. Prefer an existing MCP-capable installation. MCP needs 7.1.0 or later; use the normal `agg upgrade` path when an upgrade is needed and in scope. Writable npm global installations receive deferred stable patch/minor updates after all managed runs stop; links and project-local installs do not.

Immediately follow [Box MCP setup](agent-tooling.md#box-mcp) to register `box` in all detected installed harnesses. Do this when Aggregator was already present too. Read back each registration and verify accessible connections without changing a live session.

## 3. Initialize a fresh workspace

Prefer `agg init` over manual fleet cloning. Use a new empty target directory:

```bash
mkdir apps
cd apps
agg init
```

Interactive init asks for memorable names, PeopleLoop, Analytics, and dependency installation, defaulting to Yes, No, No, Yes. In a nonempty directory it first requires a new, unused child workspace name. Existing contents remain intact. Change into that child after setup. Noninteractive init requires an empty directory; `--yes` does not bypass this rule.

For an agent setup with the confirmed core fleet and no editor launch:

```bash
agg init --yes --no-open
```

Use `--optional pl,analytics` or `--all` only when those optional repositories are in scope. Use `--no-install` to defer dependency installation, or `--no-memorable-names` for full GitHub repo folder names. Verify available flags with `agg -h` before execution.

Core repositories clone on `dev`; optional PeopleLoop uses `Sequoia-US/pl-ui` on `main`, and Analytics uses `dev`. Memorable names include `s1` for UWP. Sessions use the actual folders on disk, so existing `uwp` checkouts need no rename.

Init clones concurrently, then performs sequential `agg install --frozen-lockfile` by default when dependencies are selected. Optional clone failures warn and continue; core clone or install failures stop setup. Completed checkouts survive failures and cancellation. Report skipped optional apps and the failing core step accurately before repairing the specific checkout or install.

Verify the resulting independent repositories, inactive sectioned `.boxrc`, and `<workspace-folder>.code-workspace`. Init selects no environment and starts no server. Keep the parent as a workspace container rather than a Git monorepo.

## 4. Repair or refresh existing checkouts

Use the existing sibling workspace. `agg init` in a populated workspace creates a new child workspace; it is not an in-place repair command.

Clone only missing approved repositories, preserving their approved names and branches. Repair remotes or branches only within authorized scope. For a stopped workspace, refresh dependencies from the sibling root with:

```bash
agg install --frozen-lockfile
workspace --no-open
```

If Box is running, prefer the affected repository's MCP `reinstall` action, which stops and resumes its tasks safely. Use `reinstallAll` only for a fleet-wide refresh. Diagnose the specific repository on failure and keep valid build cache reuse.

## 5. Start and verify Box

Follow [workspace-tooling.md](workspace-tooling.md) to reuse an existing session or start Box through `box_start` with the absolute sibling root. For human terminal startup:

```bash
box
```

Use `box --env stage` only when `stage` is requested; an explicit override wins over saved settings. Missing `.boxrc` is recreated by Box with all MFEs in build mode, none ignored, and Storybook off. Preserve existing selections and user work. `agg start` is deprecated and runs the full selected fleet in dev mode; use it only on explicit request.

Wait for required MFEs to finish compiling and serving. The dashboard URL is separate from the application URL. Discover the application's proxy/host URL from current configuration or runner output and verify the composed application with the harness's preferred browser. Check initial load, direct refresh, console, failed network requests, and an owned route.

If feature editing follows setup, switch only its owning MFEs to dev mode for HMR, then return them to build after verification. Setup alone needs no dev selection.

## 6. Troubleshoot from evidence

- **Wrong working directory:** use the sibling parent without its own `package.json` for workspace commands.
- **Missing MCP:** check version and `box mcp` support, then persist `box` in every installed harness. Report required client reloads; do not confuse saved config with a connected tool.
- **MCP discovery failure:** inspect session status and lock ownership. Older sessions or `--no-dashboard` sessions require an authorized relaunch with the current dashboard enabled. Remove an exact stale lock only after confirming its owner and managed processes stopped.
- **Another Box workspace is running:** reuse it only if it is the intended target; obtain agreement before replacing the user's session.
- **Port conflict:** identify the owning process and whether it is the desired existing stack. Preserve unrelated listeners.
- **Missing remote or blank page:** inspect task readiness, bounded logs, browser/network output, inclusion, and the owning federation configuration.
- **Stale static output:** use Rebuild for the affected task when an external input changed; ordinary restarts reuse valid caches.

If the user supplies a setup script, inspect its target folders, Git changes, installs, profile edits, credential handling, TLS settings, and startup command before execution. Prefer the v7 setup flow when the script would replace existing work or apply obsolete defaults.
