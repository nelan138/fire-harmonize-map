import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { queryFireData } from "../server/utils/duckdb";

const dataBaseUrl = "https://huggingface.co/datasets/leveluplevelyn/fire_event_nasaspaceapps/resolve/main/";
const sql = (name: string) => readFile(resolve("server/sql", name), "utf8");

describe("fire data queries", () => {
   it("returns JSON-safe events from Hugging Face for the map", async () => {
      const rows = await queryFireData(await sql("calibrated-fire-events.sql"), dataBaseUrl);
      expect(rows.length).toBeGreaterThan(0);
      expect(rows.length).toBeLessThanOrEqual(1000);
      for (const row of rows) {
         expect(row.region_id).toBe("INDOCHINA");
         expect(typeof row.latitude).toBe("number");
         expect(typeof row.longitude).toBe("number");
      }
      expect(() => JSON.stringify(rows)).not.toThrow();
   }, 60000);

   it("returns monthly heatmap values in chronological order", async () => {
      const rows = await queryFireData(await sql("fire-monthly.sql"), dataBaseUrl);
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
   }, 60000);
});
