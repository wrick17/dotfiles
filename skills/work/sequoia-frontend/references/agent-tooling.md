# Agent tooling by harness

Read this only when Ponytail or Chrome DevTools MCP is missing or the user asks to install agent tooling. Verify current upstream instructions before acting because plugin and MCP commands can change.

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
