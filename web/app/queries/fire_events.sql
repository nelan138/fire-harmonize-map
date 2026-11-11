SELECT
   latitude,
   longitude,
   frp,
   confidence,
   acq_date,
   acq_time,
   satellite,
   instrument,
   daynight,
   region_id,
   biome_id
FROM fire_events
WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
  AND region_id = 'INDOCHINA'
LIMIT 1000;
