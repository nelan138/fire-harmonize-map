<template>
   <UTooltip
      :text="tooltip"
      :ui="{
         content: 'h-auto max-w-64 items-start py-2',
         text: 'whitespace-pre-line wrap-break-word',
      }"
   >
      <button
         type="button"
         class="flex aspect-square w-10 cursor-pointer items-center justify-center rounded-sm focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:cursor-default"
         :class="[
            getHeatmapGridColor(color),
            { 'ring-2 ring-primary ring-offset-2 ring-offset-(--ui-bg)': selected },
         ]"
         :aria-label="label"
         :aria-pressed="selected"
         :disabled="disabled"
         @click="emit('select')"
      >
         {{ value }}
      </button>
   </UTooltip>
</template>

<script setup lang="ts">
type ValidValue = string | number;

const {
   tooltip,
   color = "gray",
   selected = false,
   disabled = false,
} = defineProps<{
   color?: HeatmapGridColor;
   value?: ValidValue;
   tooltip?: string;
   label: string;
   selected?: boolean;
   disabled?: boolean;
}>();

const emit = defineEmits<{ select: [] }>();
</script>
