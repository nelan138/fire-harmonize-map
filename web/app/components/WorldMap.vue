<template>
   <LMap
      :zoom="5"
      :center="[16, 105]"
      :use-global-leaflet="false"
      :options="{ minZoom: 1, maxZoom: 8, worldCopyJump: true }"
      class="h-full w-full"
   >
      <LTileLayer :url="url" attribution="NASA GIBS" :max-zoom="8" />

      <LCircleMarker
         v-for="fire in fireEvents"
         :key="`${fire.latitude}-${fire.longitude}-${fire.acq_date}-${fire.acq_time}`"
         :lat-lng="[fire.latitude, fire.longitude]"
         :radius="4"
         color="red"
      />
   </LMap>
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

import query from "~/queries/fire_events.sql?raw";

type FireEvent = {
   latitude: number;
   longitude: number;
   frp: number;
   confidence: string | number;
   acq_date: string;
   acq_time: number;
   satellite: string;
   instrument: string;
};

const fireEvents = ref<FireEvent[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
   try {
      const duckDb = useDuckDB();
      fireEvents.value = await duckDb.query<FireEvent>(query);
   } catch (cause) {
      error.value = cause instanceof Error ? cause.message : String(cause);
   } finally {
      loading.value = false;
   }
});
</script>
