-- NULL = khong loc. Du lieu theo thang, bbox loc toa do dai dien.
SELECT
   make_date(year, month, 1) AS month_start,
   last_day(month_start) AS month_end,
   region_id,
   year,
   month,
   biome_id,
   lat_centroid,
   lon_centroid,
   raw_modis_count,
   raw_viirs_count,
   raw_frp_mw,
   adj_fire_count,
   adj_frp_mw,
   sfai_zscore,
   sfai_alert_lvl
FROM read_parquet($monthly_path)
WHERE ($date_from IS NULL OR last_day(month_start) >= CAST($date_from AS DATE))
  AND ($date_to IS NULL OR month_start <= CAST($date_to AS DATE))
  AND ($selected_year IS NULL OR year = $selected_year)
  AND ($selected_month IS NULL OR month = $selected_month)
  AND ($selected_region IS NULL OR region_id = $selected_region)
  AND ($selected_biome IS NULL OR biome_id = $selected_biome)
  AND ($min_lat IS NULL OR lat_centroid >= $min_lat)
  AND ($max_lat IS NULL OR lat_centroid <= $max_lat)
  AND ($min_lon IS NULL OR lon_centroid >= $min_lon)
  AND ($max_lon IS NULL OR lon_centroid <= $max_lon)
ORDER BY month_start DESC, region_id, biome_id;
