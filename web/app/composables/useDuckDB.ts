import type { DuckDBService } from "~/utils/duckdb-service";

export const useDuckDB = (): DuckDBService => useNuxtApp().$duckdb;
