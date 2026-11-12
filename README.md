# Fire Harmonize Map

A Nuxt application for viewing NASA fire detections on a map and exploring monthly burning activity. Python calibration tools live in `backend/calibration`; the web application reads prepared Parquet datasets hosted on Hugging Face.

## Stack

- Nuxt 4, Vue 3, and TypeScript.
- Nuxt UI and Tailwind CSS for the interface.
- Leaflet with NASA GIBS background tiles.
- DuckDB Node API for server-side SQL queries over remote Parquet files.
- Python tools for data preparation and MODIS/VIIRS calibration.

## Run locally

Install Node.js and npm, then run these commands from the repository root:

```bash
cd web
npm install
npm run dev
```

Open http://localhost:3000. The root route redirects to `/map`.
Internet access is required for the remote datasets and NASA map tiles. DuckDB may also download its HTTP extension on first use.

## Pages

| Route | Purpose | Status |
| --- | --- | --- |
| `/map` | NASA basemap with up to 1,000 INDOCHINA fire detections | Implemented |
| `/activities` | Monthly burning-activity heatmap for INDOCHINA | Implemented |
| `/debug` | Paginated table of the fire-event API response | Implemented |
| `/diagnostics` | SFAI anomaly diagnostics | Placeholder |
| `/validation` | Scientific validation | Placeholder |

## Data flow

```text
Vue component
  -> Nuxt server API
  -> DuckDB on the Node.js server
  -> Hugging Face Parquet files
  -> JSON response to the component
```

The current map and calendar use server APIs. SQL execution for these endpoints happens on the server, rather than in the browser. Browser Network tools show `/api/...` requests; the server makes the remote Parquet requests.

### Dataset

Public dataset: [leveluplevelyn/fire_event_nasaspaceapps](https://huggingface.co/datasets/leveluplevelyn/fire_event_nasaspaceapps).

Default base URL:

```text
https://huggingface.co/datasets/leveluplevelyn/fire_event_nasaspaceapps/resolve/main/
```

| Remote file | DuckDB view | Purpose |
| --- | --- | --- |
| `fire_events.parquet` | `fire_events` | Individual fire detections |
| `fire_monthly.parquet` | `fire_monthly` | Monthly counts and alert levels |

These APIs do not require local Parquet files in `web/public/data`. The endpoint name `calibrated-fire-events` is retained, but its source file is `fire_events.parquet`; the endpoint does not perform calibration itself.

### Configuration

`web/nuxt.config.ts` defines `runtimeConfig.fireDataBaseUrl`. Override it with `NUXT_FIRE_DATA_BASE_URL` to use another public dataset location containing both files with compatible columns.

PowerShell example, from `web`:

```powershell
$env:NUXT_FIRE_DATA_BASE_URL = "https://huggingface.co/datasets/leveluplevelyn/fire_event_nasaspaceapps/resolve/main/"
npm run dev
```

Restart the server after changing configuration. Use a commit revision instead of `main` in the URL when you need a fixed dataset version.

### API endpoints

| Endpoint | SQL file in `web/server/sql` | Response |
| --- | --- | --- |
| `/api/calibrated-fire-events` | `calibrated-fire-events.sql` | Up to 1,000 INDOCHINA events with non-null coordinates |
| `/api/fire-monthly` | `fire-monthly.sql` | INDOCHINA monthly records ordered by year and month |

SQL files are bundled as Nitro server assets. `web/server/utils/duckdb.ts` creates connection-local views over the remote files, executes the requested SQL, and returns JSON-safe records.

## Important files

```text
backend/calibration/           Python data preparation and calibration tools
web/nuxt.config.ts            Runtime data URL and server-asset configuration
web/server/utils/duckdb.ts     Remote Parquet views and query execution
web/server/sql/               SQL queries used by the APIs
web/server/api/               JSON API handlers
web/app/components/           Map, fire markers, and heatmap components
web/app/pages/                Application pages
web/tests/fire-data.test.ts   Integration tests for both SQL queries
```

## Verification

From `web`:

```bash
npm test
```

The integration tests query the public Hugging Face dataset directly. They check event coordinates and region, the event limit, monthly ordering, numeric values, and JSON serialization. Internet access is required; each test allows up to 60 seconds. The test dataset URL is defined in `web/tests/fire-data.test.ts`, independently of Nuxt runtime configuration.

For a manual check, open `/api/calibrated-fire-events` and `/api/fire-monthly` in the browser and confirm that both return JSON arrays. Then check `/map`, `/activities`, and `/debug`.

## Production

From `web`:

```bash
npm run build
node .output/server/index.mjs
```

Deploy to a Node.js environment compatible with the native DuckDB dependency, with outbound access to the remote data. Set `NUXT_FIRE_DATA_BASE_URL` in the deployment environment if needed. A static-only deployment cannot execute these server API endpoints.

## Current limitations

- Queries currently select INDOCHINA; the map query has a 1,000-row limit without chronological ordering.
- Monthly records can contain multiple biome rows for the same month. The current heatmap keys cells by month/year, so regional aggregation needs correction before treating each cell as a regional total.
- The Python SFAI calculation and calibration validation still need review against the project plan. Existing alert colors are not evidence of completed scientific validation.
