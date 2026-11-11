<template>
   <USidebar
      v-model:open="open"
      v-slot="{ state }"
      collapsible="icon"
      :ui="{
         container: 'top-(--ui-header-height) bg-default',
      }"
   >
      <UNavigationMenu
         orientation="vertical"
         :collapsed="state === 'collapsed'"
         :items="items"
         :ui="{ list: 'flex flex-col gap-4' }"
         variant="link"
      />
   </USidebar>
</template>

<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

const open = defineModel<boolean>("open", {
   required: true,
});

const items: NavigationMenuItem[] = [
   {
      label: "Interactive map",
      icon: "lucide:globe",
      to: "/map",
   },
   {
      label: "Burning activity calendar",
      icon: "lucide:calendar-days",
      to: "/activities",
   },
   {
      label: "SFAI Anomaly Diagnostics",
      icon: "lucide:flame",
      to: "/diagnostics",
   },
   {
      label: "Scientific Validation",
      icon: "lucide:shield-check",
      to: "/validation",
   },
   {
      label: "Debug",
      icon: "lucide:bug",
      to: "/debug",
   },
];
</script>

<style scoped></style>
