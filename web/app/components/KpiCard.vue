<template>
   <UCard>
      <dl class="space-y-2">
         <dt class="text-sm text-muted">{{ label }}</dt>
         <dd class="text-2xl font-semibold text-highlighted tabular-nums">
            <span
               v-if="color"
               class="inline-flex rounded-md px-3 py-1 text-base"
               :class="getHeatmapGridColor(color)"
            >
               {{ value }}
            </span>
            <template v-else>{{ value }}</template>
         </dd>
      </dl>
      <p class="mt-2 text-xs text-muted">{{ detail }}</p>
   </UCard>
</template>

<script setup lang="ts">
defineProps<{
   label: string;
   value: string;
   detail: string;
   color?: HeatmapGridColor;
}>();
</script>
