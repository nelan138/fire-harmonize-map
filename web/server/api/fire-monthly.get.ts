import type { FireActivity } from "../../app/types/FireActivity";
import { queryFireData } from "../utils/duckdb";

export default defineEventHandler(async (event): Promise<FireActivity[]> => {
   const sql = await useStorage("assets:sql").getItem<string>("fire-monthly.sql");
   if (!sql) throw createError({ statusCode: 500, statusMessage: "Monthly fire query is missing" });

   return await queryFireData(sql, useRuntimeConfig(event).fireDataDir) as FireActivity[];
});
