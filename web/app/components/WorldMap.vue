<template>
   <ClientOnly>
      <LMap
         :zoom="5"
         :center="[16, 105]"
         :use-global-leaflet="false"
         :options="{ minZoom: 1, maxZoom: 8, worldCopyJump: true }"
         class="h-full w-full"
      >
         <LTileLayer :url="url" attribution="NASA GIBS" :max-zoom="8" />

         <slot />
      </LMap>
   </ClientOnly>
</template>

<script setup lang="ts">
const epsg = "3857"; // flat online web maps
const layerIdentifier = "BlueMarble_ShadedRelief_Bathymetry"; // cloudless
const tileMatrixSet = "GoogleMapsCompatible_Level8"; // zoom 0 -> 8
const tileMatrix = "{z}";
const tileRow = "{y}";
const tileCol = "{x}";
const formatExt = "jpeg";

const url = `https://gibs.earthdata.nasa.gov/wmts/epsg${epsg}/best/${layerIdentifier}/default/${tileMatrixSet}/${tileMatrix}/${tileRow}/${tileCol}.${formatExt}`;
</script>
