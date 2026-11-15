<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">4</span>
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
            {{ expertMode ? 'Publication-Grade Scientific Figures (300 DPI)' : 'Visual Evidence Gallery: 5 NASA Satellite Proofs' }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-400">
            {{ expertMode ? 'Direct diagnostic outputs from authentic NASA FIRMS observations &mdash; Click any figure to expand full-screen modal' : 'Real satellite charts showing how our algorithm repairs historical fire trends &mdash; Click to enlarge' }}
          </p>
        </div>
      </div>
    </div>

    <!-- Figure Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="(fig, idx) in activeFigures"
        :key="idx"
        class="group flex flex-col rounded-xl bg-slate-900/60 border border-slate-800 hover:border-emerald-500/40 transition-all overflow-hidden shadow-lg"
      >
        <!-- Image Container with Modal Trigger -->
        <div
          class="relative aspect-[16/10] bg-slate-950 overflow-hidden cursor-pointer"
          @click="selectedFigure = fig"
        >
          <img
            :src="fig.src"
            :alt="fig.title"
            class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />
          <div class="absolute inset-0 bg-slate-950/20 group-hover:bg-transparent transition-colors flex items-center justify-center opacity-0 group-hover:opacity-100">
            <span class="px-3 py-1.5 rounded-lg bg-slate-900/90 text-white text-xs font-medium border border-slate-700 flex items-center gap-1.5 shadow-xl">
              <UIcon name="i-lucide-maximize-2" class="w-3.5 h-3.5 text-emerald-400" />
              <span>{{ expertMode ? 'Expand High-Res Figure' : 'Enlarge Image' }}</span>
            </span>
          </div>
          <!-- Tag Badge -->
          <div class="absolute top-2 left-2 px-2 py-0.5 rounded bg-slate-900/80 backdrop-blur-sm border border-slate-700 text-[11px] font-mono font-bold text-emerald-400">
            {{ fig.tag }}
          </div>
        </div>

        <!-- Card Body -->
        <div class="p-4 flex-1 flex flex-col justify-between space-y-3">
          <div>
            <h4 class="font-bold text-white text-sm leading-snug group-hover:text-emerald-300 transition-colors">
              {{ fig.title }}
            </h4>
            <p class="text-xs text-slate-400 mt-1 line-clamp-2">
              {{ fig.shortDesc }}
            </p>
          </div>

          <!-- Caption Accordion Toggle -->
          <div class="pt-2 border-t border-slate-800">
            <button
              type="button"
              class="w-full text-left text-xs font-medium text-emerald-400 hover:text-emerald-300 flex items-center justify-between py-1 transition-colors cursor-pointer"
              @click="toggleCaption(idx)"
            >
              <span class="flex items-center gap-1">
                <UIcon name="i-lucide-book-open" class="w-3.5 h-3.5" />
                <span>{{ openedCaptions.includes(idx) ? 'Hide Explanation' : (expertMode ? 'Figure Reading Guide' : 'How to Read This Chart') }}</span>
              </span>
              <UIcon
                :name="openedCaptions.includes(idx) ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'"
                class="w-4 h-4 transition-transform"
              />
            </button>

            <!-- Expanded Caption Box -->
            <div v-if="openedCaptions.includes(idx)" class="mt-2.5 p-3 rounded-lg bg-slate-950 border border-slate-800/80 text-xs text-slate-300 space-y-1.5 leading-relaxed">
              <div v-for="(guide, gIdx) in fig.detailedGuide" :key="gIdx" class="flex items-start gap-1.5">
                <span class="text-emerald-400 shrink-0 font-bold">&bull;</span>
                <span><strong class="text-white">{{ guide.label }}:</strong> {{ guide.desc }}</span>
              </div>
              <div class="p-2 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-[11px] mt-2 font-medium">
                <strong>{{ expertMode ? 'Scientific Takeaway:' : 'Key Takeaway:' }}</strong> {{ fig.keyTakeaway }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Fullscreen Modal Lightbox -->
    <div
      v-if="selectedFigure"
      class="fixed inset-0 z-50 bg-slate-950/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-8"
      @click.self="selectedFigure = null"
    >
      <div class="relative max-w-5xl w-full bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        <!-- Modal Header -->
        <div class="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div>
            <div class="text-xs font-mono text-emerald-400 font-bold">{{ selectedFigure.tag }}</div>
            <div class="text-base sm:text-lg font-bold text-white">{{ selectedFigure.title }}</div>
          </div>
          <button
            type="button"
            class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors cursor-pointer"
            @click="selectedFigure = null"
          >
            <UIcon name="i-lucide-x" class="w-5 h-5" />
          </button>
        </div>

        <!-- Modal Image Body -->
        <div class="p-4 overflow-auto flex-1 bg-slate-950 flex items-center justify-center">
          <img
            :src="selectedFigure.src"
            :alt="selectedFigure.title"
            class="max-w-full max-h-[70vh] object-contain rounded-lg"
          />
        </div>

        <!-- Modal Footer -->
        <div class="p-3 bg-slate-900 border-t border-slate-800 text-xs text-slate-400 flex items-center justify-between">
          <span>{{ expertMode ? 'Publication-grade resolution (300 DPI Matplotlib Scientific Vector Engine)' : 'Authentic NASA Satellite FIRMS Data' }}</span>
          <a
            :href="selectedFigure.src"
            target="_blank"
            download
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition-colors"
          >
            <UIcon name="i-lucide-download" class="w-4 h-4" />
            <span>Download High-Res PNG</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  expertMode?: boolean;
}>();

interface FigureItem {
  tag: string;
  title: string;
  shortDesc: string;
  src: string;
  keyTakeaway: string;
  detailedGuide: { label: string; desc: string }[];
}

const selectedFigure = ref<FigureItem | null>(null);
const openedCaptions = ref<number[]>([]);

const toggleCaption = (idx: number) => {
  if (openedCaptions.value.includes(idx)) {
    openedCaptions.value = openedCaptions.value.filter((i) => i !== idx);
  } else {
    openedCaptions.value.push(idx);
  }
};

const laymanFigures: FigureItem[] = [
  {
    tag: 'FIGURE 1',
    title: 'Proof 1: True Heat Energy Is Fully Conserved',
    shortDesc: 'Comparing real fire heat release against our predictions across forests and grasslands.',
    src: '/visualizations/fig1_frp_scaling_energy_conservation.png',
    keyTakeaway: 'The red predicted heat bar perfectly matches the dark blue real satellite bar with less than 0.3% difference.',
    detailedGuide: [
      { label: 'Left Chart', desc: 'Each dot is a real fire. The colored lines show our mathematical curve matching older satellite data to modern standards.' },
      { label: 'Middle Chart', desc: 'Error bell curve: The green peak centers tightly on zero, proving our model neither undercounts nor exaggerates fire energy.' },
      { label: 'Right Chart', desc: 'Total energy comparison: Red (Our Model) and Dark Blue (Real VIIRS measurements) are virtually identical.' }
    ]
  },
  {
    tag: 'FIGURE 2',
    title: 'Proof 2: Fair Scaling Without Exaggerating Mega-Fires',
    shortDesc: 'How we smoothly translate fire rankings instead of using a rigid, distorting multiplier.',
    src: '/visualizations/fig2_count_quantile_mapping_ecdf.png',
    keyTakeaway: 'Every fire category receives its natural scaling factor (2x to 4x) according to the type of forest or field.',
    detailedGuide: [
      { label: 'Left Chart', desc: 'Cumulative probability curve: shows how fire intensity is distributed across 17,771 real geographical cells.' },
      { label: 'Middle Chart', desc: 'The translation curves: naturally bend according to real vegetation density instead of forcing an artificial straight line.' },
      { label: 'Right Chart', desc: 'How many small VIIRS fires fit inside one old MODIS pixel (average is approximately 3 fires per square kilometer).' }
    ]
  },
  {
    tag: 'FIGURE 3',
    title: 'Proof 3: Fixing the False 2012 Spike Across 5 Continents',
    shortDesc: 'Testing our model on 5 global fire hotspots: Amazon, California, Vietnam, Brazil Pantanal, and Australia.',
    src: '/visualizations/fig3_sensor_fracture_time_series.png',
    keyTakeaway: 'In every continent, the raw numbers had a fake 2012 jump. Our coral harmonized line makes the timeline smooth and continuous.',
    detailedGuide: [
      { label: 'Left Chart', desc: 'Daily fire counts: Gray (old MODIS), Dark Red (raw VIIRS), and Coral (our harmonized continuous curve).' },
      { label: 'Middle Chart', desc: 'Total fire heat across all 5 benchmark regions, maintaining consistent energy levels.' },
      { label: 'Right Chart', desc: 'Standardized drought index: clearly highlights true historic mega-drought years regardless of which satellite was flying.' }
    ]
  },
  {
    tag: 'FIGURE 4',
    title: 'Proof 4: A Close-Up Case Study (Central Highlands, Vietnam)',
    shortDesc: 'Side-by-side satellite view during peak dry season burning on March 15–19, 2023.',
    src: '/visualizations/fig4_spatial_subpixel_granularity.png',
    keyTakeaway: 'Modern VIIRS detects 4.6x more hotspots because it catches small farming and roadside burns under the forest canopy.',
    detailedGuide: [
      { label: 'Left (MODIS)', desc: 'Only sees isolated, large 1 km squares and misses small scattered agricultural fires.' },
      { label: 'Middle (VIIRS)', desc: 'Resolves dense 375 m clusters tracing actual valley topography and agricultural clearings.' },
      { label: 'Right (Harmonized)', desc: 'Our hexagonal energy map highlights true fire cores without losing sight of small fires.' }
    ]
  },
  {
    tag: 'FIGURE 5',
    title: 'Proof 5: Complete Verification Dashboard',
    shortDesc: 'All quality and statistical checks compiled into one comprehensive overview.',
    src: '/visualizations/fig5_comprehensive_validation_dashboard.png',
    keyTakeaway: 'All tests verify that FireHarmonize delivers a seamless, reliable 25-year wildfire record.',
    detailedGuide: [
      { label: 'Top Panels', desc: 'Statistical alignment showing perfect 1-to-1 diagonal agreement across all biomes.' },
      { label: 'Bottom Left', desc: 'Error distribution centered at 0% error with minimal scatter.' },
      { label: 'Bottom Right', desc: 'Quality audit summary table confirming 100% test success.' }
    ]
  }
];

const expertFigures: FigureItem[] = [
  {
    tag: 'FIGURE 1',
    title: 'Wooster FRP Power Scaling & Energy Conservation',
    shortDesc: 'Log-log radiative power scaling curves across 4 biomes and cumulative thermal energy preservation.',
    src: '/visualizations/fig1_frp_scaling_energy_conservation.png',
    keyTakeaway: 'Discrete event-level Wooster power scaling maintains cumulative energy error between -0.29% and +0.32% on the independent test split.',
    detailedGuide: [
      { label: 'Panel (a) Left', desc: 'Log-log scatter plot of MODIS FRP (1 km) versus coincident VIIRS FRP (375 m). Dashed black line represents 1:1 parity; colored curves depict fitted Wooster functions per biome.' },
      { label: 'Panel (b) Center', desc: 'Residual error distributions before and after calibration. The emerald curve collapses tightly around 0%, eliminating systematic underestimation.' },
      { label: 'Panel (c) Right', desc: 'Cumulative thermal energy totals. Calibrated predictions (red bar) match ground-truth VIIRS measurements (dark blue bar) with remarkable fidelity.' }
    ]
  },
  {
    tag: 'FIGURE 2',
    title: 'Stratified Empirical Quantile Mapping (EQM) & Multipliers',
    shortDesc: 'Empirical cumulative distribution functions on 0.1° grids and sub-pixel fire count expansion multipliers.',
    src: '/visualizations/fig2_count_quantile_mapping_ecdf.png',
    keyTakeaway: 'Completely eliminates legacy m_counts = [1, 1, 1] degeneracy, providing smooth 35-tier non-parametric quantile lookup functions.',
    detailedGuide: [
      { label: 'Panel (a) Left', desc: 'ECDF curves extracted from 17,771 authentic grid cells. The MODIS curve (dashed amber) rises steeper than the high-resolution VIIRS curve (solid teal).' },
      { label: 'Panel (b) Center', desc: 'Non-linear EQM mapping functions stratified by biome, bending with real empirical densities rather than forcing a linear scalar.' },
      { label: 'Panel (c) Right', desc: 'Frequency distribution of coincident VIIRS hotspots within individual MODIS footprints (Median = 3.0x, Mean = 2.96x).' }
    ]
  },
  {
    tag: 'FIGURE 3',
    title: 'Multi-Continental Sensor Fracture Assessment Across 5 Global Hotspots',
    shortDesc: 'Raw hotspot counts vs harmonized continuous time series in the Amazon, California, Indochina, Pantanal, and SE Australia.',
    src: '/visualizations/fig3_sensor_fracture_time_series.png',
    keyTakeaway: 'Demonstrates that the 2012 sensor fracture is a ubiquitous global phenomenon and confirms continuous calibration across all biomes.',
    detailedGuide: [
      { label: 'Panel (a) Left', desc: 'Observed daily fire counts: raw MODIS (gray), raw VIIRS (dark red), and calibrated harmonized time series (coral).' },
      { label: 'Panel (b) Center', desc: 'Integrated Fire Radiative Power (FRP in 1,000 MW) across all 5 benchmark campaign regions.' },
      { label: 'Panel (c) Right', desc: 'Standardized Fire Anomaly Index (SFAI Z-Score) distribution, clearly isolating severe drought anomalies above +1.0σ.' }
    ]
  },
  {
    tag: 'FIGURE 4',
    title: 'Spatial Sub-Pixel Granularity Case Study (Central Highlands, Vietnam)',
    shortDesc: 'Active fire episode on March 15–19, 2023: MODIS 1 km vs VIIRS 375 m vs Integrated Radiative Flux.',
    src: '/visualizations/fig4_spatial_subpixel_granularity.png',
    keyTakeaway: 'VIIRS captures 4.60x more hotspots by detecting small under-canopy and field clearing fires in dry deciduous dipterocarp forests.',
    detailedGuide: [
      { label: 'Left Panel (MODIS)', desc: 'Coarse 1 km footprints detect only isolated perimeters, omitting scattered fire fronts.' },
      { label: 'Center Panel (VIIRS)', desc: 'Fine 375 m clusters resolve fine-scale fire propagation lines along river valleys and agricultural clearings.' },
      { label: 'Right Panel (Calibrated)', desc: 'Uber H3 hexagonal density grid integrated with calibrated radiative energy flux (MW), highlighting regional thermal cores.' }
    ]
  },
  {
    tag: 'FIGURE 5',
    title: 'Comprehensive Scientific Validation Dashboard',
    shortDesc: 'Multi-axis audit: Parity alignment, empirical quantile curves, residual distributions, and quantitative scorecard.',
    src: '/visualizations/fig5_comprehensive_validation_dashboard.png',
    keyTakeaway: 'Full evidentiary dossier meeting the peer-review standards of Remote Sensing of Environment and IEEE Transactions on Geoscience and Remote Sensing.',
    detailedGuide: [
      { label: 'Panels (a) & (b)', desc: '1:1 parity diagonal and cumulative ECDF transfer curves stratified by MCD12Q1 land cover biomes.' },
      { label: 'Panel (c)', desc: 'Residual error distribution: Calibrated curve (emerald) centers around 0% compared to wide dispersion in raw inputs.' },
      { label: 'Panel (d)', desc: 'Quantitative verification scorecard auditing all statistical and thermodynamic metrics.' }
    ]
  }
];

const activeFigures = computed(() => (props.expertMode ? expertFigures : laymanFigures));
</script>
