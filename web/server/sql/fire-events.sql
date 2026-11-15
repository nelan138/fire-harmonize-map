SELECT
   CAST(latitude AS DOUBLE) AS latitude,
   CAST(longitude AS DOUBLE) AS longitude,
   TRY_CAST(frp AS DOUBLE) AS frp,
   confidence,
   CAST(acq_date AS VARCHAR) AS acq_date,
   TRY_CAST(acq_time AS INTEGER) AS acq_time,
   satellite,
   instrument,
   daynight,
   region_id,
   CAST(biome_id AS VARCHAR) AS biome_id
FROM read_parquet($path)
WHERE latitude IS NOT NULL AND longitude IS NOT NULL AND region_id = 'INDOCHINA'
LIMIT 1000
