export function getHistoricalChange(
   count: number | null,
   history: readonly number[],
): number | null {
   if (count === null || !Number.isFinite(count) || count < 0 || history.length < 2) return null;
   if (history.some((value) => !Number.isFinite(value) || value < 0)) return null;

   const mean = history.reduce((sum, value) => sum + value, 0) / history.length;
   if (mean === 0) return null;

   const change = ((count - mean) / mean) * 100;
   return Number.isFinite(change) ? change : null;
}
