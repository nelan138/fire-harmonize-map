<template>
   <ClientOnly>
      <LMap
         :zoom="5"
         :center="[16, 105]"
         :use-global-leaflet="false"
         :options="{ minZoom: 1, maxZoom: 8, worldCopyJump: true }"
         class="h-full w-full"
         @ready="map = $event"
      >
         <div
            class="w-full flex flex-col items-center absolute z-1000 p-4"
            @click.stop
            @dblclick.stop
            @pointerdown.stop
            @keydown.stop
         >
            <UInput
               v-model="coordinates"
               icon="i-lucide-search"
               size="md"
               variant="outline"
               placeholder="latitude, longitude"
               class="w-[30%]"
               :color="coordinateError ? 'error' : 'neutral'"
               :aria-invalid="!!coordinateError"
               @keydown.enter.prevent="goToCoordinates"
               @update:model-value="coordinateError = ''"
            />
            <p
               v-if="coordinateError"
               role="alert"
               class="mt-1 rounded bg-white px-2 text-sm text-red-600"
            >
               {{ coordinateError }}
            </p>
         </div>

         <LTileLayer :url="url" attribution="NASA GIBS" :max-zoom="8" />

         <slot />
      </LMap>
   </ClientOnly>
</template>

<script setup lang="ts">
import type { Map } from "leaflet";

const map = shallowRef<Map>();
const coordinates = ref("");
const coordinateError = ref("");

function goToCoordinates() {
   const parts = coordinates.value.split(",").map((part) => part.trim());
   const lat = Number(parts[0]);
   const lng = Number(parts[1]);

   if (
      parts.length !== 2 ||
      parts.some((part) => part === "") ||
      !Number.isFinite(lat) ||
      !Number.isFinite(lng) ||
      Math.abs(lat) > 90 ||
      Math.abs(lng) > 180
   ) {
      coordinateError.value =
         "Enter latitude (-90 to 90), longitude (-180 to 180).";
      return;
   }

   coordinateError.value = "";
   map.value?.flyTo([lat, lng], 5);
}

const epsg = "3857"; // flat online web maps
const layerIdentifier = "BlueMarble_ShadedRelief_Bathymetry"; // cloudless
const tileMatrixSet = "GoogleMapsCompatible_Level8"; // zoom 0 -> 8
const tileMatrix = "{z}";
const tileRow = "{y}";
const tileCol = "{x}";
const formatExt = "jpeg";

const url = `https://gibs.earthdata.nasa.gov/wmts/epsg${epsg}/best/${layerIdentifier}/default/${tileMatrixSet}/${tileMatrix}/${tileRow}/${tileCol}.${formatExt}`;
</script>
