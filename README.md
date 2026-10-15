# Insanely Fast ZSH with Ghostty config

This hosts the dotfiles and aliases for an insanely fast and rich Terminal experience.

> NOTE: Backup your .zshrc before doing this.

**Install some essentials first**
```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
```

```bash
brew install fzf zoxide eza fd thefuck stow starship
```

> NOTE: All the following things needs to be done in the home folder. It won't work anywhere else.

```bash
cd ~
git clone git@github.com:wrick17/dotfiles.git
cd dotfiles
stow .
cd ~
```

```bash
touch ~/.hushlogin
touch ~/.secrets.zsh
```

Add your secrets like `GITHUB_TOKEN` and all to your secrets to `.secrets.zsh`

```bash
source ~/.zshrc
```

```bash
p10k configure
```

## AI instructions and skills

Install RTK, the CLI proxy required by `ai/common/global.md`, from its official Homebrew tap:

```sh
brew tap rtk-ai/tap
brew install rtk-ai/tap/rtk
rtk config --create
```

The common `rtk` skill routes commands through RTK and uses `rtk proxy` when full output is needed. For automatic command rewriting in Codex, link the shared hook configuration if `~/.codex/hooks.json` does not already exist:

```sh
ln -s "$HOME/dotfiles/ai/common/codex.hooks.json" "$HOME/.codex/hooks.json"
```

If that file already exists, merge the `PreToolUse` entry from `ai/common/codex.hooks.json` into it. Restart Codex after installing the hook.

For Claude Code, merge the same `PreToolUse` entry into `~/.claude/settings.json`, with `rtk hook claude` as the command. Keep the file's other keys. `~/.claude/settings.json` holds other settings, so it is edited in place rather than linked. Restart Claude Code after adding the hook. This keeps the existing global instruction import in place. Verify the installation with `rtk --version` and `rtk gain`.

AI instructions and skills live together under `ai/`:

```text
ai/
  common/
    codex.hooks.json
    global.md
    orchestration.md
    agents.md
    claude.md
  work/
    instructions.md
    agents.md
    claude.md
    opencode.md
  personal/
    agents.md
    claude.md
  skills/
    common/
    work/
    personal/
    .sources/
    update
```

`ai/common/global.md` holds shared rules. The common `agents.md` and `claude.md` add runtime rules. Work profiles import those rules and `ai/work/instructions.md`; personal profiles import only their common runtime rules. OpenCode's work profile imports the global and work rules directly.

Choose the profile for each machine. This personal setup uses `ai/personal/agents.md` for Codex and `ai/personal/claude.md` for Claude Code. Work setups use `ai/work/agents.md` and `ai/work/claude.md`; the OpenCode work profile is `ai/work/opencode.md`.

Codex files explicitly require reading their linked instructions. Claude files use native `@` imports. When installing a profile, keep the source hierarchy together and point the installed instruction file at the profile's absolute path in this repo.

For a personal setup, create `~/.codex/AGENTS.md` with:

```markdown
Read and follow [agents.md](/Users/wrick/dotfiles/ai/personal/agents.md) before starting any task. Resolve instruction links relative to each containing file, follow them recursively, and apply all imported rules. Stop and report a required file that cannot be read.
```

Create `~/.claude/CLAUDE.md` with Claude Code's native import syntax:

```text
@/Users/wrick/dotfiles/ai/personal/claude.md
```

Replace `/Users/wrick/dotfiles` with the checkout's absolute path on another machine. Merge these entries with existing instructions instead of overwriting unrelated rules.

Skills are grouped into `ai/skills/common`, `ai/skills/work`, and `ai/skills/personal`. `sequoia-frontend` is work only. Personal setups, including this machine, use common + personal. Plugin-managed skills keep their existing installations.

On a fresh setup, link the shared skills directory into your home:

```sh
ln -s "$HOME/dotfiles/ai/skills" "$HOME/skills"
```

If `~/skills` already exists as a directory, preserve its contents and update its `common`, `personal`, `work`, `.sources`, and `update` links to the matching entries under `ai/skills`. This machine keeps that directory and its legacy skill aliases.

Codex discovers user skills through individual skill links in `~/.agents/skills`; Claude Code uses `~/.claude/skills`. Link each skill containing `SKILL.md` from `~/skills/common` and the selected profile into those directories, except skills already supplied by an installed plugin. Preserve unrelated entries. On this machine, both runtimes use the official Ponytail plugin, so neither has duplicate standalone Ponytail links. Do not link `~/skills/work` skills into a personal runtime's skill directory.

Install Ponytail for Claude Code at user scope through its official marketplace:

```sh
claude plugin marketplace add DietrichGebert/ponytail --scope user
claude plugin install ponytail@ponytail --scope user
claude plugin list
```

The plugin supplies six namespaced skills, including `/ponytail:ponytail` and `/ponytail:ponytail-review`, plus its `SessionStart`, `UserPromptSubmit`, and `SubagentStart` hooks. Node.js must be available on the non-interactive shell's `PATH` for the hooks. Start a new Claude Code session or run `/reload-plugins` after installation. The preserved common source checkout remains available to other consumers.

Upstream checkouts stay in `ai/skills/.sources`, outside the parent Git history, so their Git metadata and local edits are preserved. `~/skills/.sources` points there, and `~/skills/update` updates those existing checkouts. Restart running agents after changing instruction entrypoints, skill links, or hooks so new sessions load the updated setup.

On another machine, recreate these source checkouts before using the source-backed common skills:

```sh
mkdir -p "$HOME/dotfiles/ai/skills/.sources"
git clone git@github.com:cursor/plugins.git "$HOME/dotfiles/ai/skills/.sources/cursor-plugins"
git clone git@github.com:DietrichGebert/ponytail.git "$HOME/dotfiles/ai/skills/.sources/ponytail"
git clone git@github.com:mattpocock/skills.git "$HOME/dotfiles/ai/skills/.sources/mattpocock-skills"
git clone https://github.com/tt-a1i/archify.git "$HOME/dotfiles/ai/skills/.sources/archify"
```

The current upstream checkouts include local edits. Those edits remain in the local source repositories and need their own backup or publication to transfer to another machine.

Claude Code's user-scoped MCP servers live in `~/.claude.json`, separate from these shared instructions and skills. This machine configures `homeassistant`, `browser-mcp`, `devtools`, `t3-code`, and `openai-api-key-local-confirmation`. Vercel already connects through Claude's own connector at the same endpoint. The confirmation server uses the installed OpenAI Developers plugin's script, so update its absolute path after a plugin version change. Codex app runtimes, computer use, Codex Security, disabled servers, and ChatGPT-only connector transports are not copied. T3 also injects its own thread-scoped tools when it launches Claude.

Run `claude mcp list` to check connections. Complete each client's OAuth sign-in with `claude mcp login homeassistant` and `claude mcp login t3-code`, or use `/mcp` inside Claude Code. Home Assistant uses a URL client ID with a matching local callback port. Keep account tokens in each client's supported credential storage. Existing claude.ai connectors stay managed by Claude.
