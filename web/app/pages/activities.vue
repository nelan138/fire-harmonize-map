<template>
   <div class="space-y-6">

      <p v-if="!regionIds.length" class="my-20 text-muted flex flex-col w-full justify-center items-center">
         <H2> No data is found </H2>

         <NuxtImg src='/images/gomennasai.png' class='h-20 aspect-square rounded-full' />

         <p>
            Please select a fire area on the
            <NuxtLink to="/map" class="text-primary underline">map</NuxtLink>
            to see monthly activity for its regions.
         </p>
      </p>

      <UAlert
         v-else-if="loadError"
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

      <p v-else-if="!fireActivities" class="text-muted">
         Loading monthly fire activity…
      </p>

      <template v-else >
         <H1> Burning Activity Calendar </H1>

         <div v-for="region in selectedRegions" :key="region.id" class="space-y-3">
            <H2 class="capitalize">{{ region.id.toLowerCase().replaceAll("_", " ") }}</H2>
            <Heatmap v-if="region.activities.length" :activities="region.activities" />
            <p v-else class="text-muted">No monthly data is available for this region.</p>
         </div>
      </template>
   </div>
</template>

<script setup lang="ts">
const { nearbyFireEvents } = storeToRefs(useCircleAreaStore());
const fireMonthlyStore = useFireMonthlyStore();
const { fireActivities } = storeToRefs(fireMonthlyStore);
const loadError = ref<string | null>(null);
const loading = ref(false);

const regionIds = computed(() =>
   [...new Set(nearbyFireEvents.value.map((event) => event.region_id))],
);
const selectedRegions = computed(() =>
   regionIds.value.map((id) => ({
      id,
      activities: (fireActivities.value ?? []).filter((activity) => activity.region_id === id),
   })),
);

async function loadFireMonthly() {
   loading.value = true;
   const [, error] = await tryCatch(fireMonthlyStore.loadFireMonthly());
   loadError.value = error?.message ?? null;
   loading.value = false;
}

onMounted(() => {
   if (regionIds.value.length) void loadFireMonthly();
});
</script>
