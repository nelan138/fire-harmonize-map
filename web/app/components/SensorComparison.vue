<template>
   <UCard>
      <div class="space-y-4">
         <div class="flex flex-wrap items-center justify-between gap-3">
            <H2>Sensor comparison</H2>
            <UButton
               icon="i-lucide-printer"
               label="Print / Export PDF"
               @click="printBrief"
            />
         </div>
         <p class="text-sm text-muted">Selected month · Regional totals across biomes</p>

         <table class="w-full text-left text-sm">
            <thead class="text-muted">
               <tr>
                  <th scope="col" class="py-2 pr-4 font-medium">Data source</th>
                  <th scope="col" class="py-2 text-right font-medium">Fire detections</th>
               </tr>
            </thead>
            <tbody class="divide-y divide-default border-t border-default tabular-nums">
               <tr v-for="row in comparison" :key="row.label">
                  <th scope="row" class="py-2 pr-4 font-medium">{{ row.label }}</th>
                  <td class="py-2 text-right">{{ formatCount(row.count) }}</td>
               </tr>
            </tbody>
         </table>
      </div>
   </UCard>

   <Teleport to="body">
      <article class="monthly-executive-brief hidden print:block">
         <header class="mb-5 border-b pb-3">
            <p class="text-sm font-medium">FireHarmonize</p>
            <h1 class="text-2xl font-semibold">Monthly fire brief</h1>
         </header>

         <DiagnosisCards :activity="activity" print-brief />

         <section class="mt-5 break-inside-avoid">
            <H2>Operational summary</H2>
            <p class="mt-2 text-sm">{{ operationalSummary }}</p>
         </section>

         <section class="mt-5 break-inside-avoid">
            <H2>Sensor comparison</H2>
            <p class="mt-2 text-sm">Regional fire detections across biomes</p>
            <div class="mt-3 space-y-3" role="list">
               <div v-for="row in comparison" :key="row.label" role="listitem">
                  <div class="mb-1 flex justify-between gap-3 text-sm tabular-nums">
                     <span>{{ row.label }}</span>
                     <span>{{ formatCount(row.count) }}</span>
                  </div>
                  <div aria-hidden="true" class="h-2.5 rounded-sm border border-neutral-400">
                     <div
                        class="h-full bg-neutral-700"
                        :style="{ width: `${((row.count ?? 0) / maxCount) * 100}%` }"
                     />
                  </div>
               </div>
            </div>
         </section>
      </article>
   </Teleport>
</template>

<script setup lang="ts">
import type { FireActivity } from "../types/FireActivity";

const { activity, activities } = defineProps<{
   activity: FireActivity;
   activities: FireActivity[];
}>();

const sources = [
   { field: "raw_modis_count", label: "Raw MODIS (1 km)" },
   { field: "raw_viirs_count", label: "Raw VIIRS (375 m)" },
   { field: "adj_fire_count", label: "FireHarmonize (VIIRS-equivalent)" },
] as const;

const comparison = computed(() => {
   const rows = activities.filter((row) =>
      row.region_id === activity.region_id &&
      row.year === activity.year &&
      row.month === activity.month,
   );

   return sources.map(({ label, field }) => {
      if (!rows.length) return { label, count: null };

      let count = 0;
      for (const row of rows) {
         const value = row[field];
         if (value == null || !Number.isFinite(value) || value < 0) {
            return { label, count: null };
         }
         count += value;
      }
      return { label, count };
   });
});

const maxCount = computed(() => Math.max(1, ...comparison.value.map(({ count }) => count ?? 0)));
const numberFormat = new Intl.NumberFormat("en", { maximumFractionDigits: 1 });

function formatCount(count: number | null) {
   return count === null ? "Unavailable" : numberFormat.format(count);
}

const operationalSummary = computed(() => {
   switch (activity.sfai_alert_lvl) {
      case 5:
      case 4:
         return "The selected record shows high or emergency fire activity. Verify conditions with current imagery and local reports before deciding on a response.";
      case 3:
         return "The selected record shows elevated fire activity. Review local conditions and continue monitoring.";
      case 2:
      case 1:
         return "The selected record shows normal or minimal fire activity. Continue routine monitoring.";
      default:
         return "The selected record has no alert level. Check current imagery and local reports for conditions.";
   }
});

function printBrief() {
   window.print();
}
</script>

<style>
@page fire-brief {
   size: A4 portrait;
   margin: 15mm;
}

@media print {
   body:has(> .monthly-executive-brief) > :not(.monthly-executive-brief) {
      display: none !important;
   }

   .monthly-executive-brief {
      page: fire-brief;
      color-scheme: light;
      color: #171717;
      background: white;
      print-color-adjust: exact;
      --ui-bg: white;
      --ui-border: #d4d4d4;
      --ui-text: #171717;
      --ui-text-muted: #525252;
      --ui-text-highlighted: #171717;
   }
}
</style>
