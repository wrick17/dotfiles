---
name: sequoia-pr
description: Hard requirements for every PR in a Sequoia repository (owner Sequoia-Engineering, Sequoia-US, or pratyush-poddar_seq), plus PR checks and monitoring for all PRs raised for the user. Use before creating, updating, or monitoring any PR.
---

# Sequoia PRs

## PR protocol (hard requirement)

- Apply this protocol to every PR created or updated for a Sequoia project, including release, cherry-pick, merge, dependency, and draft PRs.
- Before creating a PR or setting its ticket metadata, use the Jira ticket ID explicitly provided by the user for this work. If none was provided, ask the user and wait for their answer before creating the PR. Never invent an ID, use a placeholder, or reuse an unrelated ticket.
- Match the repository's recent PR naming protocol: `<JIRA-ID> <type>: <description>`, for example `KP-1773 chore: support PL CDN switch in Adminshell for release-2609`.
- Use the repository's standard PR description template. Preserve `Description`, `Link to Jira Ticket`, `Remarks`, the separator, and `Code Checklist` where present. Write the ticket field as `Jira Ticket: <JIRA-ID>` with a space after the colon, replacing legacy `Jira Id` labels. Populate `https://sequoiacg.atlassian.net/browse/<JIRA-ID>`. Put the change explanation and actual validation in `Remarks`; keep checklist claims accurate and avoid custom replacement sections.
- Read back the PR title and body with `gh` and verify the ticket, URL, naming, and template before declaring PR work complete.

## PR checks and monitoring

- Monitor every PR raised for the user until all required checks pass and all the PRs are merged. Continue monitoring after reruns, new commits, and user intervention.
- Inspect failed check logs. For worker or infrastructure failures, rerun the failed checks up to three times per check before reporting a persistent failure to the user.
- Semgrep is optional. Do not report Semgrep failures or treat them as blockers to completion.
- Sonar is mandatory. If Sonar fails, inspect the run logs and extract the Sonar dashboard status link, generally starting with `https://sonar-qa.sequoia-development.com/dashboard`. Give the user the link and wait for them to handle the issue in the dashboard and confirm it is resolved. Do not attempt to fix Sonar findings yourself. If the logs contain no dashboard link, report that along with the run link.
- In T3 Code, use `watch_pull_request` when available and resume monitoring when notified. Follow the retry and Sonar rules on each update until every PR meets the completion condition above.
