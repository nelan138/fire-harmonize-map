export type BurningData = {
   region_id: string;
   year: number;
   month: number;
   adj_fire_count: number;
   sfai_alert_lvl: number;
};

export async function getBurningData(): Promise<BurningData[]> {
   const duckDb = useDuckDB();

   const result = await duckDb.query<BurningData>(`
      SELECT
         region_id,
         year,
         month,
         adj_fire_count,
         sfai_alert_lvl
      FROM harmonized_fire_monthly
      WHERE region_id = 'INDOCHINA'
      ORDER BY region_id, year, month
   `);

   return result;
}
