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

If that file already exists, merge the `PreToolUse` entry from `ai/common/codex.hooks.json` into it. Restart Codex after installing the hook. This keeps the existing global instruction import in place. Verify the installation with `rtk --version` and `rtk gain`.

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

The installed `~/.codex/AGENTS.md` points to `ai/work/agents.md`, `~/.claude/CLAUDE.md` and `~/.plaude/CLAUDE.md` import `ai/work/claude.md`, and `~/.config/opencode/AGENTS.md` points to `ai/work/opencode.md`.

Codex files explicitly require reading their linked instructions. Claude files use native `@` imports. When installing a profile, keep the source hierarchy together and point the installed instruction file at the profile's absolute path in this repo.

Skills are grouped into `ai/skills/common`, `ai/skills/work`, and `ai/skills/personal`. `sequoia-frontend` is work only. Personal setups use common + personal; this machine uses common + work. Plugin-managed skills keep their existing installations.

On a fresh setup, link the shared skills directory into your home:

```sh
ln -s "$HOME/dotfiles/ai/skills" "$HOME/skills"
```

The agent skill directories, including `~/.claude/skills` and `~/.plaude/skills`, link to the relevant entries under `~/skills/common` or `~/skills/work`. `~/skills` points to `ai/skills`, so those agent links stay valid. Upstream checkouts stay in `ai/skills/.sources`, outside the parent Git history, so their Git metadata and local edits are preserved. `~/skills/update` still updates those existing checkouts.

On another machine, recreate these source checkouts before using the source-backed common skills:

```sh
mkdir -p "$HOME/dotfiles/ai/skills/.sources"
git clone git@github.com:cursor/plugins.git "$HOME/dotfiles/ai/skills/.sources/cursor-plugins"
git clone git@github.com:DietrichGebert/ponytail.git "$HOME/dotfiles/ai/skills/.sources/ponytail"
git clone git@github.com:mattpocock/skills.git "$HOME/dotfiles/ai/skills/.sources/mattpocock-skills"
git clone https://github.com/tt-a1i/archify.git "$HOME/dotfiles/ai/skills/.sources/archify"
```

The current upstream checkouts include local edits. Those edits remain in the local source repositories and need their own backup or publication to transfer to another machine.
