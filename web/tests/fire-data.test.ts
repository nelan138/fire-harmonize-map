import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { queryFireData } from "../server/utils/duckdb";

const dataDir = resolve("public/data");
const sql = (name: string) => readFile(resolve("server/sql", name), "utf8");

describe("fire data queries", () => {
   it("returns JSON-safe calibrated events for the map", async () => {
      const rows = await queryFireData(await sql("calibrated-fire-events.sql"), dataDir);
      expect(rows.length).toBeGreaterThan(0);
      expect(rows.length).toBeLessThanOrEqual(1000);
      for (const row of rows) {
         expect(row.region_id).toBe("INDOCHINA");
         expect(typeof row.latitude).toBe("number");
         expect(typeof row.longitude).toBe("number");
      }
      expect(() => JSON.stringify(rows)).not.toThrow();
   });

   it("returns monthly heatmap values in chronological order", async () => {
      const rows = await queryFireData(await sql("fire-monthly.sql"), dataDir);
      expect(rows.length).toBeGreaterThan(0);
      const positions = rows.map((row) => Number(row.year) * 12 + Number(row.month));
      expect(positions).toEqual([...positions].sort((a, b) => a - b));
      for (const row of rows) {
         expect(row.region_id).toBe("INDOCHINA");
         expect(typeof row.adj_fire_count).toBe("number");
         expect(row.month).toBeGreaterThanOrEqual(1);
         expect(row.month).toBeLessThanOrEqual(12);
      }
      expect(() => JSON.stringify(rows)).not.toThrow();
   });
});
