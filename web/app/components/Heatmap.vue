<template>
   <div class="overflow-x-auto">
      <UAlert
         v-if="loadError"
         role="alert"
         color="error"
         variant="subtle"
         icon="i-lucide-circle-alert"
         title="Unable to load fire activities"
         :description="loadError"
      >
         <template #actions>
            <UButton
               label="Retry"
               variant="outline"
               :loading="loading"
               @click="loadFireMonthly"
            />
         </template>
      </UAlert>

      <div
         v-else
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
            />
         </template>
      </div>
   </div>
</template>

<script lang="ts" setup>
type ValidValue = string | number;

const fireMonthlyStore = useFireMonthlyStore();
const { fireActivities } = storeToRefs(fireMonthlyStore);

const xAxis = computed(() =>
   [...new Set((fireActivities.value ?? []).map((activity) => activity.year))]
      .sort((a, b) => a - b),
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

const loadError = ref<string | null>(null);
const loading = ref(false);

async function loadFireMonthly() {
   loading.value = true;
   const [, error] = await tryCatch(fireMonthlyStore.loadFireMonthly());
   loadError.value = error?.message ?? null;
   loading.value = false;
}

onMounted(loadFireMonthly);

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


</script>
