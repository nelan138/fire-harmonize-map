<template>
   <div class="space-y-6">
      <h1 class="text-2xl font-bold text-highlighted tracking-tight">
         Burning Activity Calendar
      </h1>

      <h2 class="text-lg font-semibold tracking-tight text-highlighted">
         Indochina Region
      </h2>
      <Heatmap :items="heatmapItems" :x-axis="years" :y-axis="months" />
   </div>
</template>

<script setup lang="ts">
import { getBurningData } from "~/utils/getBurningData";

type HeatmapItem = {
   row: number;
   col: number;
   color: GridColor;
   val?: string | number;
   tooltip?: string | number;
   filterValue: string | number;
};

const results = ref<BurningData[]>([]);

const colors: Record<number, GridColor> = {
   1: "green",
   2: "yellow",
   3: "orange",
   4: "red",
   5: "darkred",
};

const years = computed(() =>
   [...new Set(results.value.map((item) => item.year))].sort((a, b) => a - b),
);

const months = Array.from({ length: 12 }, (_, index) => index + 1);

const heatmapItems = computed<HeatmapItem[]>(() =>
   results.value.map((item) => ({
      row: item.month - 1,
      col: years.value.indexOf(item.year),
      color: colors[item.sfai_alert_lvl] ?? "gray",
      tooltip: `Fire Count: ${item.adj_fire_count}\n Alert Level: ${item.sfai_alert_lvl}`,
      filterValue: item.region_id,
   })),
);

onMounted(async () => {
   results.value = await getBurningData();
});
</script>
