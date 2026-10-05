# Workspace tooling preflight

Load this reference only for environment setup, startup, or workspace repair. Run these checks from the directory containing the sibling MFE repositories.

## Recommend agent tools

Check the current agent's loaded skills, plugins, MCP servers, and configuration before suggesting another install. Do not treat an unavailable command in one shell as proof that an agent integration is missing.

If [Ponytail](https://github.com/DietrichGebert/ponytail) or [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) is absent, recommend it and read [agent-tooling.md](agent-tooling.md) for the official harness-specific setup. Suggest these integrations; change agent-wide configuration only when the user asks the agent to install them.

## Generate the VS Code workspace

The `workspace` command is installed by `@sequoia-engineering/aggregator`; never install or recommend a separate package for it. If `agg` works but `workspace` is unavailable, inspect or repair the current Aggregator installation before continuing.

1. Locate `*.code-workspace` in the sibling MFE root, without descending into child repositories.
2. If one exists, inspect its folder entries and reuse it. Do not generate duplicates.
3. If none exists, verify the installed Aggregator provides `workspace`, then run this from the sibling MFE root:

```bash
workspace
```

4. Verify that `<workspace-directory-name>.code-workspace` was created and contains the detected MFE folders.
5. Tell the user to open and use that file as their VS Code workspace. If the `code` CLI is available, the explicit command is `code <name>.code-workspace`.

The current Aggregator command may try another installed editor automatically. The generated `.code-workspace` file is still the artifact to use in VS Code. Do not move repositories or hand-author a second workspace file merely to change which editor opened.

## Create the Box configuration

Before running Box, ensure `.boxrc` exists in the sibling MFE root.

1. Identify the owning MFE from the task, route, source files, or repository remote. If setup is the only context and the active MFE cannot be inferred, ask the user which MFE or small set of MFEs they will edit.
2. When `.boxrc` is absent, create it immediately after the active MFE set is known.
3. Write each actively edited MFE's exact local folder name once, one per line. Include a host or shared MFE only when the user will edit it too.
4. Validate every entry against a sibling directory. Do not include comments, blank placeholders, remote names that differ from local folders, or nonexistent repositories.
5. When `.boxrc` already exists, preserve it unless the task needs a different dev set; show the proposed change before replacing the user's current selection.
6. Ensure the generated `.box/` directory is ignored by Git and never committed.

Keep the dev set small. Box runs listed MFEs in development mode and builds or serves the rest from its cache. A missing `.boxrc` is a configuration task, not a reason to fall back to `agg start`.
