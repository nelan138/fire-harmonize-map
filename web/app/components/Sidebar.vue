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
   },
   {
      label: "Placeholder",
      icon: "lucide:map",
   },
   {
      label: "Placeholder",
      icon: "lucide:flame",
   },
   {
      label: "Placeholder",
      icon: "lucide:shield-question-mark",
   },
];
</script>

<style scoped></style>
