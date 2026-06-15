# Environment variables only — zsh loads ~/.zshrc automatically for interactive shells.
# Do NOT source ~/.zshrc here; early sourcing breaks Warp terminal bootstrap.
export PATH="$HOME/dotfiles/bin:$HOME/.local/bin:/opt/homebrew/bin:$PATH"
[[ -f "$HOME/.cargo/env" ]] && . "$HOME/.cargo/env"
