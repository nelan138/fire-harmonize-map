<template>
   <div class="space-y-4">
      <div>
         <h1 class="text-2xl font-semibold text-highlighted">DuckDB Debug</h1>
         <p class="text-sm text-muted">
            {{ loading ? "Loading records…" : `${rows.length} records` }}
         </p>
      </div>

      <UAlert
         v-if="error"
         color="error"
         icon="i-lucide-circle-alert"
         title="Could not load records"
         :description="error"
      />

      <template v-else>
         <div
            class="max-h-[70vh] overflow-auto rounded-lg border border-default"
         >
            <UTable
               :data="visibleRows"
               :columns="columns"
               :loading="loading"
               sticky
            >
               <template #empty>No records found.</template>
            </UTable>
         </div>

         <div v-if="rows.length > pageSize" class="flex justify-end">
            <UPagination
               v-model:page="page"
               :items-per-page="pageSize"
               :total="rows.length"
            />
         </div>
      </template>
   </div>
</template>

<script setup lang="ts">
import debugQuery from "~/queries/fire_events.sql?raw";

type DebugRow = Record<string, unknown>;

const toFieldLabel = (field: string): string =>
   field
      .split("_")
      .map((word) =>
         word === "id"
            ? "ID"
            : `${word.charAt(0).toUpperCase()}${word.slice(1)}`,
      )
      .join(" ");

const pageSize = 10;
const page = ref(1);
const rows = ref<DebugRow[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const columns = computed(() =>
   rows.value[0]
      ? Object.keys(rows.value[0]).map((field) => ({
           accessorKey: field,
           header: toFieldLabel(field),
        }))
      : [],
);

const visibleRows = computed(() => {
   const start = (page.value - 1) * pageSize;
   return rows.value.slice(start, start + pageSize);
});

onMounted(async () => {
   try {
      const db = useDuckDB();

      rows.value = await db.query(debugQuery);
   } catch (cause) {
      error.value = cause instanceof Error ? cause.message : String(cause);
   } finally {
      loading.value = false;
   }
});
</script>
