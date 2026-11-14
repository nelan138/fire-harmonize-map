import type { FireActivity } from "../types/FireActivity";

export function getHistoricalChange(
   selected: FireActivity,
   activities: FireActivity[] | null,
): number | null {
   if (!activities || !Number.isFinite(selected.adj_fire_count) || selected.adj_fire_count < 0) {
      return null;
   }

   const history = activities.filter((activity) =>
      activity.region_id === selected.region_id &&
      activity.month === selected.month &&
      (activity.biome_id ?? null) === (selected.biome_id ?? null) &&
      (activity.h3_index ?? null) === (selected.h3_index ?? null) &&
      activity.year >= 2000 && activity.year <= 2024,
   );
   const years = new Set(history.map((activity) => activity.year));
   if (
      years.size < 2 || years.size !== history.length ||
      history.some((activity) => !Number.isFinite(activity.adj_fire_count) || activity.adj_fire_count < 0)
   ) {
      return null;
   }

   const mean = history.reduce((sum, activity) => sum + activity.adj_fire_count, 0) / history.length;
   if (mean === 0) return null;

   const change = ((selected.adj_fire_count - mean) / mean) * 100;
   return Number.isFinite(change) ? change : null;
}
