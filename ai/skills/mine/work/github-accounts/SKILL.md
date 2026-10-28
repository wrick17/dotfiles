---
name: github-accounts
description: Selects the GitHub account and tool for a repository. Use before any Git or GitHub operation that touches a remote: clone, fetch, pull, push, PRs, issues, or API calls.
---

# GitHub accounts

- Before any Git or GitHub operation, inspect the repository's default remote and identify its owner. Use `origin` when no other default is configured. For a clone, inspect the target URL. If the remote or owner is ambiguous, resolve it before proceeding.
- If the owner is `Sequoia-Engineering`, `Sequoia-US`, or `pratyush-poddar_seq`, use the `pratyush-poddar_seq` GitHub account for all operations and explicitly use the `gh` CLI for GitHub access. Do not use the GitHub connector for these repositories.
- For all other projects, use the `wrick17` GitHub account. Either the `gh` CLI or the GitHub connector is allowed.
- Verify the selected account before proceeding. With `gh`, select the required account using `gh auth switch --hostname github.com --user <account>` when needed, then confirm it with `gh api user --jq .login`. With the GitHub connector, verify its authenticated account.
- Use native `git` for local Git operations and Git transport where needed. Ensure SSH or HTTPS credentials use the required account for remote operations; switching `gh` accounts alone does not verify Git transport identity.
