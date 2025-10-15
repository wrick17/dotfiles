if [[ $- == *i* ]] && [ -f ~/.zshrc ]; then
  . ~/.zshrc
fi

. "$HOME/.cargo/env"