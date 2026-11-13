# Fire Harmonize Map

A web app for viewing NASA fire detections and monthly fire activity in Indochina.

## Run locally

Use Node.js 24.15.0 or newer in the 24.x series and run these commands from the repository root.

```bash
cd web
npm install
npm run dev
```

Open [localhost:3000](http://localhost:3000). No `.env` file is required.

Internet access is required for the NASA map tiles and the [Parquet files on Hugging Face](https://huggingface.co/datasets/leveluplevelyn/fire_event_nasaspaceapps) that DuckDB queries.
