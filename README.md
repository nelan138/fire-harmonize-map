# Fire Harmonize Map

A Nuxt web app for exploring NASA fire detections and regional fire activity. The map opens over Indochina.

## Run locally

Use Node.js 24.15.0 or newer in the 24.x series. From the repository root, switch to `web/` to install dependencies and start Nuxt.

```bash
cd web
npm install
npm run dev
```

Open [localhost:3000](http://localhost:3000). No `.env` file is required.

## Explore fire activity

- **Interactive map (`/map`)**. Search by latitude and longitude to move the map. Click near a detection to see the available fire events within 20 km and inspect their details.
- **Burning activity calendar (`/activities`)**. Select a fire area on the map, then open the calendar to see monthly fire counts and alert levels for the regions represented in that area.

The app needs internet access for NASA GIBS map tiles and the [Parquet dataset on Hugging Face](https://huggingface.co/datasets/leveluplevelyn/fire_event_nasaspaceapps). The Nuxt server queries the dataset with DuckDB.
