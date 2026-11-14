export type FireEvent = {
   latitude: number;
   longitude: number;
   frp: number;
   confidence: string | number;
   acq_date: string;
   acq_time: number;
   satellite: string;
   instrument: string;
   daynight: string;
   region_id: string;
   biome_id: string | null;
};
