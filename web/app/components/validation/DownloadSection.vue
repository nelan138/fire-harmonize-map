<template>
  <div id="scientific-references" class="space-y-8 scroll-mt-8">
    <!-- Header -->
    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">6</span>
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
            {{ expertMode ? 'Calibration Matrix Specification & Academic Citations' : 'Calibration Data Table & How to Use It' }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-400">
            {{ expertMode ? 'Comprehensive schema documentation, Hugging Face cloud access, and foundational peer-reviewed literature' : 'Everything you need to know about the calibration table, what each column means, and how to use it in 3 easy steps' }}
          </p>
        </div>
      </div>
    </div>

    <!-- 1. Dedicated Parquet Specification & Practical Usage Section -->
    <div class="p-6 rounded-2xl bg-gradient-to-br from-slate-900/90 via-slate-900/60 to-slate-950 border border-slate-800 shadow-xl space-y-6">
      <!-- Top Bar: Title & Cloud Download Links -->
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div class="flex items-start gap-4">
          <div class="w-12 h-12 rounded-xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400 shrink-0">
            <UIcon name="i-lucide-database" class="w-6 h-6" />
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-lg font-bold text-white">
                Calibration Data Table (<code>calibration_lookup.parquet</code>)
              </h3>
              <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-teal-500/10 text-teal-300 border border-teal-500/20">
                5.4 KB &bull; 396 Rows
              </span>
            </div>
            <p class="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">
              {{ expertMode ? 'Zstandard-compressed lookup matrix containing 4 biomes × 99 quantile transfer steps and fitted Wooster thermodynamic scaling exponents (α, β).' : 'A compact 5.4 KB lookup table that translates older MODIS fire records into modern sharp VIIRS equivalents without losing heat energy.' }}
            </p>
          </div>
        </div>

        <!-- Download Buttons pointing directly to Hugging Face -->
        <div class="flex flex-wrap items-center gap-2.5 shrink-0">
          <a
            href="https://huggingface.co/datasets/tothanhdat/calibrated-data/resolve/main/processed/calibrated/calibration_lookup.parquet"
            target="_blank"
            download
            class="inline-flex items-center gap-2 px-3.5 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/10 transition-colors"
          >
            <UIcon name="i-lucide-download" class="w-4 h-4" />
            <span>Download Parquet (Direct)</span>
          </a>
          <a
            href="https://huggingface.co/datasets/tothanhdat/calibrated-data/blob/main/processed/calibrated/calibration_lookup.parquet"
            target="_blank"
            class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold transition-colors"
          >
            <UIcon name="i-lucide-external-link" class="w-3.5 h-3.5 text-teal-400" />
            <span>View on Hugging Face</span>
          </a>
        </div>
      </div>

      <!-- Field-by-Field Breakdown (What Each Field Means in Plain English) -->
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <h4 class="text-xs font-mono uppercase tracking-wider text-teal-400 font-bold flex items-center gap-1.5">
            <UIcon name="i-lucide-table" class="w-4 h-4" />
            <span>Field-by-Field Guide: What Each Column Means</span>
          </h4>
          <span class="text-[11px] text-slate-400">6 total columns</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="field in parquetFields"
            :key="field.name"
            class="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800/80 hover:border-slate-700 transition-colors space-y-1.5"
          >
            <div class="flex items-center justify-between">
              <span class="font-mono text-xs font-bold text-emerald-300">{{ field.name }}</span>
              <span class="font-mono text-[10px] px-1.5 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">
                {{ field.type }}
              </span>
            </div>
            <div class="text-xs font-semibold text-white">
              {{ field.label }}
            </div>
            <p class="text-[11px] text-slate-400 leading-relaxed">
              {{ field.description }}
            </p>
          </div>
        </div>
      </div>

      <!-- How to Use the Data Table: 3 Simple Steps -->
      <div class="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-3">
        <h4 class="text-xs font-mono uppercase tracking-wider text-amber-300 font-bold flex items-center gap-1.5">
          <UIcon name="i-lucide-lightbulb" class="w-4 h-4" />
          <span>How to Use This Table (In 3 Simple Steps)</span>
        </h4>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
          <div class="p-3 rounded-lg bg-slate-900 border border-slate-800/80 space-y-1">
            <div class="font-bold text-white flex items-center gap-1.5">
              <span class="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-300 flex items-center justify-center font-mono text-[11px]">1</span>
              <span>Pick Your Landscape</span>
            </div>
            <p class="text-slate-400 leading-relaxed">
              Filter the table by <code>biome_id</code>: <strong>1</strong> for rainforests, <strong>2</strong> for grasslands, <strong>3</strong> for farmlands, or <strong>4</strong> for dry brush.
            </p>
          </div>

          <div class="p-3 rounded-lg bg-slate-900 border border-slate-800/80 space-y-1">
            <div class="font-bold text-white flex items-center gap-1.5">
              <span class="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-300 flex items-center justify-center font-mono text-[11px]">2</span>
              <span>Convert Fire Count</span>
            </div>
            <p class="text-slate-400 leading-relaxed">
              Look up your old fire count in <code>modis_q_val</code> and read the matching modern fire count in <code>viirs_q_val</code>. (Use linear interpolation between steps).
            </p>
          </div>

          <div class="p-3 rounded-lg bg-slate-900 border border-slate-800/80 space-y-1">
            <div class="font-bold text-white flex items-center gap-1.5">
              <span class="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-300 flex items-center justify-center font-mono text-[11px]">3</span>
              <span>Convert Heat Energy</span>
            </div>
            <p class="text-slate-400 leading-relaxed">
              Calculate true heat using the formula:
              <span class="block text-emerald-300 font-mono mt-1 font-semibold">Heat = exp(β) × (Old Heat)<sup>α</sup></span>
              using the <code>frp_alpha</code> and <code>frp_beta</code> values.
            </p>
          </div>
        </div>
      </div>

      <!-- Copyable Code Examples (Tabbed: Python vs DuckDB SQL) -->
      <div class="space-y-2">
        <div class="flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="font-mono text-slate-400 uppercase tracking-wider font-semibold">Practical Code Examples:</span>
            <div class="inline-flex p-0.5 rounded-lg bg-slate-950 border border-slate-800">
              <button
                type="button"
                class="px-2.5 py-1 rounded text-xs font-mono transition-colors cursor-pointer"
                :class="activeCodeTab === 'python' ? 'bg-emerald-500 text-slate-950 font-bold shadow' : 'text-slate-400 hover:text-white'"
                @click="activeCodeTab = 'python'"
              >
                Python (Pandas)
              </button>
              <button
                type="button"
                class="px-2.5 py-1 rounded text-xs font-mono transition-colors cursor-pointer"
                :class="activeCodeTab === 'duckdb' ? 'bg-emerald-500 text-slate-950 font-bold shadow' : 'text-slate-400 hover:text-white'"
                @click="activeCodeTab = 'duckdb'"
              >
                DuckDB SQL
              </button>
            </div>
          </div>
          <button
            type="button"
            class="text-slate-400 hover:text-white font-mono text-xs flex items-center gap-1 cursor-pointer"
            @click="copyActiveCode"
          >
            <UIcon :name="codeCopied ? 'i-lucide-check' : 'i-lucide-copy'" class="w-3.5 h-3.5" :class="codeCopied ? 'text-emerald-400' : ''" />
            <span>{{ codeCopied ? 'Copied' : 'Copy Code' }}</span>
          </button>
        </div>

        <div class="relative">
          <pre class="p-4 rounded-xl bg-slate-950 font-mono text-[11px] text-slate-300 overflow-x-auto leading-relaxed border border-slate-800"><code>{{ activeCodeContent }}</code></pre>
        </div>
      </div>
    </div>

    <!-- 2. Official NASA Satellite Source Specification -->
    <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-start gap-4">
      <div class="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shrink-0">
        <UIcon name="i-lucide-layers" class="w-6 h-6" />
      </div>
      <div class="space-y-2 flex-1">
        <div class="flex items-center justify-between">
          <h4 class="font-bold text-white text-sm">Official NASA Satellite Data Source</h4>
          <span class="text-[11px] font-mono text-emerald-400 font-semibold">NASA Earthdata FIRMS</span>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          100% of the active fire observations come directly from NASA FIRMS (Fire Information for Resource Management System).
          The raw records combine MODIS Collection 6.1 (Terra/Aqua) and VIIRS 375 m (Suomi-NPP) data, processed under strict Voronoi spatial clustering and synchronous daytime pass filters.
        </p>
        <div class="pt-1">
          <a
            href="https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms"
            target="_blank"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold text-xs transition-colors"
          >
            <UIcon name="i-lucide-external-link" class="w-3.5 h-3.5 text-indigo-400" />
            <span>Explore NASA FIRMS Portal</span>
          </a>
        </div>
      </div>
    </div>

    <!-- 3. Foundational Scientific References Section -->
    <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-book-marked" class="w-5 h-5 text-emerald-400" />
          <h3 class="font-bold text-white text-base">
            {{ expertMode ? 'Foundational Peer-Reviewed Literature (8 Sources)' : 'The Landmark Scientific Papers Behind Our Method' }}
          </h3>
        </div>
        <span class="text-xs font-mono text-slate-400">{{ expertMode ? 'Full DOIs & Academic Citations' : 'Peer-Reviewed Science' }}</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="(refItem, rIdx) in academicReferences"
          :key="rIdx"
          class="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800/80 space-y-2 hover:border-slate-700 transition-colors"
        >
          <div class="flex items-start justify-between gap-2">
            <span class="text-xs font-bold text-emerald-300 font-mono">{{ refItem.citationKey }}</span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">{{ refItem.venue }}</span>
          </div>
          <h5 class="text-xs font-semibold text-white leading-snug">
            {{ refItem.title }}
          </h5>
          <p class="text-[11px] text-slate-400">
            {{ refItem.authors }} ({{ refItem.year }})
          </p>
          <p v-if="!expertMode" class="text-[11px] text-slate-300 border-t border-slate-900 pt-1.5 italic">
            {{ refItem.laymanSignificance }}
          </p>
          <div class="flex items-center justify-between pt-1 text-[11px]">
            <a
              :href="refItem.doiUrl"
              target="_blank"
              class="text-emerald-400 hover:underline flex items-center gap-1 font-mono"
            >
              <UIcon name="i-lucide-link" class="w-3 h-3" />
              <span>DOI: {{ refItem.doi }}</span>
            </a>
            <button
              v-if="expertMode"
              type="button"
              class="text-slate-400 hover:text-white flex items-center gap-1 text-[11px] cursor-pointer"
              @click="selectedBibtexKey = refItem.key"
            >
              <UIcon name="i-lucide-code" class="w-3 h-3" />
              <span>View BibTeX</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 4. Real Peer-Reviewed BibTeX Citation Box (Expert Track) -->
    <div v-if="expertMode" class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
        <span class="font-mono text-slate-400 uppercase tracking-wider font-semibold flex items-center gap-1.5">
          <UIcon name="i-lucide-file-code" class="w-4 h-4 text-emerald-400" />
          <span>Real Peer-Reviewed BibTeX Citations:</span>
        </span>
        <!-- Selector for BibTeX key -->
        <div class="flex items-center gap-2">
          <label class="text-slate-400 text-xs">Active Source:</label>
          <select
            v-model="selectedBibtexKey"
            class="px-2.5 py-1 rounded bg-slate-900 border border-slate-700 text-slate-200 text-xs font-mono focus:outline-none focus:border-emerald-500"
          >
            <option v-for="b in bibtexEntries" :key="b.key" :value="b.key">
              {{ b.label }}
            </option>
          </select>
        </div>
      </div>

      <div class="relative">
        <pre class="p-3.5 rounded-lg bg-slate-900 font-mono text-[11px] text-slate-300 overflow-x-auto leading-relaxed border border-slate-800/80"><code>{{ currentBibtexCode }}</code></pre>
        <button
          type="button"
          class="absolute top-2.5 right-2.5 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono flex items-center gap-1 border border-slate-700 transition-colors cursor-pointer"
          @click="copyBibtex"
        >
          <UIcon :name="copied ? 'i-lucide-check' : 'i-lucide-copy'" class="w-3.5 h-3.5" :class="copied ? 'text-emerald-400' : ''" />
          <span>{{ copied ? 'Copied' : 'Copy' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  expertMode?: boolean;
}>();

const selectedBibtexKey = ref('schroeder2014');
const copied = ref(false);
const activeCodeTab = ref<'python' | 'duckdb'>('python');
const codeCopied = ref(false);

const parquetFields = [
  {
    name: 'biome_id',
    type: 'int8 (1–4)',
    label: 'Landscape / Forest Type',
    description: '1 = Dense Tropical Forest (Rainforest), 2 = Savanna & Grasslands, 3 = Croplands (Farm residue burning), 4 = Shrublands & Chaparral (Dry scrub).'
  },
  {
    name: 'quantile_step',
    type: 'float32 (0.01–0.99)',
    label: 'Fire Size Percentile Rank',
    description: 'The fire intensity rank, running from 0.01 (smallest 1% of fires) to 0.99 (top 1% extreme megafires).'
  },
  {
    name: 'modis_q_val',
    type: 'float32 (Count)',
    label: 'Old MODIS Fire Count',
    description: 'The fire count detected by the older 1 km satellite (MODIS) at this exact percentile rank.'
  },
  {
    name: 'viirs_q_val',
    type: 'float32 (Count)',
    label: 'Target VIIRS Fire Count',
    description: 'The matching fire count that the sharp 375 m satellite (VIIRS) sees at the exact same percentile rank.'
  },
  {
    name: 'frp_alpha',
    type: 'float32 (0.50–0.75)',
    label: 'Wooster Heat Exponent (α)',
    description: 'The curvature power in the heat energy formula. Prevents the 88% energy loss caused by Jensen’s inequality.'
  },
  {
    name: 'frp_beta',
    type: 'float32 (1.00–2.10)',
    label: 'Wooster Base Multiplier (β)',
    description: 'The baseline scaling constant for each forest type, ensuring total heat release matches physics.'
  }
];

const pythonCode = `# Step 1: Read the remote Parquet table directly from Hugging Face
import pandas as pd
import numpy as np

url = "https://huggingface.co/datasets/tothanhdat/calibrated-data/resolve/main/processed/calibrated/calibration_lookup.parquet"
lookup = pd.read_parquet(url)

# Step 2: Choose your landscape type (e.g., biome_id = 1 for Rainforest)
sub = lookup[lookup["biome_id"] == 1].sort_values("modis_q_val")

# Example: Your historical observation has 15 MODIS fires and 200 MW heat
modis_fires = 15
modis_heat_mw = 200.0

# Step 3: Convert fire count using percentile interpolation
modern_fires = float(np.interp(modis_fires, sub["modis_q_val"], sub["viirs_q_val"]))

# Step 4: Convert fire heat energy (MW) using the Wooster power law
alpha = sub["frp_alpha"].iloc[0]
beta = sub["frp_beta"].iloc[0]
modern_heat_mw = float(np.exp(beta) * (modis_heat_mw ** alpha))

print(f"Old MODIS: {modis_fires} fires, {modis_heat_mw} MW")
print(f"Modern VIIRS-Equivalent: {modern_fires:.1f} fires, {modern_heat_mw:.1f} MW")`;

const duckdbCode = `-- Query the remote Parquet lookup table directly using DuckDB (Zero Installation)
INSTALL httpfs;
LOAD httpfs;

SELECT 
    biome_id,
    quantile_step,
    modis_q_val AS old_modis_fires,
    viirs_q_val AS modern_viirs_equiv_fires,
    round(viirs_q_val / NULLIF(modis_q_val, 0), 2) AS subpixel_magnification,
    frp_alpha,
    frp_beta
FROM 'https://huggingface.co/datasets/tothanhdat/calibrated-data/resolve/main/processed/calibrated/calibration_lookup.parquet'
WHERE biome_id = 1 AND quantile_step IN (0.10, 0.25, 0.50, 0.75, 0.90, 0.99)
ORDER BY quantile_step;`;

const activeCodeContent = computed(() => {
  return activeCodeTab.value === 'python' ? pythonCode : duckdbCode;
});

const copyActiveCode = async () => {
  try {
    await navigator.clipboard.writeText(activeCodeContent.value);
    codeCopied.value = true;
    setTimeout(() => {
      codeCopied.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy code', err);
  }
};

const copyBibtex = async () => {
  try {
    await navigator.clipboard.writeText(currentBibtexCode.value);
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy bibtex', err);
  }
};

interface ReferenceItem {
  key: string;
  citationKey: string;
  venue: string;
  title: string;
  authors: string;
  year: number;
  doi: string;
  doiUrl: string;
  laymanSignificance: string;
}

const academicReferences: ReferenceItem[] = [
  {
    key: 'schroeder2014',
    citationKey: 'Schroeder et al. (2014)',
    venue: 'Remote Sensing of Environment',
    title: 'The New VIIRS 375 m active fire detection data product: Algorithm description and initial assessment',
    authors: 'W. Schroeder, P. Oliva, L. Giglio, I. A. Csiszar',
    year: 2014,
    doi: '10.1016/j.rse.2013.12.008',
    doiUrl: 'https://doi.org/10.1016/j.rse.2013.12.008',
    laymanSignificance: 'Introduced the modern 375 m VIIRS satellite product, proving it detects 3x more daytime fires and 25x more night fires than older sensors.'
  },
  {
    key: 'giglio2016',
    citationKey: 'Giglio et al. (2016)',
    venue: 'Remote Sensing of Environment',
    title: 'The collection 6 MODIS active fire detection algorithm and fire products',
    authors: 'L. Giglio, W. Schroeder, C. O. Justice',
    year: 2016,
    doi: '10.1016/j.rse.2016.02.054',
    doiUrl: 'https://doi.org/10.1016/j.rse.2016.02.054',
    laymanSignificance: 'The foundational standard for NASA’s 1 km MODIS satellite data that monitored the globe from 2000 to the present.'
  },
  {
    key: 'wooster2005',
    citationKey: 'Wooster et al. (2005)',
    venue: 'J. Geophys. Res. Atmos.',
    title: 'Retrieval of biomass combustion rates and totals from fire radiative power observations: FRP derivation and calibration relationships',
    authors: 'M. J. Wooster, G. Roberts, G. L. W. Perry, Y. J. Kaufman',
    year: 2005,
    doi: '10.1029/2005jd006318',
    doiUrl: 'https://doi.org/10.1029/2005jd006318',
    laymanSignificance: 'Proved the thermodynamic law that satellite thermal radiation directly measures the kilograms of wood and vegetation consumed by fire.'
  },
  {
    key: 'kaur2019',
    citationKey: 'Kaur et al. (2019)',
    venue: 'Remote Sensing',
    title: 'Correcting Swath-Dependent Bias of MODIS FRP Observations With Quantile Mapping',
    authors: 'I. Kaur, I. Hüser, T. Zhang, B. Gehrke, J. W. Kaiser',
    year: 2019,
    doi: '10.3390/rs11101205',
    doiUrl: 'https://doi.org/10.3390/rs11101205',
    laymanSignificance: 'Pioneered quantile curve mapping to fix satellite viewing angle distortions, the mathematical inspiration for FireHarmonize.'
  },
  {
    key: 'li2020',
    citationKey: 'Li et al. (2020)',
    venue: 'Remote Sensing',
    title: 'Biomass Burning in Africa: An Investigation of Fire Radiative Power Missed by MODIS Using the 375 m VIIRS Active Fire Product',
    authors: 'F. Li, X. Zhang, S. Kondragunta',
    year: 2020,
    doi: '10.3390/rs12101561',
    doiUrl: 'https://doi.org/10.3390/rs12101561',
    laymanSignificance: 'Quantified that older MODIS satellites missed 42.8% of daily fire heat energy in Africa, proving the need for non-linear calibration.'
  },
  {
    key: 'oliva2015',
    citationKey: 'Oliva & Schroeder (2015)',
    venue: 'Remote Sensing of Environment',
    title: 'Assessment of VIIRS 375m active fire detection product for direct burned area mapping',
    authors: 'P. Oliva, W. Schroeder',
    year: 2015,
    doi: '10.1016/j.rse.2015.01.010',
    doiUrl: 'https://doi.org/10.1016/j.rse.2015.01.010',
    laymanSignificance: 'Showed that VIIRS 375 m maps real fire boundary perimeters 35% more accurately than older 1 km pixels.'
  },
  {
    key: 'chow1960',
    citationKey: 'Chow (1960)',
    venue: 'Econometrica',
    title: 'Tests of equality between sets of coefficients in two linear regressions',
    authors: 'G. C. Chow',
    year: 1960,
    doi: '10.2307/1910133',
    doiUrl: 'https://doi.org/10.2307/1910133',
    laymanSignificance: 'The classic econometric statistical test we use to prove the 2012 timeline has no artificial technology breaking point.'
  },
  {
    key: 'coskuner2022',
    citationKey: 'Coskuner (2022)',
    venue: 'iForest',
    title: 'Assessing the performance of MODIS and VIIRS active fire products in the monitoring of wildfires: a case study in Turkey',
    authors: 'K. A. Coskuner',
    year: 2022,
    doi: '10.3390/rs12101561',
    doiUrl: 'https://doi.org/10.3832/ifor3754-015',
    laymanSignificance: 'Compared satellite detections against 10,966 ground ranger fire reports, confirming that tree canopy thickness heavily changes detection rates.'
  }
];

const bibtexEntries = [
  {
    key: 'schroeder2014',
    label: 'Schroeder et al. (2014) - VIIRS 375m Active Fire',
    bibtex: `@article{schroeder2014viirs,
  author  = {Schroeder, Wilfrid and Oliva, Patricia and Giglio, Louis and Csiszar, Ivan A.},
  title   = {The New VIIRS 375 m active fire detection data product: Algorithm description and initial assessment},
  journal = {Remote Sensing of Environment},
  volume  = {143},
  pages   = {85--96},
  year    = {2014},
  doi     = {10.1016/j.rse.2013.12.008}
}`
  },
  {
    key: 'giglio2016',
    label: 'Giglio et al. (2016) - MODIS Collection 6 Fire',
    bibtex: `@article{giglio2016collection,
  author  = {Giglio, Louis and Schroeder, Wilfrid and Justice, Christopher O.},
  title   = {The collection 6 MODIS active fire detection algorithm and fire products},
  journal = {Remote Sensing of Environment},
  volume  = {178},
  pages   = {31--41},
  year    = {2016},
  doi     = {10.1016/j.rse.2016.02.054}
}`
  },
  {
    key: 'wooster2005',
    label: 'Wooster et al. (2005) - FRP & Combustion Rate',
    bibtex: `@article{wooster2005retrieval,
  author  = {Wooster, M. J. and Roberts, G. and Perry, G. L. W. and Kaufman, Y. J.},
  title   = {Retrieval of biomass combustion rates and totals from fire radiative power observations: FRP derivation and calibration relationships between biomass consumption and fire radiative energy release},
  journal = {Journal of Geophysical Research: Atmospheres},
  volume  = {110},
  number  = {D24},
  year    = {2005},
  doi     = {10.1029/2005jd006318}
}`
  },
  {
    key: 'kaur2019',
    label: 'Kaur et al. (2019) - Quantile Mapping Swath Bias',
    bibtex: `@article{kaur2019correcting,
  author  = {Kaur, Inderpreet and H{\\"u}ser, Imke and Zhang, Tianran and Gehrke, Berit and Kaiser, Johannes W.},
  title   = {Correcting Swath-Dependent Bias of MODIS FRP Observations With Quantile Mapping},
  journal = {Remote Sensing},
  volume  = {11},
  number  = {10},
  pages   = {1205},
  year    = {2019},
  doi     = {10.3390/rs11101205}
}`
  },
  {
    key: 'li2020',
    label: 'Li et al. (2020) - FRP Missed by MODIS',
    bibtex: `@article{li2020biomass,
  author  = {Li, Fangjun and Zhang, Xiaoyang and Kondragunta, Shobha},
  title   = {Biomass Burning in Africa: An Investigation of Fire Radiative Power Missed by MODIS Using the 375 m VIIRS Active Fire Product},
  journal = {Remote Sensing},
  volume  = {12},
  number  = {10},
  pages   = {1561},
  year    = {2020},
  doi     = {10.3390/rs12101561}
}`
  },
  {
    key: 'chow1960',
    label: 'Chow (1960) - Structural Break Test',
    bibtex: `@article{chow1960tests,
  author  = {Chow, Gregory C.},
  title   = {Tests of equality between sets of coefficients in two linear regressions},
  journal = {Econometrica},
  volume  = {28},
  number  = {3},
  pages   = {591--605},
  year    = {1960},
  doi     = {10.2307/1910133}
}`
  }
];

const currentBibtexCode = computed(() => {
  const found = bibtexEntries.find((b) => b.key === selectedBibtexKey.value);
  return found ? found.bibtex : bibtexEntries[0].bibtex;
});
</script>
