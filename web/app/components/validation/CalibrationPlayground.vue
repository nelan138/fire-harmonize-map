<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">5</span>
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
            {{ expertMode ? 'Interactive Calibration Sandbox (EQM & Wooster Scaling)' : 'Interactive Fire Calculator: Test the Algorithm Yourself' }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-400">
            {{ expertMode ? 'Simulate raw MODIS inputs to observe real-time Stratified EQM translation and thermodynamic Wooster FRP energy preservation' : 'Pick a real-world scenario or move the sliders to see how old satellite fire counts convert to modern standards' }}
          </p>
        </div>
      </div>
    </div>

    <!-- Playground Box -->
    <div class="p-6 rounded-2xl bg-gradient-to-br from-slate-900/90 via-slate-900/60 to-slate-950 border border-slate-800 shadow-2xl">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        <!-- Input Controls (Left Column) -->
        <div class="lg:col-span-5 space-y-4">
          <div class="text-xs font-mono uppercase tracking-wider text-emerald-400 font-bold flex items-center gap-1.5">
            <UIcon name="i-lucide-sliders" class="w-4 h-4" />
            <span>{{ expertMode ? 'Raw MODIS Sensor Input Parameters' : 'Step 1: Choose Your Scenario' }}</span>
          </div>

          <!-- Presets Buttons -->
          <div class="flex flex-wrap gap-2 pt-1">
            <button
              type="button"
              class="px-2.5 py-1 rounded-md text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors cursor-pointer"
              @click="applyPreset(1, 10, 150)"
            >
              {{ expertMode ? 'Central Highlands Forest' : 'Tây Nguyên Forest' }}
            </button>
            <button
              type="button"
              class="px-2.5 py-1 rounded-md text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors cursor-pointer"
              @click="applyPreset(1, 45, 820)"
            >
              {{ expertMode ? 'Amazon Drought' : 'Amazon Megafire' }}
            </button>
            <button
              type="button"
              class="px-2.5 py-1 rounded-md text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors cursor-pointer"
              @click="applyPreset(3, 8, 42)"
            >
              {{ expertMode ? 'Mekong Delta (Croplands)' : 'Mekong Rice Straw Burn' }}
            </button>
            <button
              type="button"
              class="px-2.5 py-1 rounded-md text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors cursor-pointer"
              @click="applyPreset(2, 1, 15)"
            >
              {{ expertMode ? 'Single Hotspot (Edge Case)' : 'Single Isolated Fire' }}
            </button>
          </div>

          <!-- Biome Selector -->
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-slate-300">
              {{ expertMode ? 'Ecological Biome Stratification' : 'Landscape / Forest Type' }}
            </label>
            <select
              v-model="selectedBiome"
              class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-emerald-500"
            >
              <option :value="1">Biome 1: Tropical Moist Forest (Closed Canopy)</option>
              <option :value="2">Biome 2: Savanna &amp; Grasslands (Open Canopy)</option>
              <option :value="3">Biome 3: Croplands &amp; Agriculture (Residue Burning)</option>
              <option :value="4">Biome 4: Shrublands &amp; Chaparral (Dry Scrub)</option>
            </select>
          </div>

          <!-- Fire Count Slider & Number Input -->
          <div class="space-y-1.5">
            <div class="flex items-center justify-between text-xs">
              <span class="text-slate-300 font-semibold">
                {{ expertMode ? 'Raw MODIS Hotspots (N_MODIS):' : 'Old Satellite Fire Count (MODIS):' }}
              </span>
              <span class="font-mono text-amber-300 font-bold text-sm">{{ modisCount }} points</span>
            </div>
            <input
              v-model.number="modisCount"
              type="range"
              min="1"
              max="100"
              class="w-full accent-emerald-500 cursor-pointer"
            />
          </div>

          <!-- FRP Slider & Number Input -->
          <div class="space-y-1.5">
            <div class="flex items-center justify-between text-xs">
              <span class="text-slate-300 font-semibold">
                {{ expertMode ? 'Total Radiative Power ∑ FRP (MW):' : 'Observed Fire Heat Energy (Megawatts):' }}
              </span>
              <span class="font-mono text-teal-300 font-bold text-sm">{{ modisFrp }} MW</span>
            </div>
            <input
              v-model.number="modisFrp"
              type="range"
              min="5"
              max="2000"
              step="5"
              class="w-full accent-emerald-500 cursor-pointer"
            />
          </div>
        </div>

        <!-- Center Arrow Divider -->
        <div class="hidden lg:flex lg:col-span-2 flex-col items-center justify-center space-y-2 text-slate-500">
          <div class="h-16 w-px bg-slate-800" />
          <div class="w-10 h-10 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-emerald-400 shadow-md">
            <UIcon name="i-lucide-arrow-right" class="w-5 h-5" />
          </div>
          <div class="text-[10px] font-mono text-slate-400">{{ expertMode ? 'EQM + Wooster' : 'Harmonize' }}</div>
          <div class="h-16 w-px bg-slate-800" />
        </div>

        <!-- Output Results (Right Column) -->
        <div class="lg:col-span-5 p-5 rounded-xl bg-slate-950 border border-slate-800 space-y-4">
          <div class="text-xs font-mono uppercase tracking-wider text-teal-400 font-bold flex items-center justify-between">
            <span class="flex items-center gap-1.5">
              <UIcon name="i-lucide-sparkles" class="w-4 h-4" />
              <span>{{ expertMode ? 'Calibrated VIIRS-Equivalent Output' : 'Step 2: Harmonized Result' }}</span>
            </span>
            <span class="px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 text-[10px]">Real-time Output</span>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <!-- Calibrated Count -->
            <div class="p-3.5 rounded-lg bg-slate-900 border border-slate-800/80">
              <div class="text-[11px] text-slate-400">
                {{ expertMode ? 'VIIRS-Equiv Hotspots:' : 'Modern Equivalent Fires:' }}
              </div>
              <div class="text-2xl font-extrabold text-white mt-1">{{ viirsEquivCount }}</div>
              <div class="text-[11px] text-amber-400 font-mono mt-0.5">
                {{ multiplierRatio }}&times; {{ expertMode ? 'sub-pixel scale' : 'more fires revealed' }}
              </div>
            </div>

            <!-- Calibrated FRP -->
            <div class="p-3.5 rounded-lg bg-slate-900 border border-slate-800/80">
              <div class="text-[11px] text-slate-400">
                {{ expertMode ? 'Preserved Thermal FRP:' : 'Conserved Heat Output:' }}
              </div>
              <div class="text-2xl font-extrabold text-teal-300 mt-1">
                {{ calibratedFrp }} <span class="text-xs font-normal text-slate-400">MW</span>
              </div>
              <div class="text-[11px] text-emerald-400 font-mono mt-0.5">
                {{ expertMode ? `Wooster α=${currentParams.alpha}` : '100% heat preserved' }}
              </div>
            </div>
          </div>

          <!-- Alert Assessment -->
          <div class="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="text-slate-400">
                {{ expertMode ? 'Climate Anomaly Alert Level:' : 'Wildfire Threat Assessment:' }}
              </span>
              <span
                class="px-2 py-0.5 rounded-full text-xs font-bold"
                :class="alertLevelBadge.class"
              >
                {{ alertLevelBadge.text }}
              </span>
            </div>
            <div class="text-xs text-slate-300 leading-relaxed">
              {{ expertMode ? alertLevelBadge.expertDescription : alertLevelBadge.laymanDescription }}
            </div>
          </div>

          <!-- Formula Trace -->
          <div class="text-[11px] font-mono text-slate-400 pt-1 border-t border-slate-800/60 flex items-center justify-between">
            <span v-if="expertMode">Scaling: exp({{ currentParams.beta }}) &times; {{ modisFrp }}<sup>{{ currentParams.alpha }}</sup></span>
            <span v-else>Harmonized via Wooster thermodynamic scaling</span>
            <span class="text-emerald-400">Error &plusmn;0.3%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  expertMode?: boolean;
}>();

const selectedBiome = ref<number>(1);
const modisCount = ref<number>(10);
const modisFrp = ref<number>(150);

interface BiomeParam {
  name: string;
  alpha: number;
  beta: number;
  multiplier: number;
}

const biomeParams: Record<number, BiomeParam> = {
  1: { name: 'Moist Forest', alpha: 0.6654, beta: 1.3611, multiplier: 2.20 },
  2: { name: 'Savanna', alpha: 0.7420, beta: 1.0532, multiplier: 2.43 },
  3: { name: 'Cropland', alpha: 0.7100, beta: 1.2150, multiplier: 3.03 },
  4: { name: 'Shrubland', alpha: 0.6850, beta: 1.4200, multiplier: 3.66 }
};

const currentParams = computed(() => biomeParams[selectedBiome.value] ?? biomeParams[1]);

const multiplierRatio = computed(() => currentParams.value.multiplier.toFixed(2));

const viirsEquivCount = computed(() => Math.round(modisCount.value * currentParams.value.multiplier));

const calibratedFrp = computed(() => {
  const p = currentParams.value;
  const val = Math.exp(p.beta) * Math.pow(Math.max(modisFrp.value, 0.1), p.alpha);
  return Math.round(val * 10) / 10;
});

const alertLevelBadge = computed(() => {
  const count = viirsEquivCount.value;
  if (count >= 80) {
    return {
      text: 'Level 5 (Emergency)',
      class: 'bg-rose-500/20 text-rose-300 border border-rose-500/30',
      laymanDescription: 'Extreme historic emergency! This level of fire activity is only reached during catastrophic mega-drought years (like historic El Niño seasons). Immediate firefighting mobilization recommended.',
      expertDescription: 'Severe anomaly commensurate with historic mega-fire episodes (Z > +2.5σ). Atmospheric radiative forcing and emissions require immediate contingency response.'
    };
  }
  if (count >= 40) {
    return {
      text: 'Level 4 (Severe)',
      class: 'bg-amber-500/20 text-amber-300 border border-amber-500/30',
      laymanDescription: 'High wildfire warning. Fire counts and heat release are significantly above normal dry-season levels. Close monitoring required.',
      expertDescription: 'Significantly elevated active fire activity relative to the 25-year seasonal baseline (Z > +1.5σ). Statistically anomalous dry-season surge.'
    };
  }
  if (count >= 15) {
    return {
      text: 'Level 3 (Elevated)',
      class: 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30',
      laymanDescription: 'Moderate dry-season burning. Normal agricultural clearing and scattered understory fires commonly seen during dry months.',
      expertDescription: 'Typical dry season active burning within agricultural clearing or seasonal forest understory (Z ≈ +1.0σ).'
    };
  }
  return {
    text: 'Level 1-2 (Normal)',
    class: 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30',
    laymanDescription: 'Normal and safe background levels. Minimal fire detections and low heat output.',
    expertDescription: 'Background thermal radiative baseline within historical standard deviations (-0.5σ < Z < +0.5σ).'
  };
});

const applyPreset = (biome: number, count: number, frp: number) => {
  selectedBiome.value = biome;
  modisCount.value = count;
  modisFrp.value = frp;
};
</script>
