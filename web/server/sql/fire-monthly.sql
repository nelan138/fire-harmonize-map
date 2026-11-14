SELECT
   region_id,
   CAST(year AS INTEGER) AS year,
   CAST(month AS INTEGER) AS month,
   h3_index,
   CAST(biome_id AS INTEGER) AS biome_id,
   CAST(lat_centroid AS DOUBLE) AS lat_centroid,
   CAST(lon_centroid AS DOUBLE) AS lon_centroid,
   CAST(raw_modis_count AS INTEGER) AS raw_modis_count,
   CAST(raw_viirs_count AS INTEGER) AS raw_viirs_count,
   CAST(raw_frp_mw AS DOUBLE) AS raw_frp_mw,
   CAST(adj_fire_count AS DOUBLE) AS adj_fire_count,
   CAST(adj_frp_mw AS DOUBLE) AS adj_frp_mw,
   CAST(sfai_zscore AS DOUBLE) AS sfai_zscore,
   CAST(sfai_alert_lvl AS INTEGER) AS sfai_alert_lvl
FROM fire_monthly
ORDER BY region_id, year, month
LIMIT 1000
