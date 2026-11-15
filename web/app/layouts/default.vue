<template>
   <div>
      <UHeader :ui="{ container: 'max-w-none px-0 sm:px-0 lg:px-4', toggle: 'me-0' }">
         <template #left>
            <div class="flex gap-8">
               <UButton
                  icon="i-lucide-panel-left-open"
                  aria-label="Toggle sidebar"
                  :aria-expanded="open"
                  @click="open = !open"
               />

               <span class="text-xl font-bold tracking-tight">
                  Fire<span class="text-primary">Harmonize</span>
               </span>
            </div>
         </template>

         <template #right>
            <UColorModeButton />
         </template>
      </UHeader>

      <UMain class="flex">
         <Sidebar v-model:open="open" />

         <div class="min-w-0 flex-1 p-4">
            <slot />
         </div>
      </UMain>
   </div>
</template>

<script setup lang="ts">
const open = ref(false);
</script>
