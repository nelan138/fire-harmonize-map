<template>
   <ClientOnly>
      <LCircle
         v-for="fire in fireEvents"
         :key="`${fire.latitude}-${fire.longitude}-${fire.acq_date}-${fire.acq_time}`"
         :lat-lng="[fire.latitude, fire.longitude]"
         :radius="4"
         color="red"
      />
   </ClientOnly>
</template>

<script setup lang="ts">
const toast = useToast();

const fireEvents = ref<FireEvent[]>();

onMounted(async () => {
   const [queryResults, error] = await tryCatch(
      $fetch<FireEvent[]>("/api/calibrated-fire-events"),
   );

   if (queryResults) fireEvents.value = queryResults;

   if (error) {
      toast.add({
         title: "Unable to load fire events",
         description: error.message,
         color: "error",
         icon: "lucide:alert-octagon",
      });
   }
});
</script>
