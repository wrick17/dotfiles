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

`ai/global.md` holds shared rules. `ai/agents.md` and `ai/claude.md` add runtime rules. `ai/work.md` holds shared work policies; `work.agents.md` and `work.claude.md` import it alongside their runtime instructions. `personal.agents.md` selects the personal Codex setup. The installed `~/.codex/AGENTS.md` points to `ai/work.agents.md`, and `~/.claude/CLAUDE.md` imports `ai/work.claude.md`, so the rules come from this repo.

Codex files explicitly require reading their linked instructions. Claude files use native `@` imports. When installing a profile, keep the source hierarchy together and point the installed instruction file at the profile's absolute path in this repo.

Skills are grouped into `skills/common`, `skills/work`, and `skills/personal`. `sequoia-frontend` is work only. Personal setups use common + personal; this machine uses common + work. Plugin-managed skills keep their existing installations.

Link only the shared skills directory into your home with Stow:

```sh
stow --dir "$HOME/dotfiles" --target "$HOME" --ignore '^(?!skills(?:/|$)).*' .
```

The agent skill directories link to the relevant entries under `~/skills/common` or `~/skills/work`. Upstream checkouts stay in `skills/.sources`, outside the parent Git history, so their Git metadata and local edits are preserved. `~/skills/update` still updates those existing checkouts.

On another machine, recreate these source checkouts before using the source-backed common skills:

```sh
mkdir -p "$HOME/dotfiles/skills/.sources"
git clone git@github.com:cursor/plugins.git "$HOME/dotfiles/skills/.sources/cursor-plugins"
git clone git@github.com:DietrichGebert/ponytail.git "$HOME/dotfiles/skills/.sources/ponytail"
git clone git@github.com:mattpocock/skills.git "$HOME/dotfiles/skills/.sources/mattpocock-skills"
git clone https://github.com/tt-a1i/archify.git "$HOME/dotfiles/skills/.sources/archify"
```

The current upstream checkouts include local edits. Those edits remain in the local source repositories and need their own backup or publication to transfer to another machine.
