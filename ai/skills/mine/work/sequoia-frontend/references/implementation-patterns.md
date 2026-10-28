# Sequoia implementation patterns

## Choose structure from evidence

The fleet is intentionally mixed. Match the owning feature:

- Modern Cloud work commonly uses `src/features/<feature-slug>/` with only the required `pages`, `components`, `hooks`, `api`, `queries`, `types`, `constants`, and `utils`.
- Planning is feature-first below `src/modules/<FeatureName>/`.
- PL separates route groups, `src/pages`, domain `src/modules`, shared `src/components`, queries, and platform adapters.
- Legacy product areas use deep `src/modules/<Domain>/...` trees. Extend them locally; do not reorganize them during the requested implementation.

Use the nearest maintained feature with similar route/data complexity as the template. Follow its filename casing, aliases, named/default export style, tests, and barrel policy. Never create a generic architecture layer for one page.

## Map design concepts to code

| Design concept | Default code boundary |
| --- | --- |
| Navigable screen | Route plus a page composition component |
| Product capability | Owning feature/module |
| Repeated product-specific block | Local component |
| Design-system instance | Existing Eureka component |
| Transient interaction state | Local React state or derived state |
| Server data | Existing API wrapper plus TanStack Query hook/key pattern |
| Cross-page client state | Existing feature store only when local/URL/query state is insufficient |
| URL-driven filter/tab | Existing `host/router` search/path pattern |
| Reusable cross-product primitive | Eureka change only with approved shared scope |

Extract only when reuse, testability, or readability already justifies it. A one-use wrapper around Eureka is usually unnecessary.

## UI and styling

- Canonical new UI import: `eureka/beta/components`.
- Check `eureka/src/components/beta.ts`, the component source, types, and Storybook story before coding.
- Prefer Eureka, then approved `host/components`, then repo-local shared UI.
- Use semantic Eureka tokens for color, surface, border, typography, focus, positive/negative status, and input states.
- Use unprefixed Tailwind v4 utilities in source. Prefer static strings, a ternary, or the repo's `cn`/`cva` helper.
- Do not build class names with string fragments, imperatively mutate classes, target generated `.host-*`/`.eureka-*` classes, or use Tailwind utilities as styled-component selectors.
- Keep one-off CSS only for behavior Tailwind cannot express cleanly, such as a required keyframe or third-party integration, and keep it scoped to the feature.
- Use supplied visual measurements precisely when meaningful, but prefer an existing spacing/type/token utility over an arbitrary value.

## Routes and federation

- Import `Route`, `Switch`, `Redirect`, `Link`, and hooks from `host/router`.
- Add the route at the lowest owning router that covers the URL family.
- Preserve route order, exactness, permissions, layouts, error boundaries, feature flags, analytics, and tenant/experience selection around the neighboring routes.
- Direct refresh must resolve through the composed host.
- A route does not require a new federation expose when it is already reachable through the owning remote's app/routes entry.
- Add or change `config.js` only for a real cross-MFE public entry. Update matching remote type declarations only through the repo's established source, never generated `src/tsconfig.json`.

## Data, forms, and state

- Read the target repo's API client and adjacent hooks before writing a request. Reuse its auth, org/tenant, serialization, error, retry, and response normalization behavior.
- Use the local TanStack Query key factory and invalidation pattern where present.
- Keep transport types distinct from view models when the feature already does so.
- Do not create placeholder data or guess an endpoint from a requirements source.
- Reuse the feature's form stack. Formik/Yup, React Hook Form/Zod, and custom Eureka forms all exist; do not add another stack.
- Prefer local/derived state, then URL state, then query cache. Use Zustand or Redux only when the owning feature already uses it and the state genuinely spans components.
- Extend styled-components, Redux/Saga, or other legacy islands only when modifying that island; do not introduce them for a new page.

## Platform behavior

- Use the owning repo's permission, feature-flag, org/tenant, analytics, toast, modal, and error-boundary hooks.
- Use `host/i18n`; copy the current namespace/key convention and update every required locale file.
- Partial remote entries may need `loadNamespace`; route remotes commonly use the shell's lazy-remote path. Match the local integration.
- Preserve accessibility beyond visual fidelity: headings, landmarks, labels, descriptions, table semantics, focus order, keyboard activation, live status, and reduced-motion expectations.

## Tests and checks

Choose the smallest check that proves the new behavior:

- Pure branching/normalization: focused Rstest unit test.
- Interaction, focus, or real DOM behavior: existing `*.browser.test.*` convention.
- Route integration: route-level test and composed browser verification.
- Shared Eureka change: component test plus Storybook story when that repo's convention requires it.

Run commands declared by the target `package.json`, commonly:

```bash
bun run format
bun run lint
bun run test
bun run build
git diff --check
```

UWP and PL have different test/formatter arrangements; inspect their scripts rather than copying commands blindly. Use `lint:warning` when checking warning-only Tailwind migration diagnostics.
