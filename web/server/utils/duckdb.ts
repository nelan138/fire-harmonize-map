import { DuckDBInstance } from "@duckdb/node-api";
import { resolve } from "node:path";

let database: Promise<DuckDBInstance> | undefined;

export async function queryFireData(sql: string, dataDir: string) {
   database ??= DuckDBInstance.create(":memory:").catch((error) => {
      database = undefined;
      throw error;
   });
   const connection = await (await database).connect();

   try {
      for (const [view, file] of [
         ["fire_events", "calibrated_fire_events.parquet"],
         ["fire_monthly", "fire_monthly.parquet"],
      ] as const) {
         const path = resolve(dataDir, file).replaceAll("\\", "/").replaceAll("'", "''");
         await connection.run(
            `CREATE TEMP VIEW ${view} AS SELECT * FROM read_parquet('${path}')`,
         );
      }

      const result = await connection.runAndReadAll(sql);
      return result.getRowObjectsJson();
   } finally {
      connection.closeSync();
   }
}
