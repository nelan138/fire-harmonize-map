<template>
   <div
      class="my-20 text-muted flex flex-col w-full justify-center items-center"
   >
      <H2>{{ title }}</H2>

      <NuxtImg
         src="/images/gomennasai.png"
         alt=""
         class="h-20 aspect-square rounded-full"
      />

      <p>
         <slot name="description">{{ description }}</slot>
      </p>

      <slot name="actions" />
   </div>
</template>

<script setup lang="ts">
defineProps<{
   title: string;
   description: string;
}>();
</script>
