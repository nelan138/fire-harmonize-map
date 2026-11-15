<template>
   <LCircle
      v-for="fire in fireEvents"
      :key="`${fire.latitude}-${fire.longitude}-${fire.acq_date}-${fire.acq_time}`"
      :lat-lng="[fire.latitude, fire.longitude]"
      :radius="4"
      color="red"
   />
</template>

<script setup lang="ts">
const fireEventsStore = useFireEventsStore();
const { fireEvents } = storeToRefs(fireEventsStore);
</script>
