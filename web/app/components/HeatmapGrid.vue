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
         :class="colorClasses[color]"
      >
         {{ value }}
      </div>
   </UTooltip>
</template>

<script setup lang="ts">
type ValidValue = string | number;

const { tooltip, color = "gray" } = defineProps<{
   color?: GridColor;
   value?: ValidValue;
   tooltip?: string;
}>();

const colorClasses: Record<GridColor, string> = {
   gray: "bg-muted",
   green: "bg-success/40",
   yellow: "bg-warning/35",
   orange: "bg-warning",
   red: "bg-error/65",
   darkred: "bg-error",
};
</script>
