import type { LatLng } from "leaflet";
import { defineStore } from "pinia";
import { computed, shallowRef } from "vue";
import { useFireEventsStore } from "./fire-events";

export const circleRadiusMeters = 20_000;

export const useCircleAreaStore = defineStore("circle-area", () => {
   const clickedLocation = shallowRef<LatLng | null>(null);
   const fireEventsStore = useFireEventsStore();

   const nearbyFireEvents = computed(() => {
      const location = clickedLocation.value;
      const events = fireEventsStore.fireEvents;
      if (!location || !events) return [];

      return events
         .map((event) => ({
            event,
            distance: location.distanceTo([event.latitude, event.longitude]),
         }))
         .filter(({ distance }) => distance <= circleRadiusMeters)
         .sort((a, b) => a.distance - b.distance)
         .map(({ event }) => event);
   });

   const circleCenter = computed(() =>
      nearbyFireEvents.value.length ? clickedLocation.value : null,
   );

   return { clickedLocation, circleCenter, nearbyFireEvents };
});
