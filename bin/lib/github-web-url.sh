#!/usr/bin/env bash

github_web_url() {
	local remote remove_dot_git remove_colon
	remote="${1:-$(git config --get remote.origin.url)}"
	remove_dot_git="${remote/.git/}"
	remove_colon="${remove_dot_git/://}"
	printf '%s' "${remove_colon/git\@/https:\/\/}"
}
