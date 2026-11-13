# Login shells (Codex runs `zsh -lc`) pass through /etc/zprofile, whose path_helper moves
# /opt/homebrew/bin ahead of the gh shim. Put the shim first again so gh picks the account per repo.
path=("$HOME/.config/t3-gh/bin" ${path:#$HOME/.config/t3-gh/bin})
