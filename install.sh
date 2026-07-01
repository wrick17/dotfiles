#!/usr/bin/env bash
# Symlinks this repo into $HOME via stow. Backs up any real (non-symlink) file
# that would conflict, so stow can never silently skip a target the way it did
# for .zshenv (see README history: a stale pre-existing ~/.zshenv shadowed the
# repo's version for months because stow refuses to clobber real files).
set -euo pipefail
cd "$(dirname "$0")"

backup_dir="$HOME/.dotfiles-backup-$(date +%Y%m%d%H%M%S)"

for f in .[!.]*; do
	[[ -f "$f" ]] || continue
	target="$HOME/$f"
	if [[ -e "$target" && ! -L "$target" ]]; then
		mkdir -p "$backup_dir"
		echo "Backing up existing $target -> $backup_dir/$f"
		mv "$target" "$backup_dir/$f"
	fi
done

stow -v -t "$HOME" .

echo "Done. Run 'exec zsh' to pick up the new config."
[[ -d "$backup_dir" ]] && echo "Conflicting files backed up to: $backup_dir"
