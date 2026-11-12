# Fire Harmonize Map

## Routes

```text
|-- map                       Interactive fire-calibration map
|-- activities                Monthly burning-activity heatmap
|-- diagnostics               SFAI anomaly diagnostics
|-- validation                Scientific validation
```

## Setup

Make sure to navigate to directory `/web`

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## Fire data API

DuckDB runs on the Node.js server. SQL files live in `web/server/sql` and are
bundled as server assets. Components fetch JSON from:

- `/api/calibrated-fire-events`: up to 1,000 events for INDOCHINA.
- `/api/fire-monthly`: monthly heatmap values for INDOCHINA.

The server reads `calibrated_fire_events.parquet` and `fire_monthly.parquet`
from `public/data`, relative to the server's working directory. Set
`NUXT_FIRE_DATA_DIR` to an absolute directory to use a different location.

This requires a Node.js deployment. After building, run from `web/.output`
with `node server/index.mjs`, or set `NUXT_FIRE_DATA_DIR` to the deployed
Parquet directory. Static generation cannot run these API endpoints.

Run `npm test` from `web` to check both SQL queries against the local files.
