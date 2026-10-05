# Implementation workflow

## Resolve ownership end to end

Trace the composed path before editing:

`shell route -> federated expose -> owning route root -> feature/page -> data contracts`

- Inspect the live checkout, branch, status, `package.json`, `config.js`, TypeScript aliases, route roots, and adjacent feature.
- Search for the requested route, product vocabulary, related components, API hooks, and existing tests across sibling repos.
- Put product behavior in the owning MFE. Keep shell code generic.
- Do not create a new MFE, shared package, federation expose, or navigation contract unless the confirmed requirements truly cross that boundary and the user approved the expanded scope.
- Never edit generated `src/tsconfig.json`.

If discovery contradicts the confirmed implementation contract, stop, show the evidence, and ask the user to amend the contract before continuing.

## Reuse before creating

Use this order:

1. Existing implementation in the owning feature.
2. Eureka from `eureka/beta/components`.
3. Approved shell contracts such as `host/router`, `host/i18n`, `host/hooks`, or `host/components`.
4. Owning repo's shared components and utilities.
5. Native platform behavior styled with Tailwind.
6. An already-installed dependency.
7. Minimum new code.

Read the actual component export, implementation, types, and Storybook story before using it. Do not guess its API.

## Enforce the UI contract

- Use Eureka for existing primitives and patterns. Never recreate its buttons, inputs, dialogs, tables, tabs, cards, badges, tooltips, filters, loaders, or empty states.
- Use Tailwind v4 utilities for new styling. Preserve the repo's `src/tailwind.css` imports.
- Use semantic token utilities such as `bg-background`, `text-foreground`, and `border-border`; map supplied design values to Eureka semantics before considering arbitrary values.
- Write complete static class strings. Use the repo's `cn` or `cva` pattern for variants. Never hand-prefix classes or target generated MFE prefixes.
- Do not add styled-components, inline color values, a Tailwind config, global CSS, or a styling dependency for new page UI.
- Keep accessibility intact: semantic elements, labels, names for icon buttons, keyboard behavior, visible focus, useful loading or error announcements, and correct dialog focus handling.
- Use the owning app's `host/i18n` pattern for visible copy and accessible names. Do not introduce direct `react-intl`.
- Verify supported themes relevant to the requirements, including dark and high-contrast behavior when present.

If Eureka lacks a primitive, use the smallest accessible native composition. Change Eureka only when the component is genuinely cross-product, no existing composition works, and shared-repo scope is approved.

## Implement in the owning pattern

- Mirror the nearest current feature; do not impose a universal scaffold.
- Create only folders that contain real code. Do not add empty `store`, `types`, `utils`, barrel, or test folders.
- Prefer TypeScript for new files when the target area permits it; match adjacent naming, exports, aliases, import order, and formatting.
- Keep route pages as composition boundaries. Put reusable view pieces in local `components`, server access in the existing API layer, and server state in the local TanStack Query pattern.
- Reuse the module's form, validation, state, permission, analytics, feature-flag, toast, and error conventions. Do not migrate a legacy area as collateral work.
- Import navigation from `host/router`, never directly from a router package.
- Wire the route in the owning route root. Add a `config.js` expose only when another MFE must consume that entry.
- Do not invent backend endpoints, response shapes, permissions, translations, analytics, or feature flags. Stop and ask for a missing contract that cannot be discovered.
- Add the smallest meaningful regression check for new behavior. Prefer role- and behavior-based assertions.
