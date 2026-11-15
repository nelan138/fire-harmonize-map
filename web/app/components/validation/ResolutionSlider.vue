<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-3 flex items-center gap-3">
      <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">1</span>
      <div>
        <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
          {{ expertMode ? 'Optical Physics & The 2012 Satellite Sensor Fracture' : 'The Optical Illusion: Why Satellites Suddenly Saw 4x More Fires in 2012' }}
        </h2>
        <p class="text-xs sm:text-sm text-slate-400">
          {{ expertMode ? 'Pixel dilation geometry, sub-pixel thermal sensitivity, and empirical overpass resolution disparities' : 'How upgrading satellite cameras created the illusion of a sudden global wildfire explosion' }}
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      <!-- Left Column: Explanation (Dynamic by Track) -->
      <div class="lg:col-span-6 space-y-4 text-slate-300 text-sm leading-relaxed">
        <!-- GENERAL TRACK EXPLANATION -->
        <div v-if="!expertMode" class="space-y-4">
          <p>
            In late 2011, NASA upgraded its main fire-tracking satellites from an older camera (<strong class="text-white">MODIS</strong>) to a sharp modern camera (<strong class="text-white">VIIRS</strong>). This technology jump immediately created an optical illusion:
          </p>

          <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2.5">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-slate-400 font-medium">Old Satellite (MODIS, 2000–2011):</span>
              <span class="text-amber-300 font-bold font-mono">1 km &times; 1 km box (1.00 km&sup2;)</span>
            </div>
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-slate-400 font-medium">New Satellite (VIIRS, 2012–Present):</span>
              <span class="text-teal-300 font-bold font-mono">375 m &times; 375 m box (0.14 km&sup2;)</span>
            </div>
            <div class="flex items-center justify-between text-rose-400 font-semibold pt-1">
              <span>Magnification Difference:</span>
              <span>MODIS pixel is 7 times larger!</span>
            </div>
          </div>

          <!-- Highlight Analogy Card -->
          <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
            <div class="font-bold text-emerald-300 flex items-center gap-2">
              <UIcon name="i-lucide-lightbulb" class="w-4 h-4 text-amber-400 shrink-0" />
              <span>The 1 Megapixel vs 8 Megapixel Camera Analogy</span>
            </div>
            <p class="text-slate-300">
              Imagine taking a photo of a forested hill with a grainy <strong>1 Megapixel flip phone (MODIS)</strong>. Small campfires or farm burns are invisible—they blend into the cold green background.
            </p>
            <p class="text-slate-300">
              Then you switch to a modern <strong>8 Megapixel smartphone (VIIRS)</strong>. Suddenly, you can clearly see dozens of tiny smoke plumes and campfires under the trees.
            </p>
            <p class="text-slate-300 font-medium">
              The fire counter jumps by 300% to 500%, but <em class="text-amber-200">the forest did not burn any more than before</em>—<em class="text-emerald-200">your camera lens is simply 7 times sharper</em>!
            </p>
          </div>

          <p class="text-xs text-slate-400">
            <strong>Why This Matters:</strong> Without FireHarmonize, climate charts show an artificial 2012 jump, misleading policy makers into thinking global warming caused fires to quadruple in a single year.
          </p>
        </div>

        <!-- SCIENTIFIC DEEP DIVE EXPLANATION -->
        <div v-else class="space-y-4">
          <p>
            The transition from EOS MODIS (Terra/Aqua) to S-NPP/JPSS VIIRS represents a major architectural shift in spaceborne radiometric sounding, as characterized by <a href="https://doi.org/10.1016/j.rse.2013.12.008" target="_blank" class="text-emerald-400 hover:underline font-medium">Schroeder et al. (2014)</a> and <a href="https://doi.org/10.1016/j.rse.2016.02.054" target="_blank" class="text-emerald-400 hover:underline font-medium">Giglio et al. (2016)</a>:
          </p>

          <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 font-mono text-xs space-y-2">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-slate-400">MODIS Ground Sample Distance:</span>
              <span class="text-amber-300 font-bold">1.0 km nadir &rarr; 9.7 km&sup2; at 55&deg; scan edge</span>
            </div>
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-slate-400">VIIRS Ground Sample Distance:</span>
              <span class="text-teal-300 font-bold">375 m nadir &rarr; 0.60 km&sup2; via sample aggregation</span>
            </div>
            <div class="flex items-center justify-between text-rose-400 font-bold pt-1">
              <span>Pixel Area Expansion Factor:</span>
              <span>A<sub>MODIS</sub> / A<sub>VIIRS</sub> &approx; 7.11&times; (Nadir)</span>
            </div>
          </div>

          <div class="p-3.5 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-2">
            <div class="font-bold text-emerald-400 flex items-center gap-1.5 font-mono">
              <UIcon name="i-lucide-binary" class="w-4 h-4 shrink-0" />
              <span>Sub-Pixel Thermal Physics &amp; I-Band Radiance</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              VIIRS utilizes high-resolution imagery band <strong class="text-white">I4 (3.55–3.93 &mu;m)</strong> with a 375 m footprint. Because pixel background area is 7.11&times; smaller, small sub-pixel flaming fronts (&lt; 100 m&sup2;) generate sufficient brightness temperature elevations (&Delta;T<sub>41</sub> &gt; 10 K) above background noise without being diluted by surrounding unburned forest canopy.
            </p>
            <p class="text-slate-300 leading-relaxed font-mono text-[11px] text-slate-400">
              Bowtie Distortion: &Delta;x<sub>along-scan</sub>(&theta;) = h &middot; sec&sup2;(&theta;) &middot; &Delta;&beta; &mdash; VIIRS constrains scan-angle dilation via 3:1 sample aggregation, whereas MODIS expands up to 10-fold across track.
            </p>
          </div>
        </div>
      </div>

      <!-- Right Column: Interactive Resolution Slider -->
      <div class="lg:col-span-6 space-y-3">
        <div class="flex items-center justify-between text-xs font-mono">
          <span class="flex items-center gap-1.5 text-amber-400 font-semibold">
            <UIcon name="i-lucide-eye" class="w-4 h-4" />
            <span>&larr; Drag Left: MODIS Aqua 1 km</span>
          </span>
          <span class="flex items-center gap-1.5 text-teal-400 font-semibold">
            <span>VIIRS SNPP 375 m &rarr;</span>
            <UIcon name="i-lucide-flame" class="w-4 h-4" />
          </span>
        </div>

        <div
          ref="sliderContainer"
          class="relative w-full h-[360px] sm:h-[400px] rounded-xl overflow-hidden border border-slate-700 shadow-2xl select-none cursor-ew-resize group"
          @mousedown="startDragging"
          @touchstart="startDragging"
        >
          <!-- Background Image: VIIRS (Right Side) -->
          <img
            src="/imagery/indochina_VIIRS_SNPP_2023-03-15.jpg"
            alt="VIIRS 375m Satellite View"
            class="absolute inset-0 w-full h-full object-cover pointer-events-none"
          />

          <!-- Foreground Image: MODIS (Left Side, Clipped) -->
          <div
            class="absolute inset-0 overflow-hidden pointer-events-none border-r-2 border-emerald-400 shadow-[2px_0_12px_rgba(0,0,0,0.8)]"
            :style="{ width: `${sliderPos}%` }"
          >
            <img
              src="/imagery/indochina_MODIS_Aqua_2023-03-15.jpg"
              alt="MODIS 1km Satellite View"
              class="absolute top-0 left-0 h-full max-w-none object-cover"
              :style="{ width: containerWidth ? `${containerWidth}px` : '100%' }"
            />
          </div>

          <!-- Divider Handle -->
          <div
            class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-10 h-10 rounded-full bg-emerald-400 text-slate-950 flex items-center justify-center shadow-[0_0_20px_rgba(52,211,153,0.8)] z-20 pointer-events-none group-hover:scale-110 transition-transform"
            :style="{ left: `${sliderPos}%` }"
          >
            <UIcon name="i-lucide-move-horizontal" class="w-5 h-5 font-bold" />
          </div>

          <!-- Overlay Badge Labels -->
          <div class="absolute bottom-3 left-3 z-30 px-2.5 py-1 rounded-md bg-slate-950/80 backdrop-blur-sm border border-slate-700 text-[11px] font-mono text-amber-300">
            MODIS Aqua 1 km (2023-03-15)
          </div>
          <div class="absolute bottom-3 right-3 z-30 px-2.5 py-1 rounded-md bg-slate-950/80 backdrop-blur-sm border border-slate-700 text-[11px] font-mono text-teal-300">
            VIIRS S-NPP 375 m (2023-03-15)
          </div>
        </div>

        <p class="text-xs text-slate-400 text-center italic">
          {{ expertMode ? 'Coincident afternoon overpass (March 15, 2023, Central Highlands Vietnam). Note sub-pixel fire clustering resolved only in VIIRS.' : 'Real satellite observation over Vietnam on March 15, 2023. Drag the slider to see how blurry 1 km squares resolve into sharp 375 m pinpoints.' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  expertMode?: boolean;
}>();

const sliderContainer = ref<HTMLElement | null>(null);
const sliderPos = ref(50);
const containerWidth = ref(0);
let isDragging = false;

const updateWidth = () => {
  if (sliderContainer.value) {
    containerWidth.value = sliderContainer.value.offsetWidth;
  }
};

const handleMove = (clientX: number) => {
  if (!sliderContainer.value) return;
  const rect = sliderContainer.value.getBoundingClientRect();
  const offsetX = clientX - rect.left;
  const percentage = Math.max(5, Math.min(95, (offsetX / rect.width) * 100));
  sliderPos.value = percentage;
};

const onMouseMove = (e: MouseEvent) => {
  if (!isDragging) return;
  handleMove(e.clientX);
};

const onTouchMove = (e: TouchEvent) => {
  if (!isDragging || !e.touches[0]) return;
  handleMove(e.touches[0].clientX);
};

const stopDragging = () => {
  isDragging = false;
  window.removeEventListener('mousemove', onMouseMove);
  window.removeEventListener('mouseup', stopDragging);
  window.removeEventListener('touchmove', onTouchMove);
  window.removeEventListener('touchend', stopDragging);
};

const startDragging = (e: MouseEvent | TouchEvent) => {
  isDragging = true;
  const clientX = 'touches' in e && e.touches[0] ? e.touches[0].clientX : (e as MouseEvent).clientX;
  handleMove(clientX);

  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseup', stopDragging);
  window.addEventListener('touchmove', onTouchMove);
  window.addEventListener('touchend', stopDragging);
};

onMounted(() => {
  updateWidth();
  window.addEventListener('resize', updateWidth);
});

onUnmounted(() => {
  stopDragging();
  window.removeEventListener('resize', updateWidth);
});
</script>
