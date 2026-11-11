import * as duckdb from "@duckdb/duckdb-wasm";
import duckdbEhWorker from "@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url";
import duckdbMvpWorker from "@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url";
import duckdbEhWasm from "@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url";
import duckdbMvpWasm from "@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url";

import type { DuckDBDatabase } from "./duckdb-service";

const LOCAL_BUNDLES: duckdb.DuckDBBundles = {
   mvp: {
      mainModule: duckdbMvpWasm,
      mainWorker: duckdbMvpWorker,
   },
   eh: {
      mainModule: duckdbEhWasm,
      mainWorker: duckdbEhWorker,
   },
};

const DATA_FILES = [
   {
      fileName: "harmonized_fire_monthly.parquet",
      viewName: "harmonized_fire_monthly",
   },
   {
      fileName: "fire_events.parquet",
      viewName: "fire_events",
   },
] as const;

export const createBrowserDuckDB = async (): Promise<DuckDBDatabase> => {
   const bundle = await duckdb.selectBundle(LOCAL_BUNDLES);
   if (!bundle.mainWorker) {
      throw new Error("DuckDB did not provide a compatible browser worker");
   }

   const worker = new Worker(bundle.mainWorker);
   const logger = new duckdb.ConsoleLogger(duckdb.LogLevel.WARNING);
   const database = new duckdb.AsyncDuckDB(logger, worker);
   let connection: duckdb.AsyncDuckDBConnection | null = null;

   try {
      await database.instantiate(bundle.mainModule, bundle.pthreadWorker);

      for (const { fileName } of DATA_FILES) {
         await database.registerFileURL(
            fileName,
            new URL(`/data/${fileName}`, window.location.origin).href,
            duckdb.DuckDBDataProtocol.HTTP,
            false,
         );
      }

      connection = await database.connect();
      try {
         for (const { fileName, viewName } of DATA_FILES) {
            await connection.query(`
               CREATE OR REPLACE VIEW ${viewName} AS
               SELECT * FROM parquet_scan('${fileName}')
            `);
         }
      } finally {
         await connection.close();
         connection = null;
      }

      return database as unknown as DuckDBDatabase;
   } catch (cause) {
      await connection?.close().catch(() => undefined);
      await database.terminate();
      throw cause;
   }
};
