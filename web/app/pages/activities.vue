<template>
   <div class="space-y-6">
      <Gomennasai
         v-if="monthlyState"
         :title="monthlyState.title"
         :description="monthlyState.description"
         :role="monthlyState.kind === 'error' ? 'alert' : 'status'"
         :aria-busy="monthlyState.kind === 'loading'"
      >
         <template v-if="monthlyState.kind === 'empty'" #description>
            Please select a fire area on the
            <NuxtLink to="/map" class="text-primary underline">map</NuxtLink>
            to see monthly activity for its regions.
         </template>
         
         <template v-if="monthlyState.kind === 'error'" #actions>
            <UButton
               label="Retry"
               variant="outline"
               class="mt-4"
               @click="loadFireMonthly"
            />
         </template>
      </Gomennasai>

      <template v-else>
         <H1> Burning Activity Calendar </H1>

         <p class="text-sm text-muted">
            Select a colored cell to view its monthly diagnosis.
         </p>

         <div
            v-for="region in selectedRegions"
            :key="region.id"
            class="space-y-3"
         >
            <H2 class="capitalize">{{
               region.id.toLowerCase().replaceAll("_", " ")
            }}</H2>

            <Heatmap
               v-if="region.months.length"
               :months="region.months"
               :selected-key="selectedKey"
               @select="selectedKey = selectedKey === $event ? null : $event"
            />

            <Gomennasai
               v-else
               title="No monthly data"
               description="No monthly data is available for this region."
            />
         </div>
         
         <template v-if="selectedMonth">
            <DiagnosisCards :selected-month="selectedMonth" />
            <FireHistoryHistogram :selected-month="selectedMonth" />
            <BiomeBreakdown :selected-month="selectedMonth" />
            <SensorComparison :selected-month="selectedMonth" />
         </template>
      </template>
   </div>
</template>

<script setup lang="ts">
import { fireMonthlyRequestKey } from "../stores/fire-monthly";
import { getSelectedFireMonth, groupFireMonths } from "../utils/getSelectedFireMonth";

const { nearbyFireEvents } = storeToRefs(useCircleAreaStore());
const fireMonthlyStore = useFireMonthlyStore();
const selectedKey = ref<string | null>(null);

const regionIds = computed(() => [
   ...new Set(nearbyFireEvents.value.map((event) => event.region_id)),
]);

const requestKey = computed(() => fireMonthlyRequestKey(regionIds.value));
const request = computed(() => fireMonthlyStore.getRequest(requestKey.value));
const months = computed(() =>
   request.value.status === "success" ? groupFireMonths(request.value.rows) : [],
);

const selectedRegions = computed(() =>
   regionIds.value.map((id) => ({
      id,
      months: months.value.filter((month) => month.regionId === id),
   })),
);

const selectedMonth = computed(() => {
   const selection = months.value.find(({ key }) => key === selectedKey.value);
   return selection ? getSelectedFireMonth(selection, months.value) : null;
});

const monthlyState = computed(() => {
   if (!regionIds.value.length) {
      return {
         kind: "empty",
         title: "No data is found",
         description: "Please select a fire area on the map to see monthly activity for its regions.",
      };
   }

   if (request.value.status === "error") {
      return {
         kind: "error",
         title: "Unable to load fire activities",
         description: request.value.message,
      };
   }

   if (request.value.status !== "success") {
      return {
         kind: "loading",
         title: "Loading monthly fire activity…",
         description: "Please wait while the monthly records load.",
      };
   }

   return null;
});

watch(request, (result) => {
   if (result.status === "success" && !selectedMonth.value) selectedKey.value = null;
});

function loadFireMonthly() {
   if (regionIds.value.length) void fireMonthlyStore.loadFireMonthly(regionIds.value);
   else selectedKey.value = null;
}

watch(requestKey, loadFireMonthly);
onMounted(loadFireMonthly);
</script>
