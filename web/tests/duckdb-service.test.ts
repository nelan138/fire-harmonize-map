import { describe, expect, it, vi } from "vitest";

import {
   createDuckDBService,
   type DuckDBConnection,
   type DuckDBDatabase,
   type DuckDBPreparedStatement,
   type DuckDBResult,
} from "../app/utils/duckdb-service";

const result = <T extends Record<string, unknown>>(rows: T[]): DuckDBResult => ({
   toArray: () => rows.map((row) => ({ toJSON: () => row })),
});

const createDatabase = (options?: {
   query?: DuckDBConnection["query"];
   prepare?: DuckDBConnection["prepare"];
}) => {
   const statement: DuckDBPreparedStatement = {
      query: vi.fn(async () => result([])),
      close: vi.fn(async () => undefined),
   };
   const connection: DuckDBConnection = {
      query: options?.query ?? vi.fn(async () => result([])),
      prepare: options?.prepare ?? vi.fn(async () => statement),
      close: vi.fn(async () => undefined),
   };
   const database: DuckDBDatabase = {
      connect: vi.fn(async () => connection),
      terminate: vi.fn(async () => undefined),
   };

   return { database, connection, statement };
};

describe("createDuckDBService", () => {
   it("initializes one database for concurrent queries and returns plain rows", async () => {
      const { database } = createDatabase({
         query: vi.fn(async () => result([{ region: "Indochina", fires: 42 }]))
      });
      const factory = vi.fn(async () => database);
      const service = createDuckDBService(factory);

      expect(service.status.value).toBe("idle");

      const [first, second] = await Promise.all([
         service.query<{ region: string; fires: number }>("select * from fires"),
         service.query<{ region: string; fires: number }>("select * from fires"),
      ]);

      expect(factory).toHaveBeenCalledTimes(1);
      expect(first).toEqual([{ region: "Indochina", fires: 42 }]);
      expect(second).toEqual(first);
      expect(service.status.value).toBe("ready");
   });

   it("binds parameters and closes the statement and connection", async () => {
      const { database, connection, statement } = createDatabase();
      const service = createDuckDBService(async () => database);

      await service.query("select * from fires where year = ? and month = ?", [2023, 3]);

      expect(connection.prepare).toHaveBeenCalledWith(
         "select * from fires where year = ? and month = ?",
      );
      expect(statement.query).toHaveBeenCalledWith(2023, 3);
      expect(statement.close).toHaveBeenCalledTimes(1);
      expect(connection.close).toHaveBeenCalledTimes(1);
   });

   it("records initialization failures as errors", async () => {
      const service = createDuckDBService(async () => {
         throw "WASM unavailable";
      });

      await expect(service.query("select 1")).rejects.toThrow("WASM unavailable");
      expect(service.status.value).toBe("error");
      expect(service.error.value).toEqual(new Error("WASM unavailable"));
   });

   it("closes query resources when execution fails", async () => {
      const { database, connection, statement } = createDatabase();
      vi.mocked(statement.query).mockRejectedValueOnce(new Error("bad query"));
      const service = createDuckDBService(async () => database);

      await expect(service.query("select ?", [1])).rejects.toThrow("bad query");

      expect(statement.close).toHaveBeenCalledTimes(1);
      expect(connection.close).toHaveBeenCalledTimes(1);
   });

   it("terminates an initialized database only once", async () => {
      const { database } = createDatabase();
      const service = createDuckDBService(async () => database);
      await service.query("select 1");

      await service.dispose();
      await service.dispose();

      expect(database.terminate).toHaveBeenCalledTimes(1);
   });
});
