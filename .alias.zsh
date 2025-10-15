# Only remap cd in interactive shells; non-interactive sessions (e.g. Cursor tasks)
# rely on the builtin cd command.
if [[ -o interactive ]] && command -v z >/dev/null 2>&1; then
  alias cd="z"
fi
alias ls="eza --all --color=always --long --icons=always --no-user --no-permissions"
alias lst="eza --all --color=always --long --icons=always --no-user --no-permissions --tree --level=2"
alias ll="ls"
alias cat="bat -p"
alias c="clear"
alias x="exit"
alias gst="git status"
alias ga="git add"
alias gc="git commit -m"
function pull() {
	branch="$(git rev-parse --abbrev-ref HEAD)"
	if [ $# -eq 0 ]; then
		git pull origin $branch --rebase
	else
		git pull origin $1 --rebase
	fi
}
alias ggpu=pull
function pullMerge() {
	branch="$(git rev-parse --abbrev-ref HEAD)"
	if [ $# -eq 0 ]; then
		git pull origin $branch
	else
		git pull origin $1
	fi
}
alias ggpum=pullMerge
function gpi() {
	branch=$(git symbolic-ref --short HEAD)
	remote=$(git config --get remote.origin.url)
	removeDotGit="${remote/.git/}"
	removeColon="${removeDotGit/://}"
	url=${removeColon/git\@/https:\/\/}
	open "${url}/issues/new?title=deploy%20${branch}"
}
function _gpr_usage() {
	echo "
Usage: gpr <[options]>

Options:
	-j   --jira           Jira ticket id
	-d   --description    Description
	-t   --title          Title
	-h   --help           Help

NOTE: You have to provide description and either jira or title.

Example:

# Create a PR from master to dev branch
gpr master dev -t \"master dev sync\" -d \"rebase dev with master\"

# Create a PR from dev to current branch to dev branch with proper title and description accroding to PR template
gpr dev -j \"PRDS-1234\" -d \"fix a big bug\"
"
}
function gprm() {
	branch=$(git symbolic-ref --short HEAD)
	remote=$(git config --get remote.origin.url)
	removeDotGit="${remote/.git/}"
	removeColon="${removeDotGit/://}"
	url=${removeColon/git\@/https:\/\/}
	if [ $1 ]; then
		secondArg=$1
	else
		secondArg="dev"
	fi
	count=0
	title=""
	description=""
	while (($#)); do
		case $1 in
		-t=* | --title=*) title="${1#*=}" ;;
		-d=* | --description=*) description="${1#*=}" ;;
		*) if [ $count -eq 1 ]; then
			branch=$secondArg
			target=$1
		else target=$1; fi ;;
		esac
		count=$((count + 1))
		shift
	done

	if [ $count -eq 0 ]; then
		base="${url}/compare/${branch}"
	else
		base="${url}/compare/${target}...${branch}"
	fi
	temp="${base}?expand=1"

	if [ $title ] && [ $description ]; then
		temp="${temp}&title=${title}&body=${description}"
	elif [ $title ]; then
		temp="${temp}&title=${title}"
	elif [ $description ]; then
		temp="${temp}&body=${description}"
	fi

	open "${temp}"

	unset target
	unset count
	unset title
	unset description
	unset secondArg
	unset final
}
function gpr() {
	branch=$(git symbolic-ref --short HEAD)
	remote=$(git config --get remote.origin.url)
	removeDotGit="${remote/.git/}"
	removeColon="${removeDotGit/://}"
	url=${removeColon/git\@/https:\/\/}

	if [ $1 ]; then
		secondArg=$1
	else
		secondArg="dev"
	fi
	count=0

	if [ $# -eq 0 ]; then
		_gpr_usage
		return 0
	fi

	while (($#)); do
		case $1 in
		-j | --jira)
			shift
			ticket="${1}"
			;;
		-d | --description)
			shift
			description="${1}"
			;;
		-t | --title)
			shift
			title="${1}"
			;;
		-h | --help) _gpr_usage ;;
		*)
			shift
			;;
		esac
		count=$((count + 1))
	done

	target=$secondArg

	if [ $count -eq 0 ]; then
		base="${branch}"
	else
		base="${target}"
		head="${branch}"
	fi

	body="${description}"

	if [ $title ] || [ $ticket ]; then
		if [ $ticket ]; then
			title="${ticket} ${description}"
			body="### Description
Jira Id: ${ticket} 
Link to Jira Ticket: https://sequoiacg.atlassian.net/browse/${ticket} 
Remarks: ${description}"
		fi

		gh pr create --base "${base}" --head "${head}" --title "${title}" --body "${body}"
	fi

	unset target
	unset count
	unset title
	unset ticket
	unset body
	unset description
	unset secondArg
	unset final
	unset base
	unset head
}
alias gprm=gprm
alias gpr=gpr
alias gpi=gpi
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
alias nvm="fnm"

alias ymfe="yarn unlink @sequoiaconsulting/mfe-config-essentials ; yarn ; yarn link @sequoiaconsulting/mfe-config-essentials"
alias amfe="agg unlink @sequoiaconsulting/mfe-config-essentials ; agg ; agg link @sequoiaconsulting/mfe-config-essentials"

function yal() {
	yarn unlink @sequoiaconsulting/mfe-config-essentials
	yarn add $1
	yarn link @sequoiaconsulting/mfe-config-essentials
}
alias yal="yal"
function aal() {
	agg unlink @sequoiaconsulting/mfe-config-essentials
	agg add $1
	agg link @sequoiaconsulting/mfe-config-essentials
}
alias aal="aal"

alias f="fuck"

alias cr="cargo run"
alias cb="cargo build"
alias ca="cargo add"

DISABLE_AUTO_TITLE="true"

precmd() {
	# sets the tab title to current dir
	echo -ne "\e]1;${PWD##*/}\a"
}

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

dmgcreator() {
	hdiutil create -volname "$1" -srcfolder "$1.app" -ov -format UDZO "$1.dmg"
	open "$1.dmg"
}
alias dmg="dmgcreator"

alias p="python"