<template>
   <UCard>
      <div class="space-y-3">
         <H2>{{ monthLabel }} fire count distribution</H2>

         <template v-if="distribution && chart">
            <p class="text-sm text-muted">
               {{ distribution.counts.length }} years with data, 2000–2024 ·
               Regional totals across biomes
            </p>
            <UChart
               :definition="chart"
               :height="280"
               :tooltip="false"
               :aria-label="`${monthLabel} historical distribution of regional fire counts`"
            />
            <div class="flex flex-wrap gap-x-5 gap-y-2 text-sm text-muted">
               <span class="inline-flex items-center gap-2">
                  <span
                     aria-hidden="true"
                     class="w-5 border-t-2 border-default"
                  />
                  Mean {{ formatCount(distribution.mean) }}
               </span>
               <span class="inline-flex items-center gap-2">
                  <span
                     aria-hidden="true"
                     class="w-5 border-t-2 border-dashed border-default"
                  />
                  ±1σ and ±2σ (σ =
                  {{ formatCount(distribution.standardDeviation) }})
               </span>
               <span
                  v-if="distribution.selectedCount !== null"
                  class="inline-flex items-center gap-2"
               >
                  <span
                     aria-hidden="true"
                     class="w-5 border-t-2 border-error"
                  />
                  {{ selectedMonth.year }} ·
                  {{ formatCount(distribution.selectedCount) }}
               </span>
            </div>
         </template>

         <p v-else class="text-sm text-muted">
            At least two years of data for this month are needed to show the
            distribution.
         </p>
      </div>
   </UCard>
</template>

<script setup lang="ts">
import { defineChart, rect, ruleX } from "@tanstack/charts";
import { scaleLinear } from "@tanstack/charts/scales/linear";
import type { SelectedFireMonth } from "~/utils/getSelectedFireMonth";

const { selectedMonth } = defineProps<{
   selectedMonth: SelectedFireMonth;
}>();

const monthLabel = computed(() =>
   new Intl.DateTimeFormat("en", {
      month: "long",
      timeZone: "UTC",
   }).format(new Date(Date.UTC(selectedMonth.year, selectedMonth.month - 1))),
);

const formatCount = new Intl.NumberFormat("en", { maximumFractionDigits: 1 })
   .format;

const distribution = computed(() => {
   const counts = selectedMonth.history.map(({ count }) => count);
   if (counts.length < 2) return null;

   const mean = counts.reduce((sum, count) => sum + count, 0) / counts.length;
   const variance =
      counts.reduce((sum, count) => sum + (count - mean) ** 2, 0) /
      counts.length;
   return {
      counts,
      mean,
      standardDeviation: Math.sqrt(variance),
      selectedCount: selectedMonth.totals.fireCount,
   };
});

const chart = computed(() => {
   if (!distribution.value) return undefined;

   const { counts, mean, standardDeviation, selectedCount } =
      distribution.value;
   const min = Math.min(...counts);
   const max = Math.max(...counts);
   const binCount = min === max ? 1 : Math.ceil(Math.sqrt(counts.length));
   const binWidth = (max - min) / binCount || 1;
   const start = min === max ? Math.max(0, min - binWidth / 2) : min;
   const bins = Array.from({ length: binCount }, (_, index) => ({
      lower: start + index * binWidth,
      upper: start + (index + 1) * binWidth,
      count: 0,
   }));

   for (const count of counts) {
      const index = Math.min(
         binCount - 1,
         Math.floor((count - start) / binWidth),
      );
      bins[index]!.count++;
   }

   const deviationLines =
      standardDeviation === 0
         ? []
         : [-2, -1, 1, 2].map(
              (multiplier) => mean + multiplier * standardDeviation,
           );

   return defineChart({
      marks: [
         rect(bins, {
            x1: "lower",
            x2: "upper",
            y1: () => 0,
            y2: "count",
            fill: "var(--ui-chart-1)",
            inset: 1,
         }),
         ruleX(deviationLines, {
            stroke: "var(--ui-text-muted)",
            strokeDasharray: "4 4",
         }),
         ruleX([mean], { stroke: "var(--ui-text-muted)", strokeWidth: 2 }),
         ruleX(selectedCount === null ? [] : [selectedCount], {
            stroke: "var(--ui-error)",
            strokeWidth: 2,
         }),
      ],
      scales: {
         x: {
            scale: scaleLinear,
            nice: true,
            axis: { label: "Harmonized fire count" },
         },
         y: {
            scale: scaleLinear,
            nice: true,
            grid: true,
            axis: { label: "Years" },
         },
      },
   });
});
</script>
