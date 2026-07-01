# Environment variables only — zsh loads ~/.zshrc automatically for interactive shells.
typeset -U path
path=("$HOME/dotfiles/bin" "$HOME/.local/bin" /opt/homebrew/bin $path)
export PATH
[[ -f "$HOME/.cargo/env" ]] && . "$HOME/.cargo/env"
