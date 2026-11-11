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
import query from "~/queries/fire_events.sql?raw";

const toast = useToast();

const fireEvents = ref<FireEvent[]>();

onMounted(async () => {
   const duckDb = useDuckDB();

   const [queryResults, error] = await tryCatch(duckDb.query<FireEvent>(query));

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
