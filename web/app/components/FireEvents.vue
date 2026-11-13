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
const fireEventsStore = useFireEventsStore();
const { fireEvents } = storeToRefs(fireEventsStore);

onMounted(async () => {
   const [, error] = await tryCatch(fireEventsStore.loadFireEvents());

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
