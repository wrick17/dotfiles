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

Claude Code accounts have independent user settings, skills, and hooks. Each account's `CLAUDE.md` imports the shared rules from `ai/<profile>/claude.md` directly, so rule edits in this repo apply to every account. Provision each account once, then edit its local settings and skills. On this work machine, both accounts use the work rules:

```sh
rtk proxy python3 "$HOME/dotfiles/ai/provision-claude.py" "$HOME/.claude" --profile work --default-model haiku
rtk proxy python3 "$HOME/dotfiles/ai/provision-claude.py" "$HOME/.plaude" --profile work --default-model opus
```

The helper points `CLAUDE.md` at the shared rules and removes rule snapshots left by older runs. It materializes skill symlinks, including nested symlinks, rewrites shared skill paths to account-local copies, and fixes the SessionStart hook path. Existing settings and model choices are preserved; `--default-model` only seeds a missing choice. Changed files are backed up under `~/.local/state/claude-account-backups/` with private permissions. It leaves authentication, sessions, plugins, and caches alone. Reruns preserve account edits and do not relink skill snapshots to shared sources. Upstream skill updates require a deliberate edit to each account's local snapshot. Check the helper with `rtk proxy python3 ai/test-provision-claude.py`.

After sourcing `~/.zshrc` in a fresh terminal:

```sh
cc --model sonnet   # Enterprise work account
cc --model haiku    # Enterprise work account
pc --model opus     # Max personal account, subject to device policy
```

`cc` explicitly selects `~/.claude`; `pc` selects `~/.plaude`. Both call the executable directly. Keep `claude` unaliased: native `claude` follows an inherited `CLAUDE_CONFIG_DIR`, or Claude Code's default configuration when it is unset. Remove stale `pc` overrides from `~/.secrets.zsh`, or keep them identical to the dotfiles alias. Log in with the chosen launcher and `/login`. Keep `ANTHROPIC_API_KEY` unset for subscription use. Explicit config directories use their own `.claude.json`; the legacy implicit `~/.claude.json` is a separate file and is not migrated by provisioning.

In T3 Code, select Office for Enterprise Sonnet or Haiku, and the personal Claude provider for Max Opus. Keep the provider instances pinned to `~/.claude` and `~/.plaude` respectively. Requested model metadata is not proof of the model that answered; inspect the actual assistant transcript when checking routing.

Restart sessions after provisioning. Check each account-local SessionStart hook for missing imports and the reported account/config directory. Executables, project settings, and administrator policy still follow Claude Code's normal scopes. Plugin-managed installations and caches remain under their existing management.

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
    claude-session-rules.sh
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

Choose the profile for each machine. Personal machines use `ai/personal/agents.md` for Codex and `ai/personal/claude.md` for Claude Code. Work machines use `ai/work/agents.md` and `ai/work/claude.md`, for every Claude account on that machine; the OpenCode work profile is `ai/work/opencode.md`.

Codex files explicitly require reading their linked instructions. Claude files use native `@` imports. For Codex, keep the source hierarchy together and point its installed instruction file at the profile's absolute path in this repo. For Claude Code, use the provisioning helper so its imports resolve inside its own account directory.

For a personal machine, create `~/.codex/AGENTS.md` with:

```markdown
Read and follow [agents.md](/Users/wrick/dotfiles/ai/personal/agents.md) before starting any task. Resolve instruction links relative to each containing file, follow them recursively, and apply all imported rules. Stop and report a required file that cannot be read.
```

For Claude Code on a personal machine, run the helper with `--profile personal` and the desired default model. Keep each account's `CLAUDE.md` and imported files local to that account. Merge additional rules into those local files.

Skills are grouped into `ai/skills/common`, `ai/skills/work`, and `ai/skills/personal`. `sequoia-frontend` belongs to work machines. A machine's profile selects the initial skill set. Each Claude account has an independent materialized copy. Personal machines use common + personal. Plugin-managed skills keep their existing installations.

On a fresh setup, link the shared skills directory into your home:

```sh
ln -s "$HOME/dotfiles/ai/skills" "$HOME/skills"
```

If `~/skills` already exists as a directory, preserve its contents and update its `common`, `personal`, `work`, `.sources`, and `update` links to the matching entries under `ai/skills`. The work machine keeps that directory and its legacy skill aliases.

Codex discovers user skills through individual links in `~/.agents/skills`; keep that existing setup. Claude Code discovers skills in each account's own `skills` directory. Use the provisioning helper to materialize them, preserving existing regular directories and unrelated entries. Fresh accounts receive common and selected-profile skills, excluding Ponytail skills supplied by the plugin. Existing accounts keep their current discovered skill set. Plugin-managed skills stay managed by their plugins.

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

Claude Code's user-scoped MCP servers live in each explicit config directory's `.claude.json`, or the legacy `~/.claude.json` for implicit launches. These files remain separate from the account's instruction and skill snapshots. This machine configures `homeassistant`, `browser-mcp`, `devtools`, `t3-code`, and `openai-api-key-local-confirmation`. Vercel already connects through Claude's own connector at the same endpoint. The confirmation server uses the installed OpenAI Developers plugin's script, so update its absolute path after a plugin version change. Codex app runtimes, computer use, Codex Security, disabled servers, and ChatGPT-only connector transports are not copied. T3 also injects its own thread-scoped tools when it launches Claude.

Run `claude mcp list` to check connections. Complete each client's OAuth sign-in with `claude mcp login homeassistant` and `claude mcp login t3-code`, or use `/mcp` inside Claude Code. Home Assistant uses a URL client ID with a matching local callback port. Keep account tokens in each client's supported credential storage. Existing claude.ai connectors stay managed by Claude.
