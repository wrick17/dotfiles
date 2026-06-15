# Only remap cd in interactive shells; non-interactive sessions (e.g. Cursor tasks)
# rely on the builtin cd command.
if [[ -o interactive ]] && command -v z >/dev/null 2>&1; then
  alias cd="z"
fi

# OMZ git plugin (zinit snippet) aliases gpr -> git pull --rebase.
# Reclaim gpr for ~/dotfiles/bin/gpr (gh pr create). Use ggpu for pull --rebase.
unalias gpr 2>/dev/null

alias ls="eza --all --color=always --long --icons=always --no-user --no-permissions"
alias lst="eza --all --color=always --long --icons=always --no-user --no-permissions --tree --level=2"
alias ll="ls"
alias cat="bat -p"
alias c="clear"
alias x="exit"
alias gst="git status"
alias ga="git add"
alias gc="git commit -m"
alias gp="git push origin HEAD"
alias n="npm"
alias ni="npm install"
alias ns="npm start"
alias nd="npm run dev"
alias nb="npm run build"
alias nr="npm run"
alias g="git"
alias gbc="git symbolic-ref --short HEAD"
alias gs="git stash -u"
alias gsp="git stash pop"
alias gb="git branch"
alias gbc="git rev-parse --abbrev-ref HEAD && git rev-parse --abbrev-ref HEAD | pbcopy"
alias glg="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative"
alias glc="git rev-parse HEAD && git rev-parse HEAD | pbcopy"
alias npmplease="rm -rf node_modules/ && rm -f package-lock.json && npm install"
alias ni="npm install"
alias gco="git checkout"
alias gca="git add . && git commit -m"
alias h="htop"
alias y="yarn"
alias ys="yarn start"
alias yb="yarn build"
alias yi="yarn install"
alias yra="yarn android-dev"
alias yri="yarn ios-dev"
alias yrid="yarn ios-dev-device"
alias yrip="yarn ios-prod-device"
alias yd="yarn dev"
alias yc="yarn compile"
alias code='NODE_OPTIONS="" code'
alias chrome='open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome_dev_test" --disable-web-security'
alias dnsclear='sudo dscacheutil -flushcache;sudo killall -HUP mDNSResponder'
alias a="agg"
alias as="agg start"
alias python="/usr/bin/python3"
alias pip="pip3"
alias foo="echo foo"
alias agent="cursor-agent"
alias nvm="fnm"

alias ymfe="yarn unlink @sequoiaconsulting/mfe-config-essentials ; yarn ; yarn link @sequoiaconsulting/mfe-config-essentials"
alias amfe="agg unlink @sequoiaconsulting/mfe-config-essentials ; agg ; agg link @sequoiaconsulting/mfe-config-essentials"

alias cr="cargo run"
alias cb="cargo build"
alias ca="cargo add"

DISABLE_AUTO_TITLE="true"

_set_tab_title() {
	# Warp manages its own tab titles via OSC; emitting \e]1; corrupts bootstrap.
	[[ "$TERM_PROGRAM" == "WarpTerminal" ]] && return
	echo -ne "\e]1;${PWD##*/}\a"
}
precmd_functions+=(_set_tab_title)

alias b="bun"
alias bs="bun start"
alias bi="bun install"
alias br="bun run"
alias bd="bun dev"
alias bb="bun run build"
alias ba="bun add"
alias bda="bun run app:dev"
alias bba="bun run app:build"
alias bp="bun run preview"
alias bt="bun run test"

alias p="python"

alias doctor="bunx -y react-doctor@latest . --verbose --no-ami -y"

alias claude="claude --dangerously-skip-permissions"
