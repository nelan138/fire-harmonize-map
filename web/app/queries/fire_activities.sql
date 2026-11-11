SELECT
   region_id,
   year,
   month,
   adj_fire_count,
   sfai_alert_lvl
FROM fire_monthly
WHERE region_id = 'INDOCHINA'
ORDER BY region_id, year, month
