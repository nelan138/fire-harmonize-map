<template>
   <UDrawer
      v-model:open="drawerOpen"
      direction="right"
      title="Fire Area Details"
      :modal="false"
      :overlay="false"
      :handle="false"
      close
      class="z-1100 w-80"
   >
      <template #description>
         {{ nearbyFireEvents.length }} fire
         {{ nearbyFireEvents.length === 1 ? "event" : "events" }} within
         {{ circleRadiusMeters / 1000 }} km
      </template>

      <template #body>
         <div class="space-y-3">
            <UAccordion v-model="expandedEvent" :items="eventItems" collapsible>
               <template #default="{ item }">
                  <span class="flex min-w-0 flex-col gap-1 text-left">
                     <span class="text-highlighted">{{ item.label }}</span>
                     <span class="font-normal text-muted">
                        {{ item.latitude.toFixed(4) }},
                        {{ item.longitude.toFixed(4) }}
                     </span>
                  </span>
               </template>

               <template #body="{ item }">
                  <dl class="grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 text-sm">
                     <dt class="text-muted">Satellite</dt>
                     <dd>{{ item.satellite ?? "Unknown" }}</dd>
                     <dt class="text-muted">Instrument</dt>
                     <dd>{{ item.instrument ?? "Unknown" }}</dd>
                     <dt class="text-muted">Fire radiative power</dt>
                     <dd>
                        {{ item.frp == null ? "Unknown" : `${item.frp} MW` }}
                     </dd>
                     <dt class="text-muted">Confidence</dt>
                     <dd>{{ item.confidence ?? "Unknown" }}</dd>
                  </dl>
               </template>
            </UAccordion>

            <UButton
               v-if="visibleCount < nearbyFireEvents.length"
               label="See more"
               variant="outline"
               block
               @click="visibleCount += pageSize"
            />
         </div>
      </template>
   </UDrawer>
</template>

<script setup lang="ts">
import { circleRadiusMeters } from "../stores/circle-area";

const { circleCenter, nearbyFireEvents } = storeToRefs(useCircleAreaStore());
const drawerOpen = ref(false);
const pageSize = 5;
const visibleCount = ref(pageSize);
const expandedEvent = ref("");
const eventItems = computed(() =>
   nearbyFireEvents.value.slice(0, visibleCount.value).map((event) => ({
      ...event,
      label: `${event.acq_date ?? "Unknown date"} · ${formatTime(event.acq_time)}`,
   })),
);

watch(circleCenter, (center) => {
   drawerOpen.value = Boolean(center);
   visibleCount.value = pageSize;
   expandedEvent.value = "";
});

function formatTime(time: number | null) {
   if (time == null) return "Unknown time";

   const hhmm = String(time).padStart(4, "0");
   return `${hhmm.slice(0, 2)}:${hhmm.slice(2)} UTC`;
}
</script>
