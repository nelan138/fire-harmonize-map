import { describe, expect, it } from "vitest";
import type { FireMonthly } from "../shared/types/FireMonthly";
import { getHistoricalChange } from "../app/utils/getHistoricalChange";
import { getSelectedFireMonth, groupFireMonths } from "../app/utils/getSelectedFireMonth";

function row(overrides: Partial<FireMonthly> = {}): FireMonthly {
   return {
      region_id: "INDOCHINA",
      year: 2024,
      month: 3,
      h3_index: "N/A",
      biome_id: 1,
      lat_centroid: null,
      lon_centroid: null,
      adj_fire_count: 150,
      raw_modis_count: 30,
      raw_viirs_count: 90,
      raw_frp_mw: null,
      adj_frp_mw: null,
      sfai_zscore: null,
      sfai_alert_lvl: 2,
      ...overrides,
   };
}

describe("getHistoricalChange", () => {
   it.each([[150, 50], [50, -50], [100, 0], [0, -100]])(
      "compares %i detections with the historical mean",
      (count, expected) => expect(getHistoricalChange(count, [50, 100, 150])).toBe(expected),
   );

   it.each([null, NaN, Infinity, -1])("rejects an invalid count: %s", (count) => {
      expect(getHistoricalChange(count, [50, 150])).toBeNull();
   });

   it.each([[], [100], [0, 0], [50, NaN], [50, Infinity], [50, -1]])(
      "rejects invalid or insufficient history: %j",
      (first, second) => expect(getHistoricalChange(100, [first, second].filter((n) => n !== undefined))).toBeNull(),
   );

   it("returns an unrounded percentage", () => {
      expect(getHistoricalChange(1, [1, 2])).toBeCloseTo(-33.33333333333333);
   });
});

describe("selected fire month", () => {
   it("keeps every biome and H3 row under one stable regional key", () => {
      const primary = Object.freeze(row());
      const rows = [primary, row({ biome_id: 2, adj_fire_count: 50 }), row({ h3_index: "H3", adj_fire_count: 20 })];
      const months = groupFireMonths(rows);

      expect(months).toHaveLength(1);
      expect(months[0]).toMatchObject({
         key: "INDOCHINA:2024:3",
         rows,
         selectedRecord: null,
         totals: { fireCount: 220, rawModisCount: 90, rawViirsCount: 270 },
      });
      expect(primary.adj_fire_count).toBe(150);
   });

   it("compares regional totals for the same calendar month in the baseline years", () => {
      const months = groupFireMonths([
         row(),
         row({ biome_id: 2, adj_fire_count: 50 }),
         row({ year: 1999 }),
         row({ year: 2000, adj_fire_count: 100 }),
         row({ year: 2001, adj_fire_count: null }),
         row({ year: 2012, month: 4 }),
         row({ year: 2012, region_id: "OTHER" }),
         row({ year: 2025 }),
      ]);

      const selected = getSelectedFireMonth(months[0]!, months);
      expect(selected.history).toEqual([{ year: 2024, count: 200 }, { year: 2000, count: 100 }]);
      expect(selected.historicalChange).toBeCloseTo(100 / 3);
   });

   it("preserves zero counts and treats an incomplete total as unavailable", () => {
      const first = row({ raw_modis_count: null, raw_viirs_count: 0 });
      const months = groupFireMonths([first]);
      expect(months[0]).toMatchObject({
         selectedRecord: first,
         totals: { fireCount: 150, rawModisCount: null, rawViirsCount: 0 },
      });
   });
});
