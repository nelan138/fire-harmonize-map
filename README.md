# Fire Harmonize Map

A Nuxt web app for exploring NASA fire detections and comparing regional fire activity across years. The map opens over Indochina.

## Run locally

Use Node.js 24.15.0 or newer in the 24.x series. From the repository root, switch to `web/` to install dependencies and start Nuxt.

```bash
cd web
npm ci
npm run dev
```

Open [localhost:3000](http://localhost:3000). No `.env` file is required.

## Explore fire activity

- **Interactive map (`/map`)**. Enter latitude and longitude to move the map. Click near a detection to inspect loaded fire events within 20 km. The map API currently returns up to 1,000 Indochina detections.
- **Burning activity calendar (`/activities`)**. Select a fire area on the map, then open the calendar. Each cell shows the regional fire count on hover and uses the highest recorded alert for its color. Select a month to see regional counts, historical change, and SFAI scores and alerts for the source records.
- **Monthly analysis**. Compare the selected month with the same calendar month across available years in the 2000–2024 baseline. View each biome’s share of harmonized detections and fire radiative power, and compare raw MODIS, raw VIIRS, and harmonized counts.
- **Print or save a brief**. Use **Print / Export PDF** in the sensor comparison card to open a one-page A4 brief. Choose **Save as PDF** in the browser’s print dialog.

The calendar’s Oceanic Niño Index (ONI) card currently displays a placeholder.

## Data sources

The app needs internet access for NASA GIBS map tiles and the [Parquet dataset on Hugging Face](https://huggingface.co/datasets/leveluplevelyn/fire_event_nasaspaceapps). The Nuxt server queries the dataset with DuckDB.

| Endpoint | Parquet file |
| --- | --- |
| `/api/fire-events` | `GLOBAL_5_REGIONS_clean_fire_events.parquet` |
| `/api/fire-monthly` | `harmonized_fire_monthly.parquet` |

Use `NUXT_FIRE_DATA_BASE_URL` to override the dataset base URL. The monthly endpoint accepts an optional region filter such as `/api/fire-monthly?regions=INDOCHINA`.

## Test and build

Run these commands from `web/`.

```bash
npm test
npm run build
node .output/server/index.mjs
```
