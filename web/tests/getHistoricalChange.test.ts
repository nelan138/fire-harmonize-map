import { describe, expect, it } from "vitest";
import type { FireActivity } from "../app/types/FireActivity";
import { getHistoricalChange } from "../app/utils/getHistoricalChange";

function record(overrides: Partial<FireActivity> = {}): FireActivity {
   return {
      region_id: "INDOCHINA",
      year: 2024,
      month: 3,
      biome_id: 1,
      h3_index: "N/A",
      adj_fire_count: 150,
      sfai_alert_lvl: 2,
      historical_change: null,
      ...overrides,
   };
}

describe("getHistoricalChange", () => {
   const history = [
      record({ year: 2000, adj_fire_count: 50 }),
      record({ year: 2012, adj_fire_count: 100 }),
      record(),
   ];

   it.each([
      [150, 50],
      [50, -50],
      [100, 0],
      [0, -100],
   ])("compares %i detections with the historical mean", (count, expected) => {
      expect(getHistoricalChange(record({ adj_fire_count: count }), history)).toBe(expected);
   });

   it("matches region, calendar month, biome and H3 within 2000–2024", () => {
      const unrelated = [
         record({ region_id: "OTHER", year: 2001, adj_fire_count: 9999 }),
         record({ month: 4, year: 2002, adj_fire_count: 9999 }),
         record({ biome_id: 2, year: 2003, adj_fire_count: 9999 }),
         record({ h3_index: "OTHER_CELL", year: 2004, adj_fire_count: 9999 }),
         record({ year: 1999, adj_fire_count: 9999 }),
         record({ year: 2025, adj_fire_count: 9999 }),
      ];
      expect(getHistoricalChange(record(), [...history, ...unrelated])).toBe(50);
   });

   it("does not treat missing identifiers as all biomes or cells", () => {
      expect(getHistoricalChange(record({ biome_id: undefined }), history)).toBeNull();
      expect(getHistoricalChange(record({ h3_index: undefined }), history)).toBeNull();
   });

   it("treats null and omitted identifiers consistently", () => {
      const historyWithoutIds = history.map((activity) => ({
         ...activity, biome_id: null, h3_index: null,
      }));
      expect(getHistoricalChange(
         record({ biome_id: undefined, h3_index: undefined }), historyWithoutIds,
      )).toBe(50);
   });

   it("returns null for unloaded, missing or insufficient history", () => {
      expect(getHistoricalChange(record(), null)).toBeNull();
      expect(getHistoricalChange(record(), [])).toBeNull();
      expect(getHistoricalChange(record(), [record()])).toBeNull();
   });

   it("rejects duplicate matching years instead of overweighting them", () => {
      expect(getHistoricalChange(record(), [...history, record()])).toBeNull();
   });

   it("returns null for a zero historical mean", () => {
      const zeroHistory = history.map((activity) => ({ ...activity, adj_fire_count: 0 }));
      expect(getHistoricalChange(record(), zeroHistory)).toBeNull();
   });

   it.each([NaN, Infinity, -1])("rejects an invalid count: %s", (count) => {
      expect(getHistoricalChange(record({ adj_fire_count: count }), history)).toBeNull();
      expect(getHistoricalChange(record(), [
         ...history.slice(0, 2), record({ adj_fire_count: count }),
      ])).toBeNull();
   });

   it("returns an unrounded number without changing fetched records", () => {
      const selected = Object.freeze(record({ adj_fire_count: 120, historical_change: "untouched" }));
      const history = [
         Object.freeze(record({ year: 2000, adj_fire_count: 80 })),
         selected,
      ];
      expect(getHistoricalChange(selected, history)).toBe(20);
      expect(selected.historical_change).toBe("untouched");
      expect(getHistoricalChange(record({ adj_fire_count: 1 }), [
         record({ year: 2000, adj_fire_count: 1 }),
         record({ year: 2024, adj_fire_count: 2 }),
      ])).toBeCloseTo(-33.33333333333333);
   });
});
