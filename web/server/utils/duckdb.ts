import { DuckDBInstance } from "@duckdb/node-api";

let database: Promise<DuckDBInstance> | undefined;

async function connectFireDatabase() {
   database ??= DuckDBInstance.create(":memory:").catch((error) => {
      database = undefined;
      throw error;
   });
   return (await database).connect();
}

export async function queryFireData(sql: string, dataBaseUrl: string) {
   const connection = await connectFireDatabase();

   try {
      for (const [view, file] of [
         ["fire_events", "fire_events.parquet"],
         ["fire_monthly", "fire_monthly.parquet"],
      ] as const) {
         const path = new URL(
            file,
            `${dataBaseUrl.replace(/\/+$/, "")}/`,
         ).href.replaceAll("'", "''");
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
