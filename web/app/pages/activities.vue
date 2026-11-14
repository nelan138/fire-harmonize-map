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
               v-if="region.activities.length"
               :activities="region.activities"
               :selected-activity="selectedActivity"
               @select="
                  selectedActivity = selectedActivity === $event ? null : $event
               "
            />

            <Gomennasai
               v-else
               title="No monthly data"
               description="No monthly data is available for this region."
            />
         </div>
         
         <DiagnosisCards v-if="selectedActivity" :activity="selectedActivity" />
      </template>
   </div>
</template>

<script setup lang="ts">
import type { FireActivity } from "../types/FireActivity";

const { nearbyFireEvents } = storeToRefs(useCircleAreaStore());
const fireMonthlyStore = useFireMonthlyStore();
const { fireActivities } = storeToRefs(fireMonthlyStore);
const loadError = ref<string | null>(null);
const loading = ref(false);
const selectedActivity = shallowRef<FireActivity | null>(null);

const regionIds = computed(() => [
   ...new Set(nearbyFireEvents.value.map((event) => event.region_id)),
]);
const selectedRegions = computed(() =>
   regionIds.value.map((id) => ({
      id,
      activities: (fireActivities.value ?? []).filter(
         (activity) => activity.region_id === id,
      ),
   })),
);

const monthlyState = computed(() => {
   if (!regionIds.value.length) {
      return {
         kind: "empty",
         title: "No data is found",
         description: "Please select a fire area on the map to see monthly activity for its regions.",
      };
   }

   if (loadError.value) {
      return {
         kind: "error",
         title: "Unable to load fire activities",
         description: loadError.value,
      };
   }

   if (loading.value || !fireActivities.value) {
      return {
         kind: "loading",
         title: "Loading monthly fire activity…",
         description: "Please wait while the monthly records load.",
      };
   }

   return null;
});

watch([regionIds, fireActivities], () => {
   const activity = selectedActivity.value;
   if (
      activity &&
      (!regionIds.value.includes(activity.region_id) ||
         !fireActivities.value?.includes(activity))
   ) {
      selectedActivity.value = null;
   }
});

async function loadFireMonthly() {
   loading.value = true;
   loadError.value = null;
   const [, error] = await tryCatch(fireMonthlyStore.loadFireMonthly());
   loadError.value = error?.message ?? null;
   loading.value = false;
}

onMounted(() => {
   if (regionIds.value.length) void loadFireMonthly();
});
</script>
