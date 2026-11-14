<template>
   <section :aria-labelledby="titleId" aria-live="polite" class="space-y-4">
      <div>
         <H2 :id="titleId">Monthly diagnosis</H2>
         <p class="text-sm text-muted">
            <span class="capitalize">{{ regionName }}</span> · {{ monthLabel }}
         </p>
      </div>

      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-5 print:grid-cols-2">
         <KpiCard
            v-for="card in diagnosisCards"
            :key="card.label"
            :label="card.label"
            :value="card.value"
            :detail="card.detail"
            :color="card.color"
         />
      </div>

      <div
         v-if="!printBrief && !selectedMonth.selectedRecord"
         class="overflow-x-auto"
      >
         <table class="w-full text-left text-sm">
            <caption class="text-left">
               <H2> SFAI and alert level by source record </H2>
            </caption>
            <thead class="text-muted">
               <tr>
                  <th scope="col" class="py-2 pr-4 font-medium">
                     Record scope
                  </th>
                  <th scope="col" class="py-2 pr-4 font-medium">
                     SFAI Z-score
                  </th>
                  <th scope="col" class="py-2 font-medium">Alert level</th>
               </tr>
            </thead>
            <tbody
               class="divide-y divide-default border-t border-default tabular-nums"
            >
               <tr v-for="(record, index) in selectedMonth.rows" :key="index">
                  <th scope="row" class="py-2 pr-4 font-medium">
                     {{ recordScope(record) }}
                  </th>
                  <td class="whitespace-nowrap py-2 pr-4">
                     {{ formatZScore(record.sfai_zscore) }}
                  </td>
                  <td class="whitespace-nowrap py-2">
                     {{ formatAlertLevel(record.sfai_alert_lvl) }}
                  </td>
               </tr>
            </tbody>
         </table>
      </div>
   </section>
</template>

<script setup lang="ts">
import type { FireMonthly } from "#shared/types/FireMonthly";
import type { HeatmapGridColor } from "~/utils/getHeatmapGridColor";
import type { SelectedFireMonth } from "~/utils/getSelectedFireMonth";

const { selectedMonth, printBrief = false } = defineProps<{
   selectedMonth: SelectedFireMonth;
   printBrief?: boolean;
}>();
const titleId = useId();

const regionName = computed(() =>
   selectedMonth.regionId.toLowerCase().replaceAll("_", " "),
);
const monthLabel = computed(() => {
   return new Intl.DateTimeFormat("en", {
      month: "long",
      year: "numeric",
      timeZone: "UTC",
   }).format(new Date(Date.UTC(selectedMonth.year, selectedMonth.month - 1)));
});

const alertLabels: Record<number, string> = {
   1: "Minimal",
   2: "Normal",
   3: "Elevated",
   4: "High",
   5: "Emergency",
};
const countFormat = new Intl.NumberFormat("en", { maximumFractionDigits: 1 });
const changeFormat = new Intl.NumberFormat("en", {
   signDisplay: "exceptZero",
   minimumFractionDigits: 1,
   maximumFractionDigits: 1,
});

function recordScope(record: FireMonthly) {
   const biome =
      record.biome_id == null
         ? "Biome unspecified"
         : `Biome ${record.biome_id}`;
   return record.h3_index && record.h3_index !== "N/A"
      ? `${biome} · H3 ${record.h3_index}`
      : biome;
}

function formatZScore(score: number | null) {
   return score === null
      ? "Unavailable"
      : `${score > 0 ? "+" : ""}${score.toFixed(2)}σ`;
}

function formatAlertLevel(level: number | null) {
   const label = level === null ? undefined : alertLabels[level];
   return label ? `Level ${level} · ${label}` : "Unavailable";
}

const diagnosisCards = computed(() => {
   const { totals, historicalChange, selectedRecord } = selectedMonth;
   const cards: {
      label: string;
      value: string;
      detail: string;
      color?: HeatmapGridColor;
   }[] = [
      {
         label: "Fire count",
         value:
            totals.fireCount === null
               ? "Unavailable"
               : countFormat.format(totals.fireCount),
         detail: "Regional VIIRS-equivalent detections",
      },
      {
         label: "Historical change",
         value:
            historicalChange === null
               ? "Unavailable"
               : `${changeFormat.format(historicalChange)}%`,
         detail: "vs. same-month regional totals (2000–2024)",
      },
   ];

   if (selectedRecord) {
      const scope = recordScope(selectedRecord);
      const level = selectedRecord.sfai_alert_lvl;
      cards.push(
         {
            label: "SFAI Z-score",
            value: formatZScore(selectedRecord.sfai_zscore),
            detail: scope,
         },
         {
            label: "Alert level",
            value: formatAlertLevel(level),
            detail: scope,
            color: level !== null ? getAlertLevelColor(level) : undefined,
         },
      );
   } else if (printBrief) {
      const scores = selectedMonth.rows.flatMap(({ sfai_zscore }) =>
         sfai_zscore === null ? [] : [sfai_zscore],
      );
      const lowest = scores.length ? Math.min(...scores) : null;
      const highest = scores.length ? Math.max(...scores) : null;
      cards.push({
         label: "SFAI Z-score range",
         value:
            lowest === highest
               ? formatZScore(lowest)
               : `${formatZScore(lowest)} to ${formatZScore(highest)}`,
         detail: `Across ${scores.length} of ${selectedMonth.rows.length} source records`,
      });
   }

   if (!printBrief) {
      cards.push({
         label: "Oceanic Niño Index",
         value: "+1.2 °C",
         detail: "El Niño (placeholder)",
      });
   }

   return cards;
});
</script>
