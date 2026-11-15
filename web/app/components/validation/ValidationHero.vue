<template>
  <div class="relative overflow-hidden rounded-2xl bg-gradient-to-b from-slate-900/80 via-slate-900/50 to-slate-950/80 p-6 sm:p-8 border border-slate-800 shadow-2xl backdrop-blur-md transition-all duration-300">
    <!-- Glow Effect -->
    <div class="absolute -top-24 -left-24 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
    <div class="absolute -top-24 -right-24 w-72 h-72 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

    <div class="relative z-10 max-w-5xl mx-auto text-center space-y-4">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 text-xs font-medium text-slate-300">
        <UIcon name="i-lucide-shield-check" class="w-4 h-4 text-emerald-400" />
        <span>NASA Space Apps Challenge 2026 &bull; Earth Science &amp; Satellite Sensor Harmonization</span>
      </div>

      <!-- General Track Headline -->
      <div v-if="!expertMode" class="space-y-3">
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
          One Consistent Lens for <br class="hidden sm:inline" />
          <span class="bg-gradient-to-r from-emerald-400 via-teal-300 to-amber-300 bg-clip-text text-transparent">
            25 Years of Earth's Fire History
          </span>
        </h1>
        <p class="text-sm sm:text-base text-slate-400 max-w-3xl mx-auto leading-relaxed">
          For over two decades, NASA satellites observed wildfires with two different camera lenses.
          FireHarmonize bridges the optical gap so firefighters, climate observers, and the public
          can compare past and present wildfires without being fooled by sensor technology upgrades.
        </p>
      </div>

      <!-- Scientific Deep Dive Headline -->
      <div v-else class="space-y-3">
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
          Physical Calibration Science &amp; <br class="hidden sm:inline" />
          <span class="bg-gradient-to-r from-emerald-400 via-teal-300 to-amber-300 bg-clip-text text-transparent">
            Sensor Fracture Elimination (2000–2026)
          </span>
        </h1>
        <p class="text-sm sm:text-base text-slate-400 max-w-3xl mx-auto leading-relaxed">
          Empirical validation of <strong class="text-slate-200">Stratified Empirical Quantile Mapping (EQM)</strong>,
          thermodynamic <strong class="text-slate-200">Wooster FRP Power Scaling</strong>, resolution of
          <strong class="text-slate-200">Jensen's inequality energy loss</strong>, and econometric
          <strong class="text-slate-200">Chow &amp; KS continuity tests</strong> across 100% authentic NASA FIRMS satellite observations.
        </p>
      </div>

      <!-- Key Metrics Counters: General Track -->
      <div v-if="!expertMode" class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 pt-4 text-left">
        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-emerald-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Satellite Record</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">7.7M Fires</div>
          <div class="text-xs text-emerald-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-check-circle-2" class="w-3.5 h-3.5" />
            <span>25-year complete history</span>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-teal-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Fair Comparisons</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">220K Pairs</div>
          <div class="text-xs text-teal-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-layers" class="w-3.5 h-3.5" />
            <span>Zero double-counting</span>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-amber-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Sensor Continuity</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">Zero 2012 Jump</div>
          <div class="text-xs text-amber-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-trending-up" class="w-3.5 h-3.5" />
            <span>No fake technology spike</span>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-rose-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Energy Preserved</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">98% Match</div>
          <div class="text-xs text-rose-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-zap" class="w-3.5 h-3.5" />
            <span>True fire heat preserved</span>
          </div>
        </div>
      </div>

      <!-- Key Metrics Counters: Scientific Deep Dive -->
      <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 pt-4 text-left">
        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-emerald-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">25-Yr Historical Archive</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">7,744,594</div>
          <div class="text-xs text-emerald-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-check-circle-2" class="w-3.5 h-3.5" />
            <span>100% NASA FIRMS API</span>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-teal-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Voronoi Coincident Pairs</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">220,725</div>
          <div class="text-xs text-teal-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-layers" class="w-3.5 h-3.5" />
            <span>Zero Multi-Counting</span>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-amber-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Chow Structural Test</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">p = 0.3667</div>
          <div class="text-xs text-amber-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-trending-up" class="w-3.5 h-3.5" />
            <span>No 2012 Break (p &gt; 0.10)</span>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-rose-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">FRP Energy Preservation</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">&le; &plusmn;2.38%</div>
          <div class="text-xs text-rose-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-zap" class="w-3.5 h-3.5" />
            <span>Within &le; &plusmn;5.0% threshold</span>
          </div>
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
