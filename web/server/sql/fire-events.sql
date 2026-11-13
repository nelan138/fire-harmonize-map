SELECT
   latitude,
   longitude,
   frp,
   confidence,
   CAST(acq_date AS VARCHAR) AS acq_date,
   CAST(acq_time AS INTEGER) AS acq_time,
   satellite,
   instrument,
   daynight,
   region_id,
   biome_id
FROM fire_events
WHERE latitude IS NOT NULL AND longitude IS NOT NULL
