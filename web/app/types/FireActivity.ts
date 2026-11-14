export type FireActivity = {
   region_id: string;
   year: number;
   month: number;
   adj_fire_count: number;
   sfai_alert_lvl: number;
   sfai_zscore?: number | null;
   historical_change: number | string | null;

   /* ? Additional fields maybe */
   h3_index?: string | null;
   biome_id?: number | null;
   lat_centroid?: number | null;
   lon_centroid?: number | null;
   raw_modis_count?: number | null;
   raw_viirs_count?: number | null;
   raw_frp_mw?: number | null;
   adj_frp_mw?: number | null;
};
