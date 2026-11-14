<template>
   <section aria-labelledby="monthly-diagnosis-title" aria-live="polite" class="space-y-4">
      <div>
         <H2 id="monthly-diagnosis-title">Monthly diagnosis</H2>
         <p class="text-sm text-muted">
            <span class="capitalize">{{ regionName }}</span> · {{ monthLabel }}
         </p>
      </div>

      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
         <DiagnosisCard
            v-for="card in diagnosisCards"
            :key="card.label"
            :label="card.label"
            :value="card.value"
            :detail="card.detail"
            :color="card.color"
         />
      </div>
   </section>
</template>

<script setup lang="ts">
import type { FireActivity } from "../types/FireActivity";

const { activity } = defineProps<{ activity: FireActivity }>();

const regionName = computed(() =>
   activity.region_id.toLowerCase().replaceAll("_", " "),
);
const monthLabel = computed(() => {
   return new Intl.DateTimeFormat("en", {
      month: "long",
      year: "numeric",
      timeZone: "UTC",
   }).format(new Date(Date.UTC(activity.year, activity.month - 1)));
});
const alertLabels: Record<number, string> = {
   1: "Minimal",
   2: "Normal",
   3: "Elevated",
   4: "High",
   5: "Emergency",
};
const diagnosisCards = computed(() => {
   const alertLabel = alertLabels[activity.sfai_alert_lvl];
   const zScore = activity.sfai_zscore != null && Number.isFinite(activity.sfai_zscore)
      ? `${activity.sfai_zscore > 0 ? "+" : ""}${activity.sfai_zscore.toFixed(2)}σ`
      : "Unavailable";

   return [
      {
         label: "Fire count",
         value: activity.adj_fire_count.toLocaleString("en"),
         detail: "VIIRS-equivalent detections",
      },
      {
         label: "SFAI Z-score",
         value: zScore,
         detail: "Deviation from the seasonal baseline",
      },
      {
         label: "Historical change",
         value: "Unavailable",
         detail: "% above or below the historical monthly average",
      },
      {
         label: "Alert level",
         value: alertLabel
            ? `Level ${activity.sfai_alert_lvl} · ${alertLabel}`
            : "Unavailable",
         detail: "From level 1 (Minimal) to level 5 (Emergency)",
         color: alertLabel ? getAlertLevelColor(activity.sfai_alert_lvl) : undefined,
      },
   ];
});
</script>
