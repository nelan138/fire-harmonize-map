SELECT
   region_id,
   CAST(year AS INTEGER) AS year,
   CAST(month AS INTEGER) AS month,
   CAST(h3_index AS VARCHAR) AS h3_index,
   TRY_CAST(biome_id AS INTEGER) AS biome_id,
   TRY_CAST(lat_centroid AS DOUBLE) AS lat_centroid,
   TRY_CAST(lon_centroid AS DOUBLE) AS lon_centroid,
   TRY_CAST(raw_modis_count AS INTEGER) AS raw_modis_count,
   TRY_CAST(raw_viirs_count AS INTEGER) AS raw_viirs_count,
   TRY_CAST(raw_frp_mw AS DOUBLE) AS raw_frp_mw,
   TRY_CAST(adj_fire_count AS DOUBLE) AS adj_fire_count,
   TRY_CAST(adj_frp_mw AS DOUBLE) AS adj_frp_mw,
   TRY_CAST(sfai_zscore AS DOUBLE) AS sfai_zscore,
   TRY_CAST(sfai_alert_lvl AS INTEGER) AS sfai_alert_lvl
FROM read_parquet($path)
WHERE $regions::VARCHAR[] IS NULL OR list_contains($regions::VARCHAR[], region_id)
ORDER BY region_id, year, month, biome_id, h3_index
