export type FireEvent = {
   latitude: number;
   longitude: number;
   frp: number | null;
   confidence: string | number | null;
   acq_date: string | null;
   acq_time: number | null;
   satellite: string | null;
   instrument: string | null;
   daynight: string | null;
   region_id: string;
   biome_id: string | null;
};
