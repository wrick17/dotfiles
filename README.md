# Install stuff

```bash
cd ~

brew install fzf zoxide

touch ~/alias.zsh

git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc

p10k configure
```

> For `p10k configure` command choose whatever works for you. Mostly shell customization.


### iTerm > Settings > Profiles > General
* Title - Session Name (only this)
* Tick "Applications in terminal may change the title"