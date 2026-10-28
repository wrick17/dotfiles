# Work instructions

## Work skills

- Use `~/skills/mine/common`, `~/skills/mine/work`, `~/skills/third-party/common`, and `~/skills/third-party/work`.
- Load the matching skill before the work it covers:
  - `bothq-memory`: at the start of every non-trivial work task and on resume. BothQ is the mandatory shared memory and journal for work.
  - `github-accounts`: before any Git or GitHub operation that touches a remote.
  - `sequoia-pr`: before creating, updating, or monitoring any PR. Its Sequoia PR protocol is a hard requirement.
  - `jira-connector`: whenever the user gives a Jira ticket ID or URL.
  - `sequoia-feature-workspace`: when starting, resuming, or cleaning up a new Sequoia app feature.
  - `sequoia-frontend`: for Sequoia frontend work, according to its task triggers.

## Box

- Launch Box in the user's cmux terminal by running exactly `box`, without RTK, subcommands, flags, or arguments. Never launch it through the agent's internal terminal execution tools. This is an exception to the global RTK rule.
- Use the Box MCP server for all other configuration and control.
