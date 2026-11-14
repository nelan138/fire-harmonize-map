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

const { months, selectedKey = null } = defineProps<{
   months: FireMonth[];
   selectedKey?: string | null;
}>();
const emit = defineEmits<{ select: [key: string] }>();

const xAxis = computed(() =>
   [...new Set(months.map(({ year }) => year))].sort((a, b) => a - b),
);
const yAxis = [
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
];

type HeatmapGrid = {
   key: string;
   color: HeatmapGridColor;
   tooltip?: string;
   label: string;
   fireMonth?: FireMonth;
};

const gridMatrix = computed<HeatmapGrid[][]>(() => {
   const monthsByPosition = new Map(
      months.map((month) => [`${month.month}:${month.year}`, month]),
   );

   return yAxis.map((monthLabel, y) =>
      xAxis.value.map((year, x) => {
         const fireMonth = monthsByPosition.get(`${y + 1}:${year}`);
         const rows = fireMonth?.rows ?? [];
         const level = rows.reduce(
            (highest, { sfai_alert_lvl }) =>
               sfai_alert_lvl !== null && getAlertLevelColor(sfai_alert_lvl) !== "gray"
                  ? Math.max(highest, sfai_alert_lvl)
                  : highest,
            0,
         );
         const count = fireMonth?.totals.fireCount?.toLocaleString("en") ?? "Unavailable";
         const alert = level
            ? `${rows.length > 1 ? "Highest record alert" : "Alert level"}: ${level}`
            : "Alert level unavailable";

         return {
            key: `${y}:${x}`,
            fireMonth,
            label: fireMonth
               ? `${fireMonth.regionId.replaceAll("_", " ")}, ${monthLabel} ${year}`
               : `${monthLabel} ${year}: no monthly data`,
            color: level ? getAlertLevelColor(level) : fireMonth ? "neutral" : "gray",
            tooltip: fireMonth ? `Regional Fire Count: ${count}\n${alert}` : undefined,
         };
      }),
   );
});
</script>
