<template>
   <div class="overflow-x-auto">
      <div
         role="grid"
         class="grid w-fit items-center gap-2"
         :style="{
            gridTemplateColumns: `max-content repeat(${xAxis.length}, 2.5rem)`,
         }"
      >
         <div
            v-for="(label, col) in xAxis"
            :key="`x-${col}`"
            class="text-center text-xs font-medium text-muted"
         >
            {{ label }}
         </div>

         <template v-for="(rowCells, row) in cells" :key="`row-${row}`">
            <div role="rowheader" class="pr-2 text-sm font-medium text-muted">
               {{ yAxis[row] }}
            </div>

            <HeatmapGrid
               v-for="cell in rowCells"
               :key="cell.key"
               :value="cell.value"
               :color="cell.color"
               :tooltip="cell.tooltip"
            />
         </template>
      </div>
   </div>
</template>

<script lang="ts" setup>
type ValidValue = string | number;

export type HeatmapItem = {
   row: number;
   col: number;
   color: GridColor;
   val?: ValidValue;
   tooltip?: ValidValue;
   filterValue: ValidValue;
};

const { items, xAxis, yAxis } = defineProps<{
   items: HeatmapItem[];
   xAxis: ValidValue[];
   yAxis: ValidValue[];
}>();

const itemsByPosition = computed(
   () => new Map(items.map((item) => [`${item.row}:${item.col}`, item])),
);

const cells = computed(() =>
   yAxis.map((_, row) =>
      xAxis.map((_, col) => {
         const item = itemsByPosition.value.get(`${row}:${col}`);

         return {
            key: `${row}:${col}`,
            value: item?.val,
            color: item?.color ?? "gray",
            tooltip:
               item?.tooltip === undefined ? undefined : String(item.tooltip),
         };
      }),
   ),
);
</script>
