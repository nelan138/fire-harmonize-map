<template>
   <LCircle
      v-if="circleCenter"
      :lat-lng="circleCenter"
      :radius="circleRadiusMeters"
      color="blue"
      :fill-opacity="0.5"
      :interactive="false"
   />
</template>

<script setup lang="ts">
import { circleRadiusMeters } from "../stores/circle-area";

const { circleCenter } = storeToRefs(useCircleAreaStore());
</script>
