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

## Shortcuts (`bin/`)

Commands live as scripts in `~/dotfiles/bin/` (on your PATH via `.zshenv`).

**Why scripts, not aliases?** Aliases only load in an interactive shell. Batch `zsh -c` skips aliases — scripts work everywhere.

**Works in:** Warp, iTerm, Terminal, Ghostty, Cursor, and any zsh session. Run `exec zsh` after dotfiles changes.

### Git

| Command | What it does |
|---------|----------------|
| `g` | git passthrough |
| `ga` | git add |
| `gb` | git branch |
| `gbc` | copy branch name |
| `gc` | commit with message |
| `gca` | add all + commit |
| `gco` | checkout |
| `glc` | copy commit sha |
| `glg` | pretty log |
| `gp` | push to origin |
| `gpr` | open PR (`-d` for draft) |
| `gs` / `gsp` | stash / stash pop |
| `gst` | status |
| `gprm` | merge PR for current branch |
| `ggpu` | pull + rebase from origin |
| `ggpum` | pull merge from origin |
| `gpi` | open GitHub issue for deploy |
| `aal` | agg add + link MFE package |
| `dmg` | create + open a `.dmg` from an app |

### agg / bun / tools / ls

| Command | What it does |
|---------|----------------|
| `a` | agg passthrough |
| `as` | agg start |
| `b` | bun passthrough |
| `bi` | bun install |
| `bs` | bun start |
| `br` | bun run … |
| `bd` | bun dev |
| `bb` / `ba` | bun run build / bun add |
| `bda` / `bba` | bun run app:dev / app:build |
| `bp` / `bt` | bun run preview / test |
| `doctor` | react-doctor via bunx |
| `claude` | claude with skip-permissions flag |
| `agent` | cursor-agent |
| `nvm` | fnm passthrough |
| `ls` / `ll` / `lst` | eza listing (tree for `lst`) |
| `cat` | bat -p |

**`cd` stays interactive-only** (alias to zoxide `z`). A bin script cannot change the current shell directory. In batch, use plain `cd` or the `z` command directly.

**Check it's wired up:**

```bash
whence -v gco b doctor ls
# should show ~/dotfiles/bin/...
```

**Note:** zsh only for dotfile loading. Bash/fish need `~/dotfiles/bin` on PATH manually.

### Still interactive-only (aliases in `.alias.zsh`)

| You type | Use in batch instead |
|----------|----------------------|
| `cd` | `cd` (builtin) or `z <dir>` |
| `y`, `yi`, `yd`, … (yarn) | full `yarn` commands |
| `n`, `ni`, `nd`, … (npm) | full `npm` commands |
| `amfe`, `ymfe` | run the full agg/yarn link commands |
| `cr`, `cb`, `ca` (cargo) | full `cargo` commands |

**`.secrets.zsh`** loads only in interactive zsh. Batch gets `.zshenv` only.

**fnm auto-switch on cd** is in `.zshrc`; batch `node` may differ from your terminal unless you use `fnm exec`.

### OMZ / other alias sources

| Source | Status | What it adds |
|--------|--------|----------------|
| `OMZP::git` | **Removed** | Was git aliases (`gco`, `gpr`, …) — conflicted with `bin/` |
| `OMZP::command-not-found` | **Still loaded** | Homebrew “did you mean …?” when a command is missing — not aliases |
| `.alias.zsh` | Active | yarn, npm, cargo, chrome, `cd=z`, etc. |
| zinit | Built-in only | `zi`/`zinit` shortcuts, `run-help=man` |

**Safe to remove (already done):** `OMZP::git`.

**Pending your OK:** `OMZP::command-not-found` — only adds install hints; no overlap with `bin/`. Removing it is fine if you don’t want any OMZ snippets left.
