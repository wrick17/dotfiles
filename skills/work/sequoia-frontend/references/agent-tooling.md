# Agent tooling by harness

Read the relevant section when an integration is missing or installation is requested. Box MCP setup is automatic whenever Aggregator is present, including immediately after installing it. Ponytail and browser integrations remain recommendations unless their installation is requested. Verify current client instructions because configuration commands can change.

## Box MCP

Aggregator includes the stdio server; there is no separate MCP package to install. Follow [Aggregator's MCP guide](https://github.com/Sequoia-Engineering/kernel-aggregator-frontend/blob/v7.1.0/docs/mcp.md), using **`box`** as the client registration name for this skill rather than the guide's example name `sequoia-box`.

1. Check `node`, globally available `bun`, `box`, `agg -v`, and `box -h`. MCP support starts at Aggregator 7.1.0 and help lists `box mcp`. If an installed release is older, use its authenticated npm upgrade path when setup is authorized. If an update cannot be installed yet, report that blocker and use the existing dashboard; never guess credentials or interrupt a live session to upgrade it.
2. Discover installed harnesses through executables, installed apps/extensions, and their user configuration. After installing Aggregator, or when it is already present, install each missing `box` registration across **all detected installed harnesses**. Do not install another harness merely to add MCP. Prefer user/global scope so future sessions in other workspaces can use it.
3. Inspect the existing `box` entry in each client before writing. Reuse a correct registration. Preserve other servers, unrelated settings, file permissions, and any intentional tool restrictions. If `box` already names an unrelated server, resolve the name collision with the user instead of overwriting it. If Box is registered under another name, use the client's supported rename or migration to `box` without leaving duplicate Box processes or losing its settings.
4. Use the supported CLI or settings mechanism for each detected client. These commands register the installed executable, without a workspace binding or dashboard credentials:

| Harness | Persistent setup |
| --- | --- |
| Codex CLI/editor | Inspect `codex mcp get box`; if absent, run `codex mcp add box -- box mcp`. |
| Claude Code | Inspect `claude mcp get box`; if absent, run `claude mcp add --transport stdio --scope user box -- box mcp`. |
| Gemini CLI | Run `gemini mcp add --scope user --transport stdio box box mcp` when absent from its user config. |
| Cursor | Merge the JSON entry below into `~/.cursor/mcp.json`. |
| VS Code | Use `code --add-mcp '{"name":"box","type":"stdio","command":"box","args":["mcp"]}'` for the intended user profile, or merge the entry under `servers` in that profile's MCP settings. |
| Claude Desktop | Merge the JSON entry into its `claude_desktop_config.json` through its documented local-server configuration. |
| OpenCode | Merge `"box": {"type":"local","command":["box","mcp"],"enabled":true}` under `mcp` in the user `opencode.json`, checking the installed version's schema. |
| T3 Code and other installed MCP clients | Use their supported persistent MCP settings with name `box`, transport stdio, command `box`, arguments `["mcp"]`. Verify their schema; some clients use `servers` or a command array instead of `mcpServers`. |

```json
{
  "mcpServers": {
    "box": {
      "command": "box",
      "args": ["mcp"]
    }
  }
}
```

Merge this entry into existing configuration; do not replace the whole file with the example. For GUI clients with a restricted environment, use a stable absolute Box executable path and ensure Node and global Bun are on that client's `PATH`. Avoid ephemeral shell-session paths. `box --no-dashboard` cannot be controlled through MCP, so retain the default dashboard.

5. Read back each registration. Reload through the client's supported mechanism when possible without disrupting user work. If a reload or restart needs user action, report it as pending. Configuration alone does not prove tools are connected.
6. Verify a real MCP `tools/list` exposes `box_status`, `box_start`, `box_shutdown`, `box_task`, `box_settings`, `box_session_action`, and `box_logs`. Call `box_status`; a valid `running: false` also proves connectivity. Check each client when its connection is accessible, and distinguish a direct server handshake from a verified in-client connection. Verification must not start, stop, restart, or mutate an existing Box session.

Report installed/reused registrations, verified connections, and any blocked harness or required reload. Re-check missing registrations on subsequent setup runs. Multiple agents may attach to the same session; disconnecting one does not shut it down.

Current client references: [Gemini CLI](https://geminicli.com/docs/tools/mcp-server/), [Cursor](https://prod.cursor.com/help/customization/mcp), [VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers), [Claude Desktop](https://modelcontextprotocol.io/docs/develop/connect-local-servers), and [OpenCode](https://docs.opencode.ai/docs/mcp-servers/). Use the client docs for other detected harnesses before changing their configuration.

## Ponytail

Use [Ponytail's official install section](https://github.com/DietrichGebert/ponytail#install). Prefer its plugin or extension when one exists; otherwise install the matching instruction file.

| Harness | Official setup |
| --- | --- |
| Codex CLI/Desktop | Run `codex plugin marketplace add DietrichGebert/ponytail`, then `codex plugin add ponytail@ponytail`. Review the two hooks in `/hooks`, restart, and open a new thread. |
| Claude Code/Desktop | Send `/plugin marketplace add DietrichGebert/ponytail` and `/plugin install ponytail@ponytail` as two separate prompts, then restart. |
| Cursor | Copy the upstream `.cursor/rules/ponytail.mdc` into the project's `.cursor/rules/`. |
| GitHub Copilot CLI | Run `copilot plugin marketplace add DietrichGebert/ponytail`, then `copilot plugin install ponytail@ponytail`. |
| GitHub Copilot Chat | Copy the upstream `.github/copilot-instructions.md` into the project. |
| Gemini CLI | Run `gemini extensions install https://github.com/DietrichGebert/ponytail`. |
| OpenCode | Add `"plugin": ["@dietrichgebert/ponytail"]` to `opencode.json`. |
| Cline | Copy the upstream `.clinerules/ponytail.md` into the project. |
| Windsurf | Copy the upstream `.windsurf/rules/ponytail.md` into the project. |
| Kiro | Copy the upstream `.kiro/steering/ponytail.md` into the project or user steering directory. |
| Pi | Run `pi install git:github.com/DietrichGebert/ponytail`. |
| Other harnesses | Use the exact adapter or instruction file named in the current upstream install section; do not translate another harness's plugin command. |

The Codex and Claude plugins need Node.js on the non-interactive shell's `PATH`. Do not duplicate an existing plugin, rule, or instruction file.

## Chrome DevTools MCP

Use [Chrome DevTools MCP's official client configuration](https://github.com/ChromeDevTools/chrome-devtools-mcp#readme). Confirm Node.js LTS, npm, and current stable Google Chrome first. The server can inspect and modify browser data, so explain the access boundary and reuse the user's intended browser profile or isolated profile.

| Harness | Official setup |
| --- | --- |
| Codex | `codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest` |
| Claude Code | `claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest` |
| Cursor | Add the standard configuration below in Cursor Settings → MCP. |
| GitHub Copilot / VS Code | On macOS/Linux run `code --add-mcp '{"name":"io.github.ChromeDevTools/chrome-devtools-mcp","command":"npx","args":["-y","chrome-devtools-mcp"],"env":{}}'`. |
| Gemini CLI | `gemini mcp add -s user chrome-devtools npx chrome-devtools-mcp@latest` |
| OpenCode | Add a local MCP entry with command `npx -y chrome-devtools-mcp@latest` in `opencode.json`, following the upstream OpenCode example. |
| Cline, Windsurf, Roo Code, and other MCP clients | Add the standard configuration below through that client's documented MCP settings. |

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

Usage statistics are enabled by default. When relevant, explain the upstream `--no-usage-statistics` or `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS` opt-out before installation. Restart or reload the harness after configuration, verify the server is connected, and run one harmless browser inspection before relying on it for application verification.
