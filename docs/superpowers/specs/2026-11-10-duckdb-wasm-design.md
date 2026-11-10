# Client-side DuckDB-WASM design

## Intent

Configure the Nuxt frontend to query the existing Parquet datasets directly in the browser. This keeps the current frontend-only architecture and avoids adding a database server or API.

## Goals

- Initialize one shared DuckDB-WASM instance only in the browser.
- Package the DuckDB worker and WASM binaries with the application rather than depending on a runtime CDN.
- Provide a typed Nuxt composable that waits for initialization, opens short-lived connections, runs parameterized queries, and closes connections reliably.
- Register `/data/harmonized_fire_monthly.parquet` and `/data/calibration_lookup.parquet` as stable SQL views.
- Surface initialization and query failures clearly, and cleanly terminate the worker when the Nuxt app is disposed.
- Document how frontend code should run queries.

## Non-goals

- No Python or server-side DuckDB setup.
- No persistence, write API, synchronization, or multi-user database.
- No redesign of the map or replacement of the existing iframe in this change.
- No eager download of the Parquet datasets during initial page rendering; DuckDB will read them when queried.

## Constraints

- DuckDB must never initialize during SSR.
- The setup must work with Nuxt/Vite production builds and avoid duplicate database workers during normal client navigation and development hot reloads.
- Existing uncommitted dependency changes in `web/package.json` and `web/package-lock.json` must be preserved.

## Approaches considered

1. **Local client plugin plus composable (selected).** A Nuxt `.client` plugin owns a singleton DuckDB-WASM instance, while a composable exposes a small typed query interface. This gives centralized lifecycle handling, local assets, and a reusable API.
2. **CDN-backed client plugin.** This reduces bundler configuration but makes application startup depend on a third-party CDN and complicates strict content-security policies.
3. **Page-local initialization.** This is initially smaller but couples DuckDB to one component and risks duplicate workers, repeated setup, and inconsistent cleanup as the frontend grows.

## Proposed shape

- Add a browser-only DuckDB service responsible for selecting the best supported WASM bundle, starting its worker, creating the database, and defining the two Parquet views.
- Inject that service through a Nuxt client plugin.
- Add a `useDuckDB` composable with an async query method and observable readiness/error state.
- Add focused tests around singleton initialization, query connection cleanup, and error propagation where practical, then verify with Nuxt type checking and a production build.
- Add a short README section with a parameterized query example and the registered view names.

