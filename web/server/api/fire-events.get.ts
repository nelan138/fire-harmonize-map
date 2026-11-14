import type { FireEvent } from "#shared/types/FireEvent";
import { queryFireData } from "../utils/duckdb";
import { normalizeFireEvent } from "../utils/fire-data-rows";

export default defineEventHandler(async (event): Promise<FireEvent[]> => {
   const sql = await useStorage("assets:sql").getItem<string>("fire-events.sql");
   if (!sql) throw createError({ statusCode: 500, statusMessage: "Fire events query is missing" });

   const rows = await queryFireData(
      sql,
      useRuntimeConfig(event).fireDataBaseUrl,
      "GLOBAL_5_REGIONS_clean_fire_events.parquet",
   );
   return rows.map(normalizeFireEvent);
});
