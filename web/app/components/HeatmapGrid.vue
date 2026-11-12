<template>
   <UTooltip
      :text="tooltip"
      :ui="{
         content: 'h-auto max-w-64 items-start py-2',
         text: 'whitespace-pre-line wrap-break-word',
      }"
   >
      <div
         class="flex aspect-square w-10 items-center justify-center rounded-sm"
         :class="getHeatmapGridColor(color)"
      >
         {{ value }}
      </div>
   </UTooltip>
</template>

<script setup lang="ts">
type ValidValue = string | number;

const { tooltip, color = "gray" } = defineProps<{
   color?: HeatmapGridColor;
   value?: ValidValue;
   tooltip?: string;
}>();
</script>
