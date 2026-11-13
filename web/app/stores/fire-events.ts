import { defineStore } from "pinia";
import { shallowRef } from "vue";
import type { FireEvent } from "../types/FireEvent";
import { tryCatch } from "../utils/tryCatch";

export const useFireEventsStore = defineStore("fire-events", () => {
   const fireEvents = shallowRef<FireEvent[] | null>(null);
   let pendingRequest: Promise<void> | undefined;

   async function loadFireEvents() {
      if (fireEvents.value !== null) {
         return;
      }

      if (!pendingRequest) {
         pendingRequest = cacheFireEvents(
            $fetch<FireEvent[]>("/api/fire-events"),
         );
      }

      await pendingRequest;
   }

   async function cacheFireEvents(request: Promise<FireEvent[]>) {
      const [events, error] = await tryCatch(request);
      pendingRequest = undefined;

      if (error) {
         throw error;
      }

      fireEvents.value = events;
   }

   return { fireEvents, loadFireEvents };
});
