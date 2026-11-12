-- NULL = khong loc. Area va density doc truc tiep tu Parquet H3 bac 6.
SELECT
   make_date(year, month, 1) AS month_start,
   year,
   month,
   region_id,
   CAST(biome_id AS INTEGER) AS biome_id,
   h3_index,
   6 AS h3_resolution,
   lat_centroid AS latitude,
   lon_centroid AS longitude,
   CAST(fire_count AS INTEGER) AS fire_count,
   CAST(fire_count AS DOUBLE) AS heatmap_weight,
   area_km2,
   density_per_km2,
   frp_mw
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
  AND lat_centroid BETWEEN -90 AND 90
  AND lon_centroid BETWEEN -180 AND 180
ORDER BY month_start DESC, heatmap_weight DESC, region_id, biome_id;
