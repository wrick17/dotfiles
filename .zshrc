typeset -g POWERLEVEL9K_INSTANT_PROMPT=quiet
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Set the directory we want to store zinit and plugins
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"

# Download Zinit, if it's not there yet
if [ ! -d "$ZINIT_HOME" ]; then
  mkdir -p "$(dirname $ZINIT_HOME)"
  git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
fi

# Source/Load zinit
source "${ZINIT_HOME}/zinit.zsh"

# Add in Powerlevel10k
zinit ice depth=1; zinit light romkatv/powerlevel10k

# Zsh plugins — turbo-loaded (zinit `wait` ice) so they load right after the first
# prompt paints instead of blocking startup. compinit is deferred via atinit onto
# zsh-syntax-highlighting so zsh-completions' fpath additions land before it runs
# (same gated once-per-day dump logic as before, just moved).
zinit wait lucid for \
  depth"1" \
    Aloxaf/fzf-tab \
  depth"1" blockf \
    zsh-users/zsh-completions \
  depth"1" atload'!_zsh_autosuggest_start' \
    zsh-users/zsh-autosuggestions \
  depth"1" atinit'autoload -Uz compinit; if [[ -n "$HOME/.zcompdump"(#qN.mh+24) ]]; then compinit; else compinit -C; fi; zicdreplay' \
    zsh-users/zsh-syntax-highlighting

# OMZ git plugin aliases (gco, gp, gst, …) conflict with ~/dotfiles/bin/* scripts.
# Git completions come from zsh-completions; omit OMZP::git.
zinit ice wait lucid
zinit snippet OMZP::command-not-found

if [[ -o zle ]]; then
  bindkey -e
  bindkey '^[[A' history-search-backward
  bindkey '^[[B' history-search-forward

  # Ctrl+L: erase the visible screen AND the scrollback buffer.
  # \033[3J = erase saved (scrollback) lines — honoured by both Ghostty and cmux.
  # Ghostty's cmd+k is remapped in the Ghostty config to send \x0c (Ctrl+L) to
  # trigger this widget.
  # Timestamp guard: cmux echoes \x0c back to the pane after clear-history, which
  # would re-trigger this widget in a loop. The guard lets the first call through
  # and absorbs any re-invocations within 2s.
  zmodload zsh/datetime
  _LAST_CLEAR_TS=0
  _HAS_CMUX=$(( $+commands[cmux] ))
  _clear_scrollback() {
    local now=$EPOCHREALTIME
    printf '\033[3J'
    if (( now - _LAST_CLEAR_TS > 2 )); then
      _LAST_CLEAR_TS=$now
      if (( _HAS_CMUX )); then
        command cmux clear-history </dev/null >/dev/null 2>&1 &!
      fi
    fi
    zle .clear-screen
  }
  zle -N _clear_scrollback
  bindkey '^L' _clear_scrollback
fi

# History
HISTSIZE=5000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

export FZF_DEFAULT_COMMAND="fd --hidden --strip-cwd-prefix --exclude .git"
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND="fd --type=d --hidden --strip-cwd-prefix --exclude .git"

_fzf_compgen_path() {
  fd --hidden --exclude .git . "$1"
}

_fzf_compgen_dir() {
  fd --type=d --hidden --exclude .git . "$1"
}

show_file_or_dir_preview="if [ -d {} ]; then eza --tree --level=2 --color=always {} | head -200; else bat -n --color=always --line-range :500 {}; fi"

export FZF_CTRL_T_OPTS="--preview '$show_file_or_dir_preview'"
export FZF_ALT_C_OPTS="--preview 'eza --tree --color=always {} | head -200'"

_fzf_comprun() {
  local command=$1
  shift

  case "$command" in
    cd)           fzf --preview 'eza --tree --color=always {} | head -200' "$@" ;;
    export|unset) fzf --preview "eval 'echo \${}'"        "$@" ;;
    ssh)          fzf --preview 'dig {}'                   "$@" ;;
    *)            fzf --preview "$show_file_or_dir_preview" "$@" ;;
  esac
}

# Completion styling
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:z:*' fzf-preview 'eza -1 --color=always $realpath'
zstyle ':fzf-tab:complete:code:*' fzf-preview 'eza --tree --level=2 --color=always $realpath'

# Cache tool-generated init scripts (fzf/zoxide/fnm each fork+exec on every startup
# otherwise) — regenerate only when the binary itself is newer than the cache.
_zsh_cache_dir="${XDG_CACHE_HOME:-$HOME/.cache}/zsh-init"
mkdir -p "$_zsh_cache_dir"
_cache_eval() {
  local name=$1 bin=$2 cache="$_zsh_cache_dir/$1.zsh" bin_path
  shift 2
  bin_path=$(command -v "$bin") || return
  if [[ ! -s "$cache" || "$bin_path" -nt "$cache" ]]; then
    "$@" > "$cache" 2>/dev/null
  fi
  source "$cache"
}

if [[ -o zle ]]; then
  _cache_eval fzf fzf fzf --zsh
fi
_cache_eval zoxide zoxide zoxide init zsh
_cache_eval fnm fnm fnm env --use-on-cd

source "${HOME}/.alias.zsh"
source "${HOME}/.secrets.zsh"

export HOMEBREW_NO_AUTO_UPDATE=1
export NODE_TLS_REJECT_UNAUTHORIZED=0
export NODE_NO_WARNINGS=1

# bun completions
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# Android Studio's bundled JBR isn't registered with /usr/libexec/java_home, so this
# path is the only viable JDK for Android builds — but guard it in case this machine
# doesn't have Android Studio installed.
_android_studio_jbr="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
[[ -d "$_android_studio_jbr" ]] && export JAVA_HOME="$_android_studio_jbr"
unset _android_studio_jbr
export ANDROID_HOME="$HOME/Library/Android/sdk"

export PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:${JAVA_HOME:+$JAVA_HOME/bin:}$HOME/.antigravity/antigravity/bin:$HOME/Library/Application Support/fnm:$HOME/.npm-global/bin:$HOME/.local/bin:$HOME/.lmstudio/bin:$PATH"

# Dedupe PATH — zinit resets the -U attribute mid-load, so redeclare it here.
typeset -U path
path=($path)
