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

## Generate anomaly diagnostics for Member C

```powershell
npm.cmd run anomaly:parquet
```

It writes `web/public/data/anomaly_diagnostics.csv`. Pass `--region all` to
include all regions in the Parquet, or `--region INDOCHINA` to select one.
Use `--parquet "C:\path\to\harmonized_fire_monthly.parquet"` or
`--out "C:\path\to\diagnostics.csv"` to override the input or output path.

### CSV fields and query example

Each row is keyed by `region_id`, `h3_index`, `biome_id`, `month`, and `year`.
Fields are grouped by purpose:

- Location and time: `region_id`, `h3_index`, `year`, `month`, `biome_id`,
  `selected_date`, `lat_centroid`, `lon_centroid`, `spatial_resolution`.
- Source measurements: `raw_modis_count`, `raw_viirs_count`,
  `adj_fire_count`, `adj_frp_mw`.
- SFAI: `sfai_baseline_start_year`, `sfai_baseline_end_year`,
  `sfai_baseline_year_count`, `sfai_baseline_years`,
  `sfai_historical_mean`, `sfai_historical_std`, `sfai_z_score`,
  `sfai_alert_level`, `sfai_alert_color_hex`, `sfai_status`.
- Chow test: `chow_break_year`, `chow_pre_year_count`,
  `chow_post_year_count`, `chow_f_stat`, `chow_p_value`,
  `chow_df_numerator`, `chow_df_denominator`, `chow_status`,
  `chow_no_significant_break_detected`, `chow_verdict`.
- Climate: `oni_index`, `enso_phase`, `enso_explanation`.

For example, DuckDB can read the CSV directly:

```sql
SELECT year, month, biome_id, adj_fire_count,
       sfai_z_score, sfai_alert_level, sfai_status,
       chow_p_value, chow_status, oni_index, enso_phase
FROM read_csv_auto('public/data/anomaly_diagnostics.csv', header = true)
WHERE region_id = 'INDOCHINA' AND year = 2024 AND month = 4;
```

SFAI compares each row with earlier years for the same region/location,
biome, and calendar month. The 2012 Chow result uses the full available series
for that same group, so its fields repeat across years. Climate fields are
blank because no ONI series is included. Rerun the command whenever the
calibrated Parquet changes; the CSV is a generated snapshot, not a live link.

The inspected calibrated file contains `h3_index = "N/A"`; its rows support
regional and biome diagnostics but not per-cell map results. The runner records
that in `spatial_resolution`. It fills missing years inside each region's
coverage with zero counts. Confirm that the source has complete monthly
coverage before interpreting those zeros as no fires.
