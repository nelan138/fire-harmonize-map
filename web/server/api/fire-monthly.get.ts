import { listValue } from "@duckdb/node-api";
import type { FireMonthly } from "#shared/types/FireMonthly";
import { queryFireData } from "../utils/duckdb";
import { normalizeFireMonthly } from "../utils/fire-data-rows";

export default defineEventHandler(async (event): Promise<FireMonthly[]> => {
   const query = getQuery(event).regions;
   const regions = query === undefined ? [] : Array.isArray(query) ? query : [query];
   if (regions.some((region) => typeof region !== "string" || !region.trim())) {
      throw createError({ statusCode: 400, statusMessage: "Regions must be nonempty strings" });
   }

   const sql = await useStorage("assets:sql").getItem<string>("fire-monthly.sql");
   if (!sql) throw createError({ statusCode: 500, statusMessage: "Monthly fire query is missing" });

   const rows = await queryFireData(
      sql,
      useRuntimeConfig(event).fireDataBaseUrl,
      "harmonized_fire_monthly.parquet",
      { regions: regions.length ? listValue(regions) : null },
   );
   return rows.map(normalizeFireMonthly);
});
