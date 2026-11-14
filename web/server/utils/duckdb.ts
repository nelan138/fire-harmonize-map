import { DuckDBInstance, type DuckDBValue } from "@duckdb/node-api";

let database: Promise<DuckDBInstance> | undefined;

async function connectFireDatabase() {
   database ??= DuckDBInstance.create(":memory:").catch((error) => {
      database = undefined;
      throw error;
   });
   return (await database).connect();
}

export async function queryFireData(
   sql: string,
   dataBaseUrl: string,
   file: string,
   params: Record<string, DuckDBValue> = {},
) {
   const path = new URL(file, `${dataBaseUrl.replace(/\/+$/, "")}/`).href;
   const connection = await connectFireDatabase();

   try {
      const result = await connection.runAndReadAll(sql, { ...params, path });
      return result.getRowObjectsJson();
   } finally {
      connection.closeSync();
   }
}
