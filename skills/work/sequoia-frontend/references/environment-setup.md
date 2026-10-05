# Frontend environment setup and operation

Use the live machine, current repository configuration, and installed Aggregator CLI as the source of truth. The historical setup document and script are useful baselines, but their versions, repository list, ports, branches, and security workarounds can drift.

## Choose the operating mode

- If the user asks for help or is stuck, run read-only diagnostics first, explain the failing prerequisite, and guide or apply the smallest fix they authorize.
- If the user explicitly asks to set up or run the frontend, perform the normal in-scope installation, cloning, dependency, `.boxrc`, and startup steps on their behalf.
- Pause only for authentication or SSO in the user's browser, secret entry, `sudo` or other system approval, an unavailable company resource, disabling a security control, or a change that could overwrite existing work.

## 1. Establish the target

Confirm or discover:

- macOS or Linux and CPU architecture; if the current Box implementation does not support the platform, explain that limitation and ask whether the user wants the heavier `agg start` fallback;
- the exact workspace directory that will contain the sibling MFE repositories;
- whether this is a fresh setup, repair, dependency refresh, or startup only;
- the approved repository set and branches, using the companion workspace architecture reference as the baseline and current organization sources as authority;
- the requested environment, defaulting to `stage` only when the user has not specified one;
- the MFE or small set of MFEs the user will actively edit.

Default to `box`. Use `agg start` only when the user explicitly requests the full source-development loop. Never run workspace-wide Git or install commands from the rules repository or from inside one MFE.

## 2. Audit before changing anything

Check the OS, shell, available disk space, Git, SSH or HTTPS access, Node manager, Node, npm, Bun, Aggregator, workspace contents, repo branches and dirty state, `.boxrc`, `.box/`, and existing listeners. Do not print secrets or read token values from `.npmrc`.

Prefer existing working tools. Resolve the Node version from current `.node-version`, `.nvmrc`, `package.json`, or company setup source. Do not install both FNM and NVM or trust a version copied from an older document.

Before cloning over or updating an existing directory, inspect its remote, branch, and `git status --short`. Do not checkout, pull, clean, or replace files in a dirty repo without the user's confirmation.

## 3. Install external prerequisites

Install only missing prerequisites, using their current official instructions:

- Git, `curl`, SSH, and `unzip` where the platform does not already provide them.
- One Node manager: prefer the user's existing FNM or NVM. Follow the official [FNM](https://github.com/Schniz/fnm) or [NVM](https://github.com/nvm-sh/nvm) instructions; on macOS, prefer Homebrew for FNM when available. Configure only the user's active shell.
- The repo-required Node version, then verify `node --version` and `npm --version`.
- Bun from [Bun installation](https://bun.com/docs/installation), then verify `bun --version`.
- `@sequoia-engineering/aggregator` through the authenticated GitHub Packages registry with `bun install -g @sequoia-engineering/aggregator`, then verify with `agg -v` and `agg -h`.

For GitHub access:

1. Reuse an existing supported SSH key when possible; follow [GitHub's SSH-key check](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys).
2. Ask the user to complete organization SSO authorization when GitHub requires it.
3. Authenticate npm to `https://npm.pkg.github.com/` for `@sequoia-engineering` using [GitHub's npm-registry guidance](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry).
4. Ask the user to enter credentials directly into the secure terminal or browser flow. Never request or echo a PAT in chat.
5. Use only the package scopes required for the task. Installing packages needs `read:packages`; do not request `write:packages` unless publishing is also required.

Keep TLS verification enabled. Never set `strict-ssl=false` or `NODE_TLS_REJECT_UNAUTHORIZED=0` as a default. Diagnose the corporate CA, proxy, registry, or certificate chain first; require explicit user approval for any narrow temporary bypass.

## 4. Create or repair the sibling workspace

- Create the confirmed workspace directory.
- Clone only missing approved repositories from `Sequoia-Engineering`, using the configured SSH or HTTPS method and the current default or approved branch.
- Preserve existing repositories. Fix remotes or branches only with evidence and user approval.
- Keep every MFE as an independent Git checkout; do not initialize Git in the workspace container.
- From the workspace root, install dependencies with `agg install`. Do not run it from inside a child repo.
- Investigate and report the specific failing repo when installation fails; do not hide errors and claim the fleet succeeded.

## 5. Prepare the workspace tools

Follow [workspace-tooling.md](workspace-tooling.md) to check the recommended agent tools, generate the VS Code workspace when absent, and create the task-focused `.boxrc` before startup.

## 6. Start and verify the stack

Run from the sibling workspace root, using the selected environment:

```bash
box --env stage
```

Use `agg start --env stage` only when the user explicitly requests every MFE in source-development mode. Add CLI options only after verifying them with the current `box -h`, `agg -h`, or Aggregator source.

Before starting, reuse an existing healthy stack when possible and avoid duplicate listeners. If a conflicting process exists, identify it and ask before terminating it unless this agent started it during the current task.

The first Box build can take longer; subsequent cached starts should be lighter. Rebuild an edited remote when Box is serving a stale static bundle.

Wait until every required MFE finishes compiling. Use the URL reported by the current runner rather than assuming an older documented port. Verify the real composed application with the attached DevTools browser: initial load, direct refresh, console errors, failed network requests, and at least one owned route.

## 7. Troubleshoot from evidence

- **No `package.json`:** run `agg` or `box` from the sibling workspace root, not a child repo or unrelated directory.
- **Missing `.boxrc`:** create it with the exact local folders being edited; do not fall back to `agg start` unless the user asks.
- **401 or package install failure:** check registry mapping, token scope, token expiry, organization SSO, and package access without exposing the token.
- **SSH public-key failure:** inspect existing keys and agent state, then test `ssh -T git@github.com`; do not disable host-key checking.
- **Port already used:** identify the owning process and whether it is the desired existing stack; do not use an indiscriminate `kill -9` pipeline.
- **Missing remote or blank composed page:** confirm all required MFEs compiled, inspect runner output, browser console, network failures, and the owning repo's federation config.
- **Stale Box result:** inspect `.boxrc`, cache output, and the edited MFE; rebuild the affected remote before browser verification.

If the user supplies an automation script, inspect it before execution. Present its target workspace, repo and branch changes, profile edits, credential writes, global installs, TLS settings, and startup command. On macOS, verify the script does not require Bash features missing from the system Bash. Prefer the guided steps above when the script would mutate existing checkouts, duplicate credentials, disable TLS, or require an unsupported shell.
