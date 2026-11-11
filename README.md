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

The common `rtk` skill routes commands through RTK and uses `rtk proxy` when full output is needed.

### Apply the AI setup on a machine

`ai/apply` applies the hooks and settings from this repo on one machine. Run it once by hand on each machine, with one `--account` per Claude Code account: the config directory, the profile (`work` or `personal`), and the default model. On this work machine, both accounts use the work rules:

```sh
rtk proxy ~/dotfiles/ai/apply --account ~/.claude work haiku --account ~/.plaude work opus
```

It saves that list to `~/.config/dotfiles/ai-accounts` (under `$XDG_CONFIG_HOME` when set), one `CONFIG_DIR PROFILE DEFAULT_MODEL` line per account. The file stays on the machine and is not committed. Later runs need no arguments. To change the list, run it again with the full new set of `--account` options; that replaces the saved list.

Each run does the following:

- Installs or updates the Agent Memory client (see below).
- Runs `ai/provision-claude.py` for every saved account.
- Links `~/.codex/hooks.json` to `ai/common/codex.hooks.json` when `~/.codex` exists and the file is missing. If a different `hooks.json` is already there, it leaves the file alone and prints a warning; merge the entries from `ai/common/codex.hooks.json` into it by hand.
- Sets this repo's `core.hooksPath` to `ai/git-hooks` (see below).
- Prints a short summary, and exits non-zero if any step failed.

After that first run, pulls re-apply the setup by themselves. The tracked `post-merge` hook (plain `git pull`, including fast-forward `git pull --rebase`) and `post-rewrite` hook (a `git pull --rebase` that replays local commits) run `ai/apply` when the pull changed anything under `ai/`. They never block or undo a pull: if `ai/apply` fails, the hook prints a warning and the fix command.

Some cases still need a manual `ai/apply`:

- A fresh clone. Git never runs hooks from a fresh clone, so run the first `ai/apply --account ...` yourself. Recreate the source checkouts under `ai/skills/third-party/.sources` first (see below), because the `archify` skill links into one.
- A pull through `jj`. It does not run git hooks. If that pull moved the Ponytail pin, also run `ai/skills/sync-ponytail`.
- Any other pull that skips the hooks, such as a `git pull --rebase` whose local commits were all dropped as already upstream. Run `ai/apply`.

#### Agent Memory

Each run installs the Agent Memory client from its checkout, `~/Projects/personal/memory` by default. To use another path on a machine, set `AGENT_MEMORY_SOURCE` in the shell that runs `ai/apply`. When the checkout is missing, or there is no Node 24 or newer on `PATH` or in fnm, the run prints a warning and skips this step. The rest of the setup still applies.

The step does the following:

- Turns on `facts.inject`, `facts.synthesis` and `loop_guard.enabled` in `~/.agent-memory/config.json`. It keeps every other key and the file's `0600` mode. It does not change `inject.enabled`.
- Runs the checkout's `local/agent-memory.mjs install` with an absolute Node path.
- Registers the hooks that `install` prints in every saved Claude account, and for Codex in a managed block in `~/.codex/config.toml`. Each command starts with the absolute Node path, so hooks also run from apps such as T3 Code that have no fnm on `PATH`. Reruns replace older agent-memory entries, including hand-written ones, and leave other hooks alone. Codex also loads `hooks.json`, so it prints a startup warning about hooks defined in two places. After the block changes, restart Codex and approve the changed hooks in `/hooks`.
- On macOS, loads the daily batch job with `launchctl bootstrap` unless it is already loaded. To load a changed plist, run `launchctl bootout gui/$(id -u)/com.agent-memory.batch`, then run `ai/apply` again.

Do these steps once on each machine. They need tokens, which never go in this repo:

1. Save the job token to the `token_file` named in `~/.agent-memory/config.json`.
2. Create a read-scoped token on the memory dashboard. Save it to `~/.agent-memory/read-token`, then run `chmod 600 ~/.agent-memory/read-token`.
3. Run `~/.agent-memory/bin/agent-memory doctor`.

Privacy: with `facts.synthesis` on, the client sends redacted command digests to the Codex CLI on your Codex subscription to propose repo facts, at most 3 calls per UTC day on each machine. Your Codex provider receives those digests.

Claude Code reloads hooks from `settings.json` while it runs. Codex loads hooks at start, so restart Codex after `hooks.json` changes, and approve new or changed hooks in `/hooks`.

Both runtimes get session hooks that run `ai/common/session-temp.sh` at `SessionStart` and `SessionEnd`. Claude accounts call the script by its absolute path in this repo, so script edits arrive with a pull. The Codex entries use `"$HOME/dotfiles/..."`, which the shell expands, so the repo must live at `~/dotfiles`. Codex caps `SessionEnd` hooks at 3 seconds.

Claude Code accounts have independent user settings, skills, and hooks. Each account's `CLAUDE.md` imports the shared rules from `ai/<profile>/claude.md` directly, so rule edits in this repo apply to every account. After the first apply, edit each account's local settings and skills as needed.

The provisioning helper points `CLAUDE.md` at the shared rules and removes rule snapshots left by older runs. It materializes skill symlinks, including nested symlinks, rewrites shared skill paths to account-local copies, and registers the session hooks: the work rules hook for work profiles, and the session temp hook for every profile. Reruns update those entries in place instead of adding copies. Existing settings and model choices are preserved; `--default-model` only seeds a missing choice. Changed files are backed up under `~/.local/state/claude-account-backups/` with private permissions. It leaves authentication, sessions, plugins, and caches alone. Reruns preserve account edits and do not relink skill snapshots to shared sources. Upstream skill updates require a deliberate edit to each account's local snapshot. Check the helper with `rtk proxy python3 ai/test-provision-claude.py`.

After sourcing `~/.zshrc` in a fresh terminal:

```sh
cc --model sonnet   # Enterprise work account
cc --model haiku    # Enterprise work account
pc --model opus     # Max personal account, subject to device policy
```

`cc` explicitly selects `~/.claude`; `pc` selects `~/.plaude`. Both call the executable directly. Keep `claude` unaliased: native `claude` follows an inherited `CLAUDE_CONFIG_DIR`, or Claude Code's default configuration when it is unset. Remove stale `pc` overrides from `~/.secrets.zsh`, or keep them identical to the dotfiles alias. Log in with the chosen launcher and `/login`. Keep `ANTHROPIC_API_KEY` unset for subscription use. Explicit config directories use their own `.claude.json`; the legacy implicit `~/.claude.json` is a separate file and is not migrated by provisioning.

In T3 Code, select Office for Enterprise Sonnet or Haiku, and the personal Claude provider for Max Opus. Keep the provider instances pinned to `~/.claude` and `~/.plaude` respectively. Requested model metadata is not proof of the model that answered; inspect the actual assistant transcript when checking routing.

On work machines, the personal provider launches Claude through `ai/work/claude-personal-t3`. The launcher reads the `~/.plaude` login from that account's Keychain item, passes the access token to `~/.local/bin/claude` on an inherited pipe descriptor, drops inherited API keys, OAuth tokens, base URLs, and `CLAUDE_CODE_USE_*` provider switches, and supplies host-managed settings that default to `claude-opus-5-5` with `opus`, `sonnet`, and `haiku` available. `--help`, `-h`, and `--version` pass straight through. Link it into place, backing up any existing file:

```sh
target="$HOME/.local/bin/claude-personal-t3"
mkdir -p "$HOME/.local/bin"
[ -e "$target" ] && [ ! -L "$target" ] && mv "$target" "$target.backup-$(date +%Y%m%d%H%M%S)"
ln -sfn "$HOME/dotfiles/ai/work/claude-personal-t3" "$target"
```

Then set only these provider fields in T3 Code's settings. Leave the other settings as they are, and do not copy `~/.t3` between machines:

| Instance | Driver | Display name | `homePath` | `binaryPath` |
| --- | --- | --- | --- | --- |
| `claude` | `claudeAgent` | Claude | `~/.plaude` | absolute path of `~/.local/bin/claude-personal-t3` |
| `claudeAgent` | `claudeAgent` | Office | `~/.claude` | unset |

Credentials stay in the local Keychain and are not part of this repo. The launcher does not refresh tokens. When the personal login is missing or expired, it exits with an error; run `pc`, log in again with `/login`, then restart the T3 session. Check the launcher with `rtk proxy python3 ai/work/test-claude-personal-t3.py`; the test uses synthetic credentials and mocks Keychain and exec.

Restart sessions after provisioning. Check each account-local SessionStart hook for missing imports and the reported account/config directory. Executables, project settings, and administrator policy still follow Claude Code's normal scopes. Plugin-managed installations and caches remain under their existing management.

AI instructions and skills live together under `ai/`:

```text
ai/
  common/
    codex.hooks.json
    session-temp.sh
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
    claude-personal-t3
    test-claude-personal-t3.py
  personal/
    agents.md
    claude.md
  skills/
    mine/          # the user's own skills, including rule skills
      common/
      work/
      personal/
    third-party/   # vendored agent-agnostic copies; archify links into its checkout
      common/
      work/
      personal/
      .sources/
    update
    sync-ponytail
  git-hooks/
    post-merge
    post-rewrite
  apply
  provision-claude.py
```

`ai/common/global.md` and `ai/common/orchestration.md` hold the always-loaded shared rules, kept short. Situational rules live in skills under `ai/skills/mine` (for example `agent-memory`, `delegation`, `browser-work`, `visual-reports`, and the work skills `sequoia-pr` and `github-accounts`); the core files list a trigger line for each. The common `agents.md` and `claude.md` add runtime rules. Work profiles import those rules and `ai/work/instructions.md`; personal profiles import only their common runtime rules. OpenCode's work profile imports the global and work rules directly.

Choose the profile for each machine. Personal machines use `ai/personal/agents.md` for Codex and `ai/personal/claude.md` for Claude Code. Work machines use `ai/work/agents.md` and `ai/work/claude.md`, for every Claude account on that machine; the OpenCode work profile is `ai/work/opencode.md`.

Codex files explicitly require reading their linked instructions. Claude files use native `@` imports. For Codex, keep the source hierarchy together and point its installed instruction file at the profile's absolute path in this repo. For Claude Code, use the provisioning helper so its imports resolve inside its own account directory.

For a personal machine, create `~/.codex/AGENTS.md` with:

```markdown
Read and follow [agents.md](/Users/wrick/dotfiles/ai/personal/agents.md) before starting any task. Resolve instruction links relative to each containing file, follow them recursively, and apply all imported rules. Stop and report a required file that cannot be read.
```

For Claude Code on a personal machine, run `ai/apply` with `personal` as each account's profile, for example `ai/apply --account ~/.claude personal opus`. Keep each account's `CLAUDE.md` and imported files local to that account. Merge additional rules into those local files.

Skills are grouped by owner, then profile: `ai/skills/mine/<profile>` holds the user's own skills and `ai/skills/third-party/<profile>` holds the rest. Every machine uses `common`; work machines add `work` and personal machines add `personal`. `sequoia-frontend` and the other work skills belong to work machines. Claude accounts link the user's own skills live, so edits apply at once, and keep an independent materialized copy of third-party skills. Plugin-managed skills keep their existing installations.

On a fresh setup, link the shared skills directory into your home:

```sh
ln -s "$HOME/dotfiles/ai/skills" "$HOME/skills"
```

If `~/skills` already exists as a directory, preserve its contents and update its `mine`, `third-party`, `update`, and `sync-ponytail` links to the matching entries under `ai/skills`. The work machine keeps that directory and its legacy skill aliases.

Codex discovers user skills through individual links in `~/.agents/skills`, each pointing at `../../skills/<owner>/<profile>/<skill>`; add a link for every skill in `mine/common` and the profile's `mine` folder. Claude Code discovers skills in each account's own `skills` directory. The provisioning helper links every skill in `mine/common` and `mine/<profile>` into each account on every run, backing up any copy it replaces, and removes links to own skills that no longer exist. It materializes third-party skills, preserving existing regular directories and unrelated entries. Fresh accounts receive common and selected-profile third-party skills. Existing accounts keep their current third-party skill set. Plugin-managed skills stay managed by their plugins.

Ponytail is installed as a plugin, not vendored. The `plugins.ponytail` entry in `ai/skills/third-party/sources.json` pins its release tag, and this repo is the only place that version is set. `ai/skills/sync-ponytail` installs that tag:

- **Claude Code:** for each of `~/.claude` and `~/.plaude` that exists, it sets the `ponytail` marketplace's `ref` to the tag in the account's `settings.json`, backing up the file first. It then re-adds the marketplace and reinstalls any copy not built from the tagged commit, keeping plugin data.
- **Codex:** when `codex` is installed, it writes a one-plugin local marketplace to `~/.local/state/ponytail-codex-marketplace`, because upstream's Codex catalog always points at `main`. It then installs from that marketplace and re-approves only Ponytail's hooks.
- **Check:** for each runtime, it runs the installed `SessionStart` hook and requires `PONYTAIL MODE ACTIVE`. It exits non-zero on any failure.

```sh
rtk proxy ~/skills/sync-ponytail
```

The provisioning helper sets this repo's `core.hooksPath` to `ai/git-hooks`. It leaves an existing different value alone and prints a warning. It also leaves `core.hooksPath` unset, with a warning, when the default hooks directory already has active hooks, because setting it would disable them. When a pull moves the pin, the git hooks' `ai/apply` run also runs `sync-ponytail`. A plain `ai/apply` run by hand does not check the pin. If the sync fails, the hook warns and keeps the pull; fix the error and rerun the script. The plugin supplies six namespaced skills, such as `/ponytail:ponytail`, plus `SessionStart`, `UserPromptSubmit`, and `SubagentStart` hooks. Those hooks run `node`, which must be on the `PATH` of the shell or app that launches the agent. Restart running agents after a sync.

Third-party skills from pstack and mattpocock are vendored into `ai/skills/third-party/common` as tracked, agent-agnostic copies: no product, host, or model names in their instructions. `ai/skills/third-party/sources.json` records each skill's upstream repository, path, and the upstream commit its copy is based on. Archify stays a link into its checkout because its only host names are brand-logo data. The rstack family, `mf`, and `pdf` have no recorded upstream and are maintained by hand.

Upstream checkouts stay in `ai/skills/third-party/.sources`, outside the parent Git history, as clean mirrors. Do not edit them; edit the vendored copy. `~/skills/update` fast-forwards each checkout and three-way merges upstream changes since the recorded commit into the vendored copies. It moves the Ponytail pin to the newest upstream `vX.Y.Z` tag, found over HTTPS, and runs `sync-ponytail`. Then it checks every vendored skill for host-specific wording:

```sh
rtk proxy ~/skills/update          # pull upstream, merge, then lint
rtk proxy ~/skills/update --lint   # lint only
rtk proxy python3 ~/skills/test-update.py
```

It prints `NOTE` lines for conflicts (markers left in the file), files that changed on both sides, and skills removed upstream, which it keeps as frozen copies, plus a moved Ponytail pin. It prints `HOST-SPECIFIC` lines for wording to make generic, and exits non-zero while any remain. Review the diff, resolve the notes, and commit. Then refresh each Claude account's copies, which backs up the old ones:

```sh
rtk proxy python3 "$HOME/dotfiles/ai/provision-claude.py" "$HOME/.claude" --profile work --default-model haiku --refresh-third-party
```

Restart running agents after changing instruction entrypoints, skill links, or hooks so new sessions load the updated setup.

On another machine, recreate these source checkouts before running `update`:

```sh
mkdir -p "$HOME/dotfiles/ai/skills/third-party/.sources"
git clone git@github.com:cursor/plugins.git "$HOME/dotfiles/ai/skills/third-party/.sources/cursor-plugins"
git clone git@github.com:mattpocock/skills.git "$HOME/dotfiles/ai/skills/third-party/.sources/mattpocock-skills"
git clone https://github.com/tt-a1i/archify.git "$HOME/dotfiles/ai/skills/third-party/.sources/archify"
```

Claude Code's user-scoped MCP servers live in each explicit config directory's `.claude.json`, or the legacy `~/.claude.json` for implicit launches. These files remain separate from the account's instruction and skill snapshots. This machine configures `homeassistant`, `browser-mcp`, `devtools`, `t3-code`, and `openai-api-key-local-confirmation`. Vercel already connects through Claude's own connector at the same endpoint. The confirmation server uses the installed OpenAI Developers plugin's script, so update its absolute path after a plugin version change. Codex app runtimes, computer use, Codex Security, disabled servers, and ChatGPT-only connector transports are not copied. T3 also injects its own thread-scoped tools when it launches Claude.

Every Claude account and Codex install, work and personal, needs the `agent_memory` server, because the shared rules make Agent Memory the primary memory. The provisioning helper does not manage MCP config, so add it once per Claude account directory and once for Codex, then sign in:

```sh
export CLAUDE_CONFIG_DIR="$HOME/.plaude"   # repeat for each account directory
claude mcp add --scope user --transport http agent_memory https://memory.wrick17.com/mcp
claude mcp login agent_memory   # or /mcp inside that account
codex mcp add agent_memory --url https://memory.wrick17.com/mcp
codex mcp login agent_memory
```

BothQ (`bothq`) stays a read-only legacy archive; no rule writes to it.

Run `claude mcp list` to check connections. Complete each client's OAuth sign-in with `claude mcp login homeassistant` and `claude mcp login t3-code`, or use `/mcp` inside Claude Code. Home Assistant uses a URL client ID with a matching local callback port. Keep account tokens in each client's supported credential storage. Existing claude.ai connectors stay managed by Claude.
