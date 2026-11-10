<template>
   <div class="space-y-6">
      <H1> Burning Activity Calendar </H1>

      <H2> Indochina Region </H2>

      <Heatmap :items="heatmapItems" :x-axis="years" :y-axis="months" />
   </div>
</template>

<script setup lang="ts">
import type { HeatmapItem } from "~/components/Heatmap.vue";

const results = ref<BurningData[]>([]);

const years = computed(() =>
   [...new Set(results.value.map((item) => item.year))].sort((a, b) => a - b),
);

const months = Array.from({ length: 12 }, (_, index) => index + 1);

const heatmapItems = computed<HeatmapItem[]>(() =>
   results.value.map((item) => ({
      row: item.month - 1,
      col: years.value.indexOf(item.year),
      color: getAlertLevelColor(item.sfai_alert_lvl),
      tooltip: `Fire Count: ${item.adj_fire_count}\n Alert Level: ${item.sfai_alert_lvl}`,
   })),
);

onMounted(async () => {
   results.value = await getBurningData();
});
</script>
