# Set the directory we want to store zinit and plugins
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"

# Download Zinit, if it's not there yet
if [ ! -d "$ZINIT_HOME" ]; then
    mkdir -p "$(dirname $ZINIT_HOME)"
    git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
fi

# Source/Load zinit
source "${ZINIT_HOME}/zinit.zsh"

# Defer heavy init tasks until after the first prompt
zinit light romkatv/zsh-defer

# Load core completions plugin; run compinit in background (fast path)
# Ensure `zsh-users/zsh-completions` is available before compinit
zinit light zsh-users/zsh-completions

# Defer compinit fast path and zcompdump compilation
zsh-defer -c '
  autoload -Uz compinit
  COMPDUMP="${XDG_CACHE_HOME:-$HOME/.cache}/zsh/.zcompdump"
  mkdir -p "$(dirname "$COMPDUMP")"
  compinit -C -d "$COMPDUMP"
  if [ -s "$COMPDUMP" ]; then
    zcompile "$COMPDUMP" 2>/dev/null
  fi
  # After compinit exists, safely replay compdefs
  zinit cdreplay -q 2>/dev/null || true
'

# cdreplay moved to deferred compinit block above to ensure compinit is available

# Add in zsh plugins (deferred where safe to reduce initial latency)
zinit ice wait"1" lucid
zinit light Aloxaf/fzf-tab

zinit ice wait"1" lucid
zinit light zsh-users/zsh-autosuggestions

zinit ice wait"1" lucid
zinit light zsh-users/zsh-syntax-highlighting

zinit snippet OMZP::git
zinit snippet OMZP::yarn
zinit snippet OMZP::command-not-found

# Keybindings
bindkey -e
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward

# History
HISTSIZE=5000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups


export FZF_DEFAULT_COMMAND="fd --hidden --strip-cwd-prefix --exclude .git"
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND="fd --type=d --hidden --strip-cwd-prefix --exclude .git"

_fzf_compgen_path() {
  fd --hidden --exclude .git . "$1"
}

# Use fd to generate the list for directory completion
_fzf_compgen_dir() {
  fd --type=d --hidden --exclude .git . "$1"
}

show_file_or_dir_preview="if [ -d {} ]; then eza --tree --level=2 --color=always {} | head -200; else bat -n --color=always --line-range :500 {}; fi"

export FZF_CTRL_T_OPTS="--preview '$show_file_or_dir_preview'"
export FZF_ALT_C_OPTS="--preview 'eza --tree --color=always {} | head -200'"

# Advanced customization of fzf options via _fzf_comprun function
# - The first argument to the function is the name of the command.
# - You should make sure to pass the rest of the arguments to fzf.
_fzf_comprun() {
  local command=$1
  shift

  case "$command" in
    cd)           fzf --preview 'eza --tree --color=always {} | head -200' "$@" ;;
    export|unset) fzf --preview "eval 'echo ${}'"         "$@" ;;
    ssh)          fzf --preview "dig {}"                  "$@" ;;
    *)            fzf --preview "$show_file_or_dir_preview" "$@" ;;
  esac
}

# Completion styling
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:z:*' fzf-preview 'eza -1 --color=always $realpath'
zstyle ':fzf-tab:complete:code:*' fzf-preview 'eza --tree --level=2 --color=always $realpath'

export PATH=/opt/homebrew/bin:$PATH
export HOMEBREW_NO_AUTO_UPDATE=1
export NODE_OPTIONS="--no-warnings"
export NODE_TLS_REJECT_UNAUTHORIZED=0

# Defer non-essential shell integrations (interactive shells only)
if [[ -o interactive ]]; then
  zsh-defer -c 'eval "$(fzf --zsh)"'
  zsh-defer -c 'eval "$(zoxide init zsh)"'
fi

# Keep fnm early to ensure Node is ready for immediate use
eval "$(fnm env --use-on-cd)"
# Lazy-load thefuck to avoid Python startup cost on shell init
if command -v thefuck >/dev/null 2>&1; then
  fuck() {
    eval "$(thefuck --alias)"
    fuck "$@"
  }
fi
if [[ -o interactive ]]; then
  eval "$(starship init zsh)"
fi

source "${HOME}/.alias.zsh"
source "${HOME}/.secrets.zsh"

# bun completions (deferred)
if [[ -o interactive ]]; then
  zsh-defer -c '[ -s "${HOME}/.bun/_bun" ] && source "${HOME}/.bun/_bun"'
fi

export EDITOR="cursor"
export VISUAL="cursor"

# Enable profiling only when explicitly requested
if [ -n "$ZSH_PROF" ]; then
  zmodload zsh/zprof
fi