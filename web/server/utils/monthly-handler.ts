import type { H3Event } from "h3";
import { parseMonthlyFilters } from "./monthly-filters";
import { queryHarmonizedMonthly } from "./duckdb";

export async function handleMonthlyQuery(event: H3Event, filename: "fire-history.sql" | "fire-density.sql") {
   const filters = parseMonthlyFilters(getQuery(event));
   const sql = await useStorage("assets:sql").getItem<string>(filename);
   if (!sql) throw createError({ statusCode: 500, statusMessage: "Monthly SQL query is missing" });
   const config = useRuntimeConfig(event);
   const path = filename === "fire-density.sql" ? config.fireDensityPath : config.harmonizedMonthlyPath;
   return queryHarmonizedMonthly(sql, path, filters);
}
