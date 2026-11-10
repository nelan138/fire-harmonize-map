# Fire Harmonize Map

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

## Client-side DuckDB

DuckDB-WASM runs entirely in the browser and initializes lazily on the first
query. It registers these views over the Parquet files in `web/public/data`:

- `harmonized_fire_monthly`
- `calibration_lookup`

Use the `useDuckDB` composable from a Vue component. Query results are returned
as plain objects, and values should be passed separately from the SQL string:

```ts
const { query, status, error } = useDuckDB();

const rows = await query<{ year: number; month: number; fire_count: number }>(
   `SELECT year, month, fire_count
      FROM harmonized_fire_monthly
     WHERE year = ?
     ORDER BY month`,
   [2023],
);
```
