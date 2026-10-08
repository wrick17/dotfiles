# Sequoia frontend workspace

Use this as an orientation map, not a frozen contract. Always verify the current checkout because branches and `@sequoia-engineering/mfe` versions differ.

## Fleet shape

The Sequoia apps workspace contains independent sibling Git repositories, not one monorepo:

| Repository name (`origin` basename) | Directory | Role and useful anchors |
| --- | --- | --- |
| `kernel-adminshell-frontend` | `adminshell` | Composition host. `config.js` names remote `host`; `src/App/App.jsx` composes experiences; `src/router/index.js` exposes `host/router`; shared hooks, i18n, fetch, contexts, and components are federated contracts. |
| `kernel-eureka-frontend` | `eureka` | Design system remote. Inspect `config.js`, `src/components/beta.ts`, component implementations/stories, `src/styles`, and `src/tailwind.css`. |
| `sequoiaai-all-frontend` | `ai` | AI feature remote, primarily under `src/modules`; inspect `config.js` for the exact consumed entries. |
| `benefitos-broker-frontend` | `broker` | Broker product routes start at `src/BrokerRoutes.jsx`; feature code is mostly under `src/modules`. |
| `cloud-all-frontend` | `cloud` | Product MFE with modern `src/features` and legacy `src/modules`; composed route roots include `src/modules/Cloud.jsx`. Read `CLAUDE.md`. |
| `kernel-idm-frontend` | `idm` | Authentication remote named `auth`; routing starts around `src/App/AuthApp.js`. |
| `kernel-all-frontend` | `kernel` | Settings remote named `settings`; inspect `src/modules/Settings/Settings.jsx` and nested route owners. |
| `pl-ui` | `pl` | PeopleLoop remote named `peopleloop`; inspect `src/modules/common/PLRoutes.tsx`, `src/modules/common/routes`, `src/pages`, and `src/init/HttpRoutesPL.ts`. |
| `compos-planning-frontend` | `planning` | Planning routes start at `src/Planning.js`; feature-first code lives below `src/modules`. Read `CLAUDE.md`. |
| `benefitos-benefits-frontend` | `px` | PX app routing is under `src/App/AllRoutes`; many product modules sit below `src/modules`. |
| `compos-totalrewards-frontend` | `tr` | Total Rewards routes start at `src/TotalRewards.js`; nested modules own sub-routes. |
| `serviceos-s1service-frontend` | `s1` in fresh init; existing checkouts may use `uwp` | ServiceOS routes start at `src/UWP.js`; module and widget code coexist. Read `CLAUDE.md`. |
| `benefitos-wellbeing-frontend` | `wellbeing` | Wellbeing route root is `src/WellbeingApp.js`; versioned admin modules coexist. |

Each repo owns its `package.json`, `bun.lock`, `config.js`, build/test configuration, Git state, and deployment contract. Run Git, install, format, lint, test, and build commands inside the actual child repo.

Fresh `agg init` includes the core fleet above except optional PeopleLoop. Analytics, `Sequoia-Engineering/analytics-all-frontend`, is also optional and uses `analytics` with memorable names. PeopleLoop comes from `Sequoia-US/pl-ui` on `main`; core repositories and Analytics initialize on `dev`. Existing folder names and approved branches remain authoritative. Full-name init uses GitHub repository names instead of these short folders.

## Composition boundaries

- Root `config.js` is the live Module Federation contract. Read it before assuming the entry point or adding an expose.
- `adminshell` is a generic host. Product-specific routes and behavior stay in product MFEs.
- A visible route can delegate through more than one remote. Trace imports and lazy remote loading until reaching the component that owns the feature.
- `host/router` is the router boundary. It supplies compatibility and modern exports over the shell's active router.
- `host/i18n`, `host/hooks`, `host/fetch`, `host/contexts`, and related exposes are platform contracts. Inspect `adminshell/config.js` and types before use.
- The presence of a navigation-contribution contract is branch-dependent. Use it only when it exists in the current target checkout.
- Cross-MFE imports must go through federation exposes or approved packages, never sibling filesystem paths.

## Mandatory CSS contract

Consumer `src/tailwind.css` files use:

```css
@import "eureka/tokens";
@import "@sequoia-engineering/mfe/tailwind/base.css";
@source "../src/**/*.{js,ts,jsx,tsx,css}";
```

Eureka alone owns its local token and preflight composition. The host loads preflight once. Do not add a consumer Tailwind config, PostCSS setup, direct preflight import, or manual MFE class prefix.

## Ownership discovery

Run focused searches from the apps workspace root, excluding generated and dependency trees:

```bash
rg -n "requested-route|product-term" */src --glob '*.{js,jsx,ts,tsx}'
rg -n "from ['\"]host/router|<Route|lazyRemote" */src --glob '*.{js,jsx,ts,tsx}'
rg -n "requested-component" eureka/src/components */src --glob '*.{js,jsx,ts,tsx}'
```

Then inspect the candidate repo:

```bash
git status --short
sed -n '1,220p' package.json
sed -n '1,220p' config.js
sed -n '1,220p' tsconfig.json
```

Do not modify unrelated dirty files.
