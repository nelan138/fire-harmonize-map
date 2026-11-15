<template>
   <UAlert
      v-if="loadError"
      class="mb-4"
      role="alert"
      color="error"
      variant="subtle"
      icon="i-lucide-circle-alert"
      title="Unable to load fire events"
      :description="loadError"
   >
      <template #actions>
         <UButton
            label="Retry"
            variant="outline"
            :loading="loading"
            @click="loadFireEvents"
         />
      </template>
   </UAlert>

   <div class="h-[calc(100dvh-var(--ui-header-height)-2rem)] min-h-96">
      <WorldMap>
         <FireEvents />

         <CircleArea />
      </WorldMap>
   </div>

   <SidePanel />
</template>

<script setup lang="ts">
const fireEventsStore = useFireEventsStore();
const loadError = ref<string | null>(null);
const loading = ref(false);

async function loadFireEvents() {
   loading.value = true;
   const [, error] = await tryCatch(fireEventsStore.loadFireEvents());
   loadError.value = error?.message ?? null;
   loading.value = false;
}

onMounted(loadFireEvents);
</script>
