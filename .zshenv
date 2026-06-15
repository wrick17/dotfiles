# Environment variables only — zsh loads ~/.zshrc automatically for interactive shells.
# Do NOT source ~/.zshrc here; early sourcing breaks Warp terminal bootstrap.
[[ -f "$HOME/.cargo/env" ]] && . "$HOME/.cargo/env"
