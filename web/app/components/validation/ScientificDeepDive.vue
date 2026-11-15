<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">3</span>
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
            {{ expertMode ? 'Mathematical Formulations & Atmospheric Physics' : 'The Science Made Simple: How We Harmonize Fire Records' }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-400">
            {{ expertMode ? "Stratified ECDF quantile mapping, Wooster thermodynamic radiative scaling, and the algebraic resolution of Jensen's inequality" : 'Two core innovations that make 25 years of wildfire satellite data speak the exact same language' }}
          </p>
        </div>
      </div>
    </div>

    <!-- GENERAL TRACK CARDS -->
    <div v-if="!expertMode" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Layman Card 1: The Percentile Translator -->
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-sparkles" class="w-5 h-5 text-emerald-400" />
            <h3 class="font-bold text-white text-base">1. The Percentile Curve Matcher</h3>
          </div>
          <span class="text-xs font-mono text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">Fair Ranking</span>
        </div>

        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Instead of multiplying everything by a dumb fixed number, we use <strong>percentile matching</strong>. Think of it like standardizing test scores across different years:
        </p>

        <!-- Analogy Box -->
        <div class="p-4 rounded-lg bg-slate-950 border border-emerald-500/30 text-xs sm:text-sm text-slate-300 space-y-2">
          <div class="font-bold text-emerald-300 flex items-center gap-2">
            <UIcon name="i-lucide-graduation-cap" class="w-4 h-4 text-amber-400" />
            <span>The Standardized Exam Analogy (SAT / GRE)</span>
          </div>
          <p>
            If a math exam in the year 2000 was extremely difficult (MODIS), scoring <strong>70/100</strong> put you in the <strong>Top 5%</strong>.
          </p>
          <p>
            In 2012, a new exam was easier (VIIRS), so you needed <strong>95/100</strong> to reach that same <strong>Top 5%</strong>.
          </p>
          <p class="text-emerald-300 font-medium">
            Our algorithm matches the percentile ranks: an old 70 automatically translates to a modern 95. Every wildfire month is evaluated fairly against its own era!
          </p>
        </div>

        <!-- 4 Terrain Types -->
        <div class="space-y-1.5 text-xs">
          <div class="text-slate-400 font-semibold">Magnification Differences By Landscape:</div>
          <div class="grid grid-cols-2 gap-2">
            <div class="p-2.5 rounded bg-slate-950/80 border border-slate-800">
              <div class="text-emerald-400 font-bold">Rainforests: 2.20&times;</div>
              <div class="text-[11px] text-slate-400">Tree canopy hides small fires from older satellites</div>
            </div>
            <div class="p-2.5 rounded bg-slate-950/80 border border-slate-800">
              <div class="text-emerald-400 font-bold">Savannas: 2.43&times;</div>
              <div class="text-[11px] text-slate-400">Fast open grass fires spread wide and fast</div>
            </div>
            <div class="p-2.5 rounded bg-slate-950/80 border border-slate-800">
              <div class="text-amber-400 font-bold">Farm Fields: 3.03&times;</div>
              <div class="text-[11px] text-slate-400">Tiny straw burning patches are resolved in 375 m</div>
            </div>
            <div class="p-2.5 rounded bg-slate-950/80 border border-slate-800">
              <div class="text-rose-400 font-bold">Dry Brush: 3.66&times;</div>
              <div class="text-[11px] text-slate-400">Intense dry scrub generates scattered embers</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Layman Card 2: The Energy Law -->
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-zap" class="w-5 h-5 text-amber-400" />
            <h3 class="font-bold text-white text-base">2. The Fire Heat Energy Law</h3>
          </div>
          <span class="text-xs font-mono text-amber-400 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">Conservation of Energy</span>
        </div>

        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Counting dots on a map can be misleading: a small roadside campfire and a massive raging forest fire shouldn't count as "1 fire each".
          We track <strong>Fire Radiative Power (Megawatts)</strong>—the real physical heat released by burning vegetation.
        </p>

        <!-- Jensen's Trap Layman Box -->
        <div class="p-4 rounded-lg bg-rose-950/20 border border-rose-500/30 text-xs sm:text-sm text-slate-300 space-y-2">
          <div class="text-rose-400 font-bold flex items-center gap-1.5">
            <UIcon name="i-lucide-alert-triangle" class="w-4 h-4 shrink-0" />
            <span>The Fruit Blender Analogy (Solving Jensen's Trap)</span>
          </div>
          <p>
            Imagine you want to calculate the sweetness of a fruit salad. If you blend each fruit individually and taste them, you get the true total sweetness.
          </p>
          <p>
            In older software, someone took all the fruits together first, then applied a curved formula to the whole pile. Because of a mathematical rule called <em>Jensen's Inequality</em>, <strong>88% of the real heat energy vanished into thin air!</strong>
          </p>
          <p class="text-emerald-300 font-medium">
            FireHarmonize calculates energy for each fire individually before summing them up, recovering 88.7% of lost fire energy and keeping historical heat balances true.
          </p>
        </div>

        <div class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-400">
          <strong>Outcome for Climate Models:</strong> Accurate heat energy allows carbon emission estimates (CO<sub>2</sub> and PM2.5 smoke) to remain consistent across the entire 2000–2026 satellite record.
        </div>
      </div>
    </div>

    <!-- SCIENTIFIC DEEP DIVE CARDS -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Card 1: Stratified EQM -->
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-binary" class="w-5 h-5 text-emerald-400" />
            <h3 class="font-bold text-white text-base">1. Stratified Empirical Quantile Mapping (EQM)</h3>
          </div>
          <span class="text-xs font-mono text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">Non-Parametric</span>
        </div>

        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Extending the swath-calibration approach of <a href="https://doi.org/10.3390/rs11101205" target="_blank" class="text-emerald-400 hover:underline">Kaur et al. (2019)</a> to cross-sensor active fire mapping, our model constructs non-parametric cumulative distribution transfer functions conditioned on MCD12Q1 land-cover biomes:
        </p>

        <!-- Equation Box -->
        <div class="p-3.5 rounded-lg bg-slate-950 border border-emerald-500/30 text-center font-mono space-y-1">
          <div class="text-emerald-300 text-sm sm:text-base font-bold">
            N̂<sub>VIIRS, b</sub> = F<sub>VIIRS, b</sub><sup>-1</sup> ( F<sub>MODIS, b</sub> ( N<sub>MODIS, b</sub> ) )
          </div>
          <div class="text-[11px] text-slate-400">
            Where F<sub>MODIS, b</sub> is the ECDF of MODIS in Biome b, and F<sub>VIIRS, b</sub><sup>-1</sup> is the inverse empirical quantile function of VIIRS.
          </div>
        </div>

        <!-- 4 Biomes Table -->
        <div class="space-y-1.5 text-xs font-mono">
          <div class="text-slate-400 font-semibold mb-1">Empirical Sub-Pixel Multipliers Across 4 Biomes:</div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <div class="p-2 rounded bg-slate-950/80 border border-slate-800 text-center">
              <div class="text-emerald-400 font-bold">Biome 1</div>
              <div class="text-[10px] text-slate-400">Tropical Moist Forest</div>
              <div class="text-amber-300 font-bold mt-1">2.20&times;</div>
            </div>
            <div class="p-2 rounded bg-slate-950/80 border border-slate-800 text-center">
              <div class="text-emerald-400 font-bold">Biome 2</div>
              <div class="text-[10px] text-slate-400">Savanna &amp; Grasslands</div>
              <div class="text-amber-300 font-bold mt-1">2.43&times;</div>
            </div>
            <div class="p-2 rounded bg-slate-950/80 border border-slate-800 text-center">
              <div class="text-emerald-400 font-bold">Biome 3</div>
              <div class="text-[10px] text-slate-400">Croplands / Agriculture</div>
              <div class="text-amber-400 font-bold mt-1">3.03&times;</div>
            </div>
            <div class="p-2 rounded bg-slate-950/80 border border-slate-800 text-center">
              <div class="text-emerald-400 font-bold">Biome 4</div>
              <div class="text-[10px] text-slate-400">Shrublands &amp; Chaparral</div>
              <div class="text-rose-400 font-bold mt-1">3.66&times;</div>
            </div>
          </div>
        </div>

        <div class="p-3 rounded-lg bg-slate-950/50 border border-slate-800/80 text-xs text-slate-300 space-y-1">
          <span class="text-amber-300 font-semibold flex items-center gap-1 font-mono">
            <UIcon name="i-lucide-check-circle" class="w-3.5 h-3.5" />
            <span>Elimination of Degenerate Quantiles:</span>
          </span>
          <p>
            Historical implementations collapsed quantiles to static singletons (m_counts = [1, 1, 1]), inflating small counts by 23&times; to 59&times;. Our non-parametric grid inversion restores 35 continuous quantile tiers.
          </p>
        </div>
      </div>

      <!-- Card 2: Jensen's Law & FRP Power Scaling -->
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-zap" class="w-5 h-5 text-amber-400" />
            <h3 class="font-bold text-white text-base">2. Thermodynamic FRP Scaling &amp; Jensen's Law</h3>
          </div>
          <span class="text-xs font-mono text-amber-400 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">Thermodynamics</span>
        </div>

        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Fire Radiative Power (FRP, MW) scales directly with instantaneous biomass burning rate (<a href="https://doi.org/10.1029/2005jd006318" target="_blank" class="text-emerald-400 hover:underline">Wooster et al., 2005</a>). We establish a non-linear log-log power-law relationship with Baskerville logarithmic bias correction:
        </p>

        <!-- Equation Box -->
        <div class="p-3.5 rounded-lg bg-slate-950 border border-amber-500/30 text-center font-mono space-y-1">
          <div class="text-amber-300 text-sm sm:text-base font-bold">
            FRP<sub>VIIRS</sub> = exp(β<sub>b</sub>) &times; ( FRP<sub>MODIS</sub> )<sup>α<sub>b</sub></sup>
          </div>
          <div class="text-[11px] text-slate-400">
            Where power exponent α<sub>b</sub> &lt; 1.0 (sub-linear concavity due to atmospheric path absorption and sub-pixel fire geometry).
          </div>
        </div>

        <!-- Jensen Inequality Alert -->
        <div class="p-3.5 rounded-lg bg-rose-950/20 border border-rose-500/30 text-xs text-slate-300 space-y-2">
          <div class="text-rose-400 font-bold flex items-center gap-1.5 font-mono">
            <UIcon name="i-lucide-alert-triangle" class="w-4 h-4 shrink-0" />
            <span>Proof of 88.7% Radiative Energy Loss from Jensen's Inequality:</span>
          </div>
          <p class="font-mono text-[11px] text-slate-300 bg-slate-950 p-2 rounded">
            For concave f(x) where f''(x) &lt; 0: &nbsp; E[f(X)] &le; f(E[X]) &nbsp;&rArr;&nbsp; &sum; f(FRP<sub>i</sub>) &ll; f(&sum; FRP<sub>i</sub>)
          </p>
          <p>
            When power scaling is applied to monthly sums f(&sum; FRP), concavity (&alpha; &approx; 0.66–0.74) causes 88.7% of total radiative energy to be lost.
            By evaluating the non-linear Wooster function at the discrete event level: &sum; f(FRP<sub>i</sub>), FireHarmonize ensures held-out cumulative thermal energy error stays within <strong class="text-emerald-400">-0.29% to +0.32%</strong>.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  expertMode?: boolean;
}>();
</script>
