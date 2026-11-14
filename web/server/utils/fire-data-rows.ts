import type { FireEvent } from "#shared/types/FireEvent";
import type { FireMonthly } from "#shared/types/FireMonthly";

function finiteNumber(value: unknown): number | null {
   return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function nonemptyString(value: unknown): string | null {
   return typeof value === "string" && value.trim() ? value : null;
}

export function normalizeFireEvent(row: Record<string, unknown>): FireEvent {
   const latitude = finiteNumber(row.latitude);
   const longitude = finiteNumber(row.longitude);
   const region = nonemptyString(row.region_id);
   if (latitude === null || longitude === null || region === null) {
      throw new Error("Fire event is missing a valid location or region");
   }

   return {
      latitude,
      longitude,
      frp: finiteNumber(row.frp),
      confidence: finiteNumber(row.confidence) ?? nonemptyString(row.confidence),
      acq_date: nonemptyString(row.acq_date),
      acq_time: finiteNumber(row.acq_time),
      satellite: nonemptyString(row.satellite),
      instrument: nonemptyString(row.instrument),
      daynight: nonemptyString(row.daynight),
      region_id: region,
      biome_id: nonemptyString(row.biome_id),
   };
}

export function normalizeFireMonthly(row: Record<string, unknown>): FireMonthly {
   const region = nonemptyString(row.region_id);
   const year = finiteNumber(row.year);
   const month = finiteNumber(row.month);
   if (
      region === null ||
      year === null || !Number.isInteger(year) ||
      month === null || !Number.isInteger(month) || month < 1 || month > 12
   ) {
      throw new Error("Monthly fire record is missing a valid region, year, or month");
   }

   return {
      region_id: region,
      year,
      month,
      h3_index: nonemptyString(row.h3_index),
      biome_id: finiteNumber(row.biome_id),
      lat_centroid: finiteNumber(row.lat_centroid),
      lon_centroid: finiteNumber(row.lon_centroid),
      raw_modis_count: finiteNumber(row.raw_modis_count),
      raw_viirs_count: finiteNumber(row.raw_viirs_count),
      raw_frp_mw: finiteNumber(row.raw_frp_mw),
      adj_fire_count: finiteNumber(row.adj_fire_count),
      adj_frp_mw: finiteNumber(row.adj_frp_mw),
      sfai_zscore: finiteNumber(row.sfai_zscore),
      sfai_alert_lvl: finiteNumber(row.sfai_alert_lvl),
   };
}
