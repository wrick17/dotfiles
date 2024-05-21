alias cd="z"
alias ll="ls -all --color"
alias c="clear"
alias x="exit"
alias gst="git status"
alias ga="git add"
alias gc="git commit -m"
function pull(){
	branch="$(git rev-parse --abbrev-ref HEAD)"
	if [ $# -eq 0 ]
	then
		git pull origin $branch --rebase
	else
		git pull origin $1 --rebase
	fi
}
alias ggpu=pull
function pullMerge(){
	branch="$(git rev-parse --abbrev-ref HEAD)"
	if [ $# -eq 0 ]
	then
		git pull origin $branch
	else
		git pull origin $1
	fi
}
alias ggpum=pullMerge
function gpi(){
	branch=$(git symbolic-ref --short HEAD)
	remote=$(git config --get remote.origin.url)
	removeDotGit="${remote/.git/}"
	removeColon="${removeDotGit/://}"
	url=${removeColon/git\@/https:\/\/}
	open "${url}/issues/new?title=deploy%20${branch}"
}
function gpr(){
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
	while (( $# )); do
    case $1 in
      -t=*|--title=*)  				title="${1#*=}" ;;
      -d=*|--description=*)  	description="${1#*=}" ;;
      *)                  		if [ $count -eq 1 ]; then branch=$secondArg; target=$1; else target=$1; fi ;;
    esac
		count=$((count+1))
    shift
  done

	if [ $count -eq 0 ]; then
		base="${url}/compare/${branch}";
	else
		base="${url}/compare/${target}...${branch}";
	fi
	temp="${base}?expand=1";

	if [ $title ] && [ $description ]; then
		temp="${temp}&title=${title}&body=${description}";
	elif [ $title ]; then
		temp="${temp}&title=${title}";
	elif [ $description ]; then
		temp="${temp}&body=${description}";
	fi

	open "${temp}";

	unset target;
	unset count;
	unset title;
	unset description;
	unset secondArg;
	unset final;
}
alias gpi=gpi
alias gpr=gpr
alias gp="git push origin HEAD"
alias n="npm"
alias ni="npm install"
alias ns="npm start"
alias nd="npm run dev"
alias nb="npm run build"
alias nr="npm run"
alias g="git"
alias gbc="git symbolic-ref --short HEAD"
alias gs="git stash"
alias gsp="git stash pop"
alias gb="git branch"
alias gbc="git rev-parse --abbrev-ref HEAD && git rev-parse --abbrev-ref HEAD | pbcopy"
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
alias ss="sshpass -p 'durgapur' ssh dietpi@192.168.1.199"
alias a="agg"
alias as="agg start"
alias python="/usr/bin/python3"
alias pip="pip3"
alias foo="echo foo"
alias nvm="fnm"

alias ymfe="yarn unlink @sequoiaconsulting/mfe-config-essentials ; yarn ; yarn link @sequoiaconsulting/mfe-config-essentials"
alias amfe="agg unlink @sequoiaconsulting/mfe-config-essentials ; agg ; agg link @sequoiaconsulting/mfe-config-essentials"

DISABLE_AUTO_TITLE="true"

precmd() {
  # sets the tab title to current dir
  echo -ne "\e]1;${PWD##*/}\a"
}