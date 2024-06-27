# Insanely Fast ZSH

This hosts the dotfiles and aliases for an insanely fast and rich Terminal experience.

> NOTE: All the following things needs to be done in the home folder. It won't work anywhere else.

```bash
cd ~

touch ~/.hushlogin
touch ~/.secrets.zsh

brew install fzf zoxide eza fd thefuck stow

cd ~
git clone git@github.com:wrick17/dotfiles.git
cd dotfiles
stow .
cd ~

git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
```

```bash
p10k configure
```

> For `p10k configure` command choose whatever works for you. Mostly shell customization.

Add your secrets like `GITHUB_TOKEN` and all to your `.secrets.zsh`

```bash
source ~/.zshrc
```

And you're good to go!

## iTerm Settings

#### iTerm > Settings > Profiles > General
* Title - Session Name (only this)
* Tick "Applications in terminal may change the title"

#### iTerm > Settings > Profiles > Text
* Font `MesoLGS NF`
