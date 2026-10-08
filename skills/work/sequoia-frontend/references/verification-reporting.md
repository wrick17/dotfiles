# Verification and reporting

## Validate proportionally

From the owning repo:

1. Run its formatter and lint command.
2. Run the smallest relevant Rstest or browser test, then the repo test command when warranted.
3. Run the repo build for route, federation, CSS, or shared-contract changes.
4. Run `git diff --check` and inspect the final diff for unrelated changes.

For composed UI work:

- Use the current harness's preferred browser integration. Use the user's browser when explicitly requested and preserve their tabs.
- Do not navigate to localhost until the dev server is fully up and every MFE has finished compiling.
- Verify the real composed route, direct refresh, navigation, visible states, responsive layout, keyboard path, console, and relevant network requests.
- When a visual source exists, compare the rendered page with it at the intended viewport. Check computed styles when token or layout fidelity is in question.
- Do not substitute a standalone mock page for composed verification.

Report completion only after the requested behavior works. State any backend, permission, data, or environment blocker separately from frontend fidelity.

## Return the edited tasks to build mode

After dev-mode browser verification, finish [the Box lifecycle](workspace-tooling.md#edit-with-hmr-then-return-to-build). Switch the MFEs and any Storybook adopted for this work back to build, wait for successful static build/server readiness, and check the composed route against the resulting output. Preserve unrelated session state and leave Box running unless stopping it was requested. Report any failed build or incomplete mode cleanup instead of declaring the workspace ready.

## Generate a report when requested or required

Follow governing user and repo instructions for the report's format, location, theme, and upload destination. When no governing instruction exists, confirm those details before creating a report and do not upload it externally without explicit authorization.

When a report is required:

- Use normal Markdown for `.md`.
- Use a self-contained, responsive document for `.html`, following the user's confirmed theme preference.

Include:

- the confirmed implementation contract and source links;
- owning repository, branch, page, module, component names, and route;
- files created, changed, or removed and what each change does;
- Eureka, Tailwind, host-contract, and existing-code reuse decisions;
- API, data, permission, feature-flag, i18n, and analytics wiring;
- formatter, lint, tests, build, and browser-verification results;
- Box workspace, affected task IDs, final modes, static build readiness, and MCP setup/reload status when relevant;
- source coverage and, when a visual reference exists, fidelity, responsive, theme, accessibility, console, and network evidence;
- deviations from the contract, known limitations, skipped work, and follow-ups.

Keep the report readable, structured, and accessible. Do not create a report for routine work when neither the user nor the repository requires one.
