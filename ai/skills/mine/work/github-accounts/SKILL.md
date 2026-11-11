---
name: github-accounts
description: Selects the GitHub account and tool for a repository. Use before any Git or GitHub operation that touches a remote: clone, fetch, pull, push, PRs, issues, or API calls.
---

# GitHub accounts

Account selection is automatic. Run `gh` and `git` from inside the target repository and leave the environment as it is.

- The `gh` shim on `PATH` gives each call the token of the account that owns its target repository: `wrick17` for owner `wrick17`, `pratyush-poddar_seq` for everything else (`Sequoia-Engineering`, `Sequoia-US`, `pratyush-poddar_seq`). It reads the target from `-R`, `--owner`, the repo or URL argument, the `gh api` endpoint, `GH_REPO`, or the remote `gh` itself would use.
- Git rewrites `wrick17` remotes to the `personal` SSH alias and work HTTPS remotes to the work SSH key, so fetches and pushes use the right key and `wrick17` repos commit with the personal email.
- Keep the active `gh` account, `GITHUB_TOKEN`, and `GH_TOKEN` exactly as they are. Never run `gh auth switch`, `gh auth login`, or `gh auth logout`, and never set, unset, or override either token variable: npm needs the global `GITHUB_TOKEN`, and the shim picks the account per call.
- Make GitHub API calls with `gh api`, not curl, Octokit, or tools that read `GITHUB_TOKEN` directly. Bare `gh auth token` is not repo-aware.
- Outside a repository, name the target with `-R OWNER/REPO`, a full repo URL, or `GH_REPO=OWNER/REPO`.
- Verify with `gh api user --jq .login` from the repository, or `GH_REPO=OWNER/REPO gh api user --jq .login` for an explicit target. A wrong login is a blocker to report, not something to work around.
- For repositories owned by `Sequoia-Engineering`, `Sequoia-US`, or `pratyush-poddar_seq`, use the `gh` CLI for all GitHub access, not the GitHub connector. For other owners, either is allowed; verify the connector's authenticated account before using it on a personal repo.
- Known limit: a work repo that also has a `wrick17` remote commits with the personal email; set `user.email` in that repo if it matters.
