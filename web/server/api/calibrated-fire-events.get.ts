import type { FireEvent } from "../../app/types/FireEvent";
import { queryFireData } from "../utils/duckdb";

export default defineEventHandler(async (event): Promise<FireEvent[]> => {
   const sql = await useStorage("assets:sql").getItem<string>("calibrated-fire-events.sql");
   if (!sql) throw createError({ statusCode: 500, statusMessage: "Fire events query is missing" });

   return await queryFireData(sql, useRuntimeConfig(event).fireDataDir) as FireEvent[];
});
