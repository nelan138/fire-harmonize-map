import { defineStore } from "pinia";
import { shallowRef } from "vue";
import type { FireActivity } from "../types/FireActivity";
import { tryCatch } from "../utils/tryCatch";

export const useFireMonthlyStore = defineStore("fire-monthly", () => {
   const fireActivities = shallowRef<FireActivity[] | null>(null);
   let pendingRequest: Promise<void> | undefined;

   async function loadFireMonthly() {
      if (fireActivities.value !== null) {
         return;
      }

      if (!pendingRequest) {
         pendingRequest = cacheFireActivities(
            $fetch<FireActivity[]>("/api/fire-monthly"),
         );
      }

      await pendingRequest;
   }

   async function cacheFireActivities(request: Promise<FireActivity[]>) {
      const [activities, error] = await tryCatch(request);
      pendingRequest = undefined;

      if (error) {
         throw error;
      }

      fireActivities.value = activities;
   }

   return { fireActivities, loadFireMonthly };
});
