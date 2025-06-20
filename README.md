# Insanely Fast ZSH with Ghostty config

This hosts the dotfiles and aliases for an insanely fast and rich Terminal experience.

> NOTE: Backup your .zshrc before doing this.

**Install Ghostty first**
```bash
brew install --cask ghostty
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
