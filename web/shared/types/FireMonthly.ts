export type FireMonthly = {
   region_id: string;
   year: number;
   month: number;
   h3_index: string | null;
   biome_id: number | null;
   lat_centroid: number | null;
   lon_centroid: number | null;
   raw_modis_count: number | null;
   raw_viirs_count: number | null;
   raw_frp_mw: number | null;
   adj_fire_count: number | null;
   adj_frp_mw: number | null;
   sfai_zscore: number | null;
   sfai_alert_lvl: number | null;
};
