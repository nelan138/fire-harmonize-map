<template>
   <div class="overflow-x-auto">
      <div
         class="grid w-fit items-center gap-2"
         :style="{
            gridTemplateColumns: `max-content repeat(${xAxis.length}, 2.5rem)`,
         }"
      >
         <div aria-hidden="true" />

         <div
            v-for="(label, x) in xAxis"
            :key="`x-${x}`"
            class="text-center text-xs font-medium text-muted"
         >
            {{ label }}
         </div>

         <template v-for="(grids, y) in gridMatrix" :key="`y-${y}`">
            <div class="pr-2 text-sm font-medium text-muted">
               {{ yAxis[y] }}
            </div>

            <HeatmapGrid
               v-for="grid in grids"
               :key="grid.key"
               :value="grid.value"
               :color="grid.color"
               :tooltip="grid.tooltip"
            />
         </template>
      </div>
   </div>
</template>

<script lang="ts" setup>
type ValidValue = string | number;

const xAxis = ref<ValidValue[]>([]);
const yAxis = shallowRef<ValidValue[]>([
   "January",
   "February",
   "March",
   "April",
   "May",
   "June",
   "July",
   "August",
   "September",
   "October",
   "November",
   "December",
]);

import query from "~/queries/fire_activities.sql?raw";

const toast = useToast();

const fireActivities = ref<FireActivity[]>();

onMounted(async () => {
   const duckDb = useDuckDB();

   const [queryResults, error] = await tryCatch(
      duckDb.query<FireActivity>(query),
   );

   if (queryResults) {
      fireActivities.value = queryResults;
      xAxis.value = [
         ...new Set(queryResults.map((activity) => activity.year)),
      ].sort((a, b) => a - b);
   }

   if (error) {
      toast.add({
         title: "Unable to load fire activities",
         description: error.message,
         color: "error",
         icon: "lucide:alert-octagon",
      });
   }
});

type HeatmapGrid = {
   key: string;
   value?: ValidValue;
   color: HeatmapGridColor;
   tooltip?: string;
   filterValue?: ValidValue;
};

const gridMatrix = computed<HeatmapGrid[][]>(() => {
   const activitiesByPosition = new Map(
      (fireActivities.value ?? []).map((activity) => [
         `${activity.month}:${activity.year}`,
         activity,
      ]),
   );

   return yAxis.value.map((_, y) =>
      xAxis.value.map((year, x) => {
         const activity = activitiesByPosition.get(`${y + 1}:${year}`);

         return {
            key: `${y}:${x}`,
            color: activity
               ? getAlertLevelColor(activity.sfai_alert_lvl)
               : "gray",
            tooltip: activity
               ? `Fire Count: ${activity.adj_fire_count}\nAlert Level: ${activity.sfai_alert_lvl}`
               : undefined,
         };
      }),
   );
});

const colors: Record<number, HeatmapGridColor> = {
   1: "green",
   2: "yellow",
   3: "orange",
   4: "red",
   5: "darkred",
};

function getAlertLevelColor(alertLevel: number) {
   return colors[alertLevel] ?? "gray";
}
</script>
