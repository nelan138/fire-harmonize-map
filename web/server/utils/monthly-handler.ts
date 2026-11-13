import { createError, type H3Event } from "h3";
import { queryHarmonizedMonthly } from "./duckdb";

const regions = ["INDOCHINA", "AMAZON", "CALIFORNIA", "PANTANAL", "SE_AUSTRALIA"];

export async function handleMonthlyQuery(event: H3Event, filename: "fire-history.sql" | "fire-density.sql") {
   const filters = parseMonthlyFilters(getQuery(event));
   const sql = await useStorage("assets:sql").getItem<string>(filename);
   if (!sql) throw createError({ statusCode: 500, statusMessage: "Monthly SQL query is missing" });
   const config = useRuntimeConfig(event);
   const path = filename === "fire-density.sql" ? config.fireDensityPath : config.harmonizedMonthlyPath;
   return queryHarmonizedMonthly(sql, path, filters);
}

function parseMonthlyFilters(query: Record<string, unknown>) {
   const invalid = (message: string): never => {
      throw createError({ statusCode: 400, statusMessage: message });
   };
   const allowed = new Set(["date_from", "date_to", "year", "month", "region_id", "biome_id", "min_lat", "max_lat", "min_lon", "max_lon"]);
   for (const key of Object.keys(query)) {
      if (!allowed.has(key)) invalid(`Unknown query parameter: ${key}`);
   }
   const text = (key: string): string | null => {
      const value = query[key];
      if (value === undefined) return null;
      if (typeof value !== "string" || !value.trim()) invalid(`${key} must be a single non-empty value`);
      return (value as string).trim();
   };
   const number = (key: string, min: number, max: number, integer = false) => {
      const value = text(key);
      if (value === null) return null;
      const parsed = Number(value);
      if (!Number.isFinite(parsed) || parsed < min || parsed > max || (integer && !Number.isInteger(parsed))) {
         invalid(`${key} must be ${integer ? "an integer" : "a number"} between ${min} and ${max}`);
      }
      return parsed;
   };
   const date = (key: string) => {
      const value = text(key);
      if (value === null) return null;
      if (!/^\d{4}-\d{2}-\d{2}$/.test(value) || value.startsWith("0000")) invalid(`${key} must be a valid YYYY-MM-DD date`);
      const parsed = new Date(`${value}T00:00:00Z`);
      if (!Number.isFinite(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== value) invalid(`${key} must be a valid YYYY-MM-DD date`);
      return value;
   };
   const filters = {
      date_from: date("date_from"),
      date_to: date("date_to"),
      selected_year: number("year", 1, 9999, true),
      selected_month: number("month", 1, 12, true),
      selected_region: text("region_id")?.toUpperCase() ?? null,
      selected_biome: number("biome_id", 1, 4, true),
      min_lat: number("min_lat", -90, 90),
      max_lat: number("max_lat", -90, 90),
      min_lon: number("min_lon", -180, 180),
      max_lon: number("max_lon", -180, 180),
   };
   if (filters.selected_region && !regions.includes(filters.selected_region)) invalid(`region_id must be one of: ${regions.join(", ")}`);
   if (filters.date_from && filters.date_to && filters.date_from > filters.date_to) invalid("date_from must be before or equal to date_to");
   if (filters.min_lat !== null && filters.max_lat !== null && filters.min_lat > filters.max_lat) invalid("min_lat must be <= max_lat");
   if (filters.min_lon !== null && filters.max_lon !== null && filters.min_lon > filters.max_lon) invalid("min_lon must be <= max_lon");
   return filters;
}
