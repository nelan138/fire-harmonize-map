<template>
   <UCard>
      <div class="space-y-4">
         <H2>Biome breakdown</H2>

         <template v-if="biomes.length">
            <UChart
               v-if="chart"
               :definition="chart"
               :height="140"
               aria-label="Biome shares of harmonized fire detections and fire radiative power"
            >
               <template #tooltip="{ primaryPoint }">
                  <p class="font-medium">{{ primaryPoint.datum.biome }}</p>
                  <p>
                     {{ formatShare(primaryPoint.datum.share) }} ·
                     {{ formatValue(primaryPoint.datum.value) }}
                     {{ primaryPoint.datum.unit }}
                  </p>
               </template>
            </UChart>

            <p v-if="leadingBiome" class="text-sm text-muted">
               {{ leadingBiome.name }} accounted for
               {{ formatShare(leadingBiome.share) }} of harmonized
               fire detections this month.
            </p>

            <div class="overflow-x-auto">
               <table class="w-full text-left text-sm">
                  <caption class="sr-only">
                     Harmonized values and shares by biome
                  </caption>
                  <thead class="text-muted">
                     <tr>
                        <th scope="col" class="py-2 pr-4 font-medium">Biome</th>
                        <th scope="col" class="py-2 pr-4 font-medium">Fire detections</th>
                        <th scope="col" class="py-2 font-medium">FRP (MW)</th>
                     </tr>
                  </thead>
                  <tbody
                     class="divide-y divide-default border-t border-default tabular-nums"
                  >
                     <tr v-for="biome in biomes" :key="biome.id ?? 'unknown'">
                        <th scope="row" class="py-2 pr-4 font-medium">
                           <span class="inline-flex items-center gap-2">
                              <span
                                 aria-hidden="true"
                                 class="size-2.5 shrink-0 rounded-full"
                                 :style="{ backgroundColor: biome.color }"
                              />
                              {{ biome.name }}
                           </span>
                        </th>
                        <td class="whitespace-nowrap py-2 pr-4">
                           {{ formatMetric(biome.detections) }}
                        </td>
                        <td class="whitespace-nowrap py-2">
                           {{ formatMetric(biome.frp) }}
                        </td>
                     </tr>
                  </tbody>
               </table>
            </div>
         </template>
         <p v-else class="text-sm text-muted">No biome data for this month.</p>
      </div>
   </UCard>
</template>

<script setup lang="ts">
import { barX, defineChart } from "@tanstack/charts";
import { scaleBand } from "@tanstack/charts/scales/band";
import { scaleLinear } from "@tanstack/charts/scales/linear";
import type { SelectedFireMonth } from "~/utils/getSelectedFireMonth";

const { selectedMonth } = defineProps<{
   selectedMonth: SelectedFireMonth;
}>();

const biomeNames: Record<number, string> = {
   1: "Dense forests",
   2: "Savanna & grasslands",
   3: "Croplands",
   4: "Shrublands & chaparral",
};

const metrics = [
   { key: "detections", label: "Fire detections", unit: "detections" },
   { key: "frp", label: "FRP", unit: "MW" },
] as const;

type Metric = { value: number | null; share: number | null };
type Totals = Record<(typeof metrics)[number]["key"], number | null>;

const formatValue = new Intl.NumberFormat("en", { maximumFractionDigits: 1 }).format;
const formatShare = new Intl.NumberFormat("en", {
   style: "percent",
   maximumFractionDigits: 1,
}).format;

function addValue(total: number | null, value: number | null | undefined) {
   if (total === null || value == null || !Number.isFinite(value) || value < 0) return null;
   return total + value;
}

function formatMetric({ value, share }: Metric) {
   if (value === null) return "Unavailable";
   return share === null ? formatValue(value) : `${formatValue(value)} (${formatShare(share)})`;
}

const biomes = computed(() => {
   const byBiome = new Map<number | null, Totals>();
   let totalFrp: number | null = 0;

   for (const row of selectedMonth.rows) {
      const id = row.biome_id ?? null;
      const biome = byBiome.get(id) ?? { detections: 0, frp: 0 };
      biome.detections = addValue(biome.detections, row.adj_fire_count);
      biome.frp = addValue(biome.frp, row.adj_frp_mw);
      totalFrp = addValue(totalFrp, row.adj_frp_mw);
      byBiome.set(id, biome);
   }

   function metric(value: number | null, total: number | null): Metric {
      return { value, share: value !== null && total ? value / total : null };
   }

   return [...byBiome]
      .sort(([a], [b]) => (a ?? Number.MAX_SAFE_INTEGER) - (b ?? Number.MAX_SAFE_INTEGER))
      .map(([id, values]) => ({
         id,
         name: id === null ? "Unknown biome" : (biomeNames[id] ?? `Biome ${id}`),
         color: id !== null && biomeNames[id] ? `var(--ui-chart-${id})` : "var(--ui-text-muted)",
         detections: metric(values.detections, selectedMonth.totals.fireCount),
         frp: metric(values.frp, totalFrp),
      }));
});

const leadingBiome = computed(() => {
   const [first, second] = [...biomes.value].sort(
      (a, b) => (b.detections.share ?? 0) - (a.detections.share ?? 0),
   );
   if (first?.detections.share == null || first.detections.share === second?.detections.share) return null;
   return { name: first.name, share: first.detections.share };
});

const chart = computed(() => {
   const segments = metrics.flatMap(({ key, label, unit }) =>
      biomes.value.flatMap((biome) => {
         const { value, share } = biome[key];
         if (value === null || share === null || share <= 0) return [];

         return [{
            id: `${key}:${biome.id}`,
            metric: label,
            biome: biome.name,
            color: biome.color,
            value,
            share,
            unit,
         }];
      }),
   );
   if (!segments.length) return undefined;

   return defineChart({
      marks: [barX(segments, {
         key: "id",
         x: "share",
         y: "metric",
         z: "biome",
         fill: (segment) => segment.color,
         maxThickness: 24,
      })],
      scales: {
         x: {
            scale: scaleLinear().domain([0, 1]),
            axis: { ticks: { values: [0, 0.25, 0.5, 0.75, 1], format: formatShare } },
         },
         y: { scale: scaleBand },
      },
   }, { focus: "nearest-x", keyboard: true });
});
</script>
