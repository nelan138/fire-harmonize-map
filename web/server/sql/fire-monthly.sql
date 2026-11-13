SELECT
   region_id,
   CAST(year AS INTEGER) AS year,
   CAST(month AS INTEGER) AS month,
   CAST(adj_fire_count AS DOUBLE) AS adj_fire_count,
   CAST(sfai_alert_lvl AS INTEGER) AS sfai_alert_lvl
FROM fire_monthly
ORDER BY region_id, year, month
LIMIT 1000