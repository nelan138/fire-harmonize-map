<template>
   <div class="overflow-x-auto p-1">
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
            <div class="pr-2 text-left text-sm font-medium text-muted">
               {{ yAxis[y] }}
            </div>

            <HeatmapGrid
               v-for="grid in grids"
               :key="grid.key"
               :value="grid.value"
               :color="grid.color"
               :tooltip="grid.tooltip"
               :label="grid.label"
               :selected="!!grid.activity && grid.activity === selectedActivity"
               :disabled="!grid.activity"
               @select="grid.activity && emit('select', grid.activity)"
            />
         </template>
      </div>
   </div>
</template>

<script lang="ts" setup>
import type { FireActivity } from "../types/FireActivity";

type ValidValue = string | number;

const { activities, selectedActivity = null } = defineProps<{
   activities: FireActivity[];
   selectedActivity?: FireActivity | null;
}>();
const emit = defineEmits<{ select: [activity: FireActivity] }>();

const xAxis = computed(() =>
   [...new Set(activities.map((activity) => activity.year))].sort((a, b) => a - b),
);
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

type HeatmapGrid = {
   key: string;
   value?: ValidValue;
   color: HeatmapGridColor;
   tooltip?: string;
   label: string;
   activity?: FireActivity;
};

const gridMatrix = computed<HeatmapGrid[][]>(() => {
   const activitiesByPosition = new Map(
      activities.map((activity) => [
         `${activity.month}:${activity.year}`,
         activity,
      ]),
   );

   return yAxis.value.map((_, y) =>
      xAxis.value.map((year, x) => {
         const activity = activitiesByPosition.get(`${y + 1}:${year}`);

         return {
            key: `${y}:${x}`,
            activity,
            label: activity
               ? `${activity.region_id.replaceAll("_", " ")}, ${yAxis.value[y]} ${year}`
               : `${yAxis.value[y]} ${year}: no monthly data`,
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
</script>
