import { readonly, ref, type Ref } from "vue";

export type DuckDBStatus = "idle" | "initializing" | "ready" | "error";
export type DuckDBRow = Record<string, unknown>;

export interface DuckDBResultRow {
   toJSON(): DuckDBRow;
}

export interface DuckDBResult {
   toArray(): DuckDBResultRow[];
}

export interface DuckDBPreparedStatement {
   query(...params: unknown[]): Promise<DuckDBResult>;
   close(): Promise<void>;
}

export interface DuckDBConnection {
   query(sql: string): Promise<DuckDBResult>;
   prepare(sql: string): Promise<DuckDBPreparedStatement>;
   close(): Promise<void>;
}

export interface DuckDBDatabase {
   connect(): Promise<DuckDBConnection>;
   terminate(): Promise<void>;
}

export type DuckDBFactory = () => Promise<DuckDBDatabase>;

export interface DuckDBService {
   status: Readonly<Ref<DuckDBStatus>>;
   error: Readonly<Ref<Error | null>>;
   query<T extends DuckDBRow>(sql: string, params?: readonly unknown[]): Promise<T[]>;
   dispose(): Promise<void>;
}

const toError = (cause: unknown): Error =>
   cause instanceof Error ? cause : new Error(String(cause));

export const createDuckDBService = (factory: DuckDBFactory): DuckDBService => {
   const status = ref<DuckDBStatus>("idle");
   const error = ref<Error | null>(null);

   let database: DuckDBDatabase | null = null;
   let initialization: Promise<DuckDBDatabase> | null = null;
   let disposal: Promise<void> | null = null;
   let disposed = false;

   const getDatabase = (): Promise<DuckDBDatabase> => {
      if (disposed) {
         return Promise.reject(new Error("DuckDB has been disposed"));
      }

      if (database) {
         return Promise.resolve(database);
      }

      if (!initialization) {
         status.value = "initializing";
         error.value = null;
         initialization = factory().then(
            (instance) => {
               database = instance;
               status.value = "ready";
               return instance;
            },
            (cause: unknown) => {
               const initializationError = toError(cause);
               error.value = initializationError;
               status.value = "error";
               throw initializationError;
            },
         );
      }

      return initialization;
   };

   const query = async <T extends DuckDBRow>(
      sql: string,
      params: readonly unknown[] = [],
   ): Promise<T[]> => {
      const instance = await getDatabase();
      const connection = await instance.connect();
      let statement: DuckDBPreparedStatement | null = null;

      try {
         const queryResult = params.length
            ? await (statement = await connection.prepare(sql)).query(...params)
            : await connection.query(sql);

         return queryResult.toArray().map((row) => row.toJSON() as T);
      } finally {
         try {
            await statement?.close();
         } finally {
            await connection.close();
         }
      }
   };

   const dispose = (): Promise<void> => {
      if (disposal) {
         return disposal;
      }

      disposed = true;
      disposal = (async () => {
         const instance = database ?? (await initialization?.catch(() => null)) ?? null;
         database = null;
         if (instance) {
            await instance.terminate();
         }
      })();

      return disposal;
   };

   return {
      status: readonly(status),
      error: readonly(error),
      query,
      dispose,
   };
};
