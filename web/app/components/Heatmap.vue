<template>
   <div class="overflow-x-auto p-1">
      <div
         class="grid w-fit items-center gap-2"
         :style="{
            gridTemplateColumns: `max-content repeat(${xAxis.length}, 2.5rem)`,
         }"
      >
         <div aria-hidden="true" />

         <div
            v-for="(label, x) in xAxis"
            :key="`x-${x}`"
            class="text-center text-xs font-medium text-muted"
         >
            {{ label }}
         </div>

         <template v-for="(grids, y) in gridMatrix" :key="`y-${y}`">
            <div class="pr-2 text-left text-sm font-medium text-muted">
               {{ yAxis[y] }}
            </div>

            <HeatmapGrid
               v-for="grid in grids"
               :key="grid.key"
               :value="grid.value"
               :color="grid.color"
               :tooltip="grid.tooltip"
               :label="grid.label"
               :selected="!!grid.fireMonth && grid.fireMonth.key === selectedKey"
               :disabled="!grid.fireMonth"
               @select="grid.fireMonth && emit('select', grid.fireMonth.key)"
            />
         </template>
      </div>
   </div>
</template>

<script lang="ts" setup>
import type { FireMonth } from "../utils/getSelectedFireMonth";

type ValidValue = string | number;

const { months, selectedKey = null } = defineProps<{
   months: FireMonth[];
   selectedKey?: string | null;
}>();
const emit = defineEmits<{ select: [key: string] }>();

const xAxis = computed(() =>
   [...new Set(months.map(({ year }) => year))].sort((a, b) => a - b),
);
const yAxis = shallowRef<ValidValue[]>([
   "January",
   "February",
   "March",
   "April",
   "May",
   "June",
   "July",
   "August",
   "September",
   "October",
   "November",
   "December",
]);

type HeatmapGrid = {
   key: string;
   value?: ValidValue;
   color: HeatmapGridColor;
   tooltip?: string;
   label: string;
   fireMonth?: FireMonth;
};

const gridMatrix = computed<HeatmapGrid[][]>(() => {
   const monthsByPosition = new Map(
      months.map((month) => [`${month.month}:${month.year}`, month]),
   );

   return yAxis.value.map((_, y) =>
      xAxis.value.map((year, x) => {
         const fireMonth = monthsByPosition.get(`${y + 1}:${year}`);
         const level = fireMonth?.selectedRecord?.sfai_alert_lvl;
         const count = fireMonth?.totals.fireCount?.toLocaleString("en") ?? "Unavailable";
         const alert = level == null ? "See diagnosis for record-level alerts" : `Alert Level: ${level}`;

         return {
            key: `${y}:${x}`,
            fireMonth,
            label: fireMonth
               ? `${fireMonth.regionId.replaceAll("_", " ")}, ${yAxis.value[y]} ${year}`
               : `${yAxis.value[y]} ${year}: no monthly data`,
            color: level != null ? getAlertLevelColor(level) : fireMonth ? "neutral" : "gray",
            tooltip: fireMonth ? `Regional Fire Count: ${count}\n${alert}` : undefined,
         };
      }),
   );
});
</script>
