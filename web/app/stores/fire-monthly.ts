import { defineStore } from "pinia";
import { shallowRef } from "vue";
import type { FireMonthly } from "#shared/types/FireMonthly";
import { tryCatch } from "../utils/tryCatch";

type MonthlyRequest =
   | { status: "idle" | "pending" }
   | { status: "error"; message: string }
   | { status: "success"; rows: FireMonthly[] };

export function fireMonthlyRequestKey(regions: readonly string[] = []) {
   return JSON.stringify([...new Set(regions)].sort());
}

export const useFireMonthlyStore = defineStore("fire-monthly", () => {
   const requests = shallowRef<Partial<Record<string, MonthlyRequest>>>({});
   const pendingRequests = new Map<string, Promise<void>>();

   function setRequest(key: string, request: MonthlyRequest) {
      requests.value = { ...requests.value, [key]: request };
   }

   function getRequest(key: string): MonthlyRequest {
      return requests.value[key] ?? { status: "idle" };
   }

   async function fetchMonthly(key: string, regions: readonly string[]) {
      const [rows, error] = await tryCatch($fetch<FireMonthly[]>("/api/fire-monthly", {
         query: regions.length ? { regions } : undefined,
      }));

      setRequest(key, error ? { status: "error", message: error.message } : { status: "success", rows });
   }

   function loadFireMonthly(regions: readonly string[] = []) {
      const key = fireMonthlyRequestKey(regions);
      if (getRequest(key).status === "success") return;

      const pending = pendingRequests.get(key);
      if (pending) return pending;

      const request = fetchMonthly(key, regions).finally(() => pendingRequests.delete(key));
      pendingRequests.set(key, request);
      setRequest(key, { status: "pending" });
      return request;
   }

   return { requests, getRequest, loadFireMonthly };
});
