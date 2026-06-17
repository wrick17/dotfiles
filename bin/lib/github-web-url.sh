#!/usr/bin/env bash

github_web_url() {
	local remote
	remote="${1:-$(git config --get remote.origin.url)}"
	remote="${remote%.git}"

	if [[ $remote =~ ^git@([^:]+):(.+)$ ]]; then
		printf 'https://%s/%s' "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"
		return
	fi

	if [[ $remote =~ ^https?:// ]]; then
		printf '%s' "$remote"
		return
	fi

	printf '%s' "$remote"
}
