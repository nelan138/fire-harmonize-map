import type { FireMonthly } from "#shared/types/FireMonthly";
import { getHistoricalChange } from "./getHistoricalChange";

export type FireMonth = {
   key: string;
   regionId: string;
   year: number;
   month: number;
   rows: FireMonthly[];
   totals: {
      fireCount: number | null;
      rawModisCount: number | null;
      rawViirsCount: number | null;
   };
   selectedRecord: FireMonthly | null;
};

export type SelectedFireMonth = FireMonth & {
   history: { year: number; count: number }[];
   historicalChange: number | null;
};

function sumCounts(
   rows: FireMonthly[],
   field: "adj_fire_count" | "raw_modis_count" | "raw_viirs_count",
) {
   let total = 0;
   for (const row of rows) {
      const count = row[field];
      if (count == null || !Number.isFinite(count) || count < 0) return null;
      total += count;
   }
   return Number.isFinite(total) ? total : null;
}

export function groupFireMonths(rows: FireMonthly[]) {
   const groups = new Map<string, FireMonthly[]>();
   for (const row of rows) {
      const key = `${row.region_id}:${row.year}:${row.month}`;
      const group = groups.get(key);
      if (group) group.push(row);
      else groups.set(key, [row]);
   }

   return Array.from(groups, ([key, rows]): FireMonth => {
      const first = rows[0]!;
      return {
         key,
         regionId: first.region_id,
         year: first.year,
         month: first.month,
         rows,
         totals: {
            fireCount: sumCounts(rows, "adj_fire_count"),
            rawModisCount: sumCounts(rows, "raw_modis_count"),
            rawViirsCount: sumCounts(rows, "raw_viirs_count"),
         },
         selectedRecord: rows.length === 1 ? first : null,
      };
   });
}

export function getSelectedFireMonth(
   selected: FireMonth,
   months: FireMonth[],
): SelectedFireMonth {
   const history = months.flatMap(({ regionId, year, month, totals }) =>
      regionId === selected.regionId && month === selected.month &&
      year >= 2000 && year <= 2024 && totals.fireCount !== null
         ? [{ year, count: totals.fireCount }]
         : [],
   );

   return {
      ...selected,
      history,
      historicalChange: getHistoricalChange(selected.totals.fireCount, history.map(({ count }) => count)),
   };
}
