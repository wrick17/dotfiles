# Only remap cd in interactive shells; non-interactive sessions (e.g. Cursor tasks)
# rely on the builtin cd command. cd cannot be a bin script — it must stay a shell alias/function.
if [[ -o interactive ]] && command -v z >/dev/null 2>&1; then
  alias cd="z"
fi

alias c="clear"
alias x="exit"
alias n="npm"
alias ni="npm install"
alias ns="npm start"
alias nd="npm run dev"
alias nb="npm run build"
alias nr="npm run"
alias npmplease="rm -rf node_modules/ && rm -f package-lock.json && npm install"
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
alias python="/usr/bin/python3"
alias pip="pip3"
alias foo="echo foo"

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

alias p="python"
