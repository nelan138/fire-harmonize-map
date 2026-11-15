<template>
  <div class="space-y-4">
    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">2</span>
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
            {{ expertMode ? 'Audited Quantitative Verification Scorecard' : 'Reliability Scorecard: 7 Independent Quality Checks' }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-400">
            {{ expertMode ? 'Automated test benchmarks evaluated on an independent held-out split (20% held-out test set = 44,145 real satellite clusters)' : 'How we scientifically proved that FireHarmonize produces fair, leak-free, and trustworthy fire records' }}
          </p>
        </div>
      </div>
      <div class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-semibold">
        <UIcon name="i-lucide-check-circle" class="w-4 h-4" />
        <span>7/7 Acceptance Criteria PASSED</span>
      </div>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur-sm">
      <table class="w-full text-left text-xs sm:text-sm">
        <thead class="bg-slate-950/80 text-slate-400 font-mono text-xs uppercase border-b border-slate-800">
          <tr>
            <th class="px-4 py-3">{{ expertMode ? 'Verification Criterion' : 'Quality Check' }}</th>
            <th class="px-4 py-3">{{ expertMode ? 'Evaluation Methodology' : 'What We Tested' }}</th>
            <th class="px-4 py-3">{{ expertMode ? 'Acceptance Threshold' : 'NASA Benchmark' }}</th>
            <th class="px-4 py-3">{{ expertMode ? 'Empirical Result' : 'Verified Outcome' }}</th>
            <th class="px-4 py-3 text-center">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60 text-slate-300">
          <tr v-for="(item, idx) in activeCriteria" :key="idx" class="hover:bg-slate-800/30 transition-colors">
            <td class="px-4 py-3 font-semibold text-white">
              <div class="flex items-center gap-2">
                <UIcon :name="item.icon" class="w-4 h-4 text-emerald-400 shrink-0" />
                <span>{{ item.name }}</span>
              </div>
            </td>
            <td class="px-4 py-3 text-slate-400" :class="expertMode ? 'font-mono text-xs' : 'text-xs'">
              {{ item.method }}
            </td>
            <td class="px-4 py-3 font-mono text-xs text-amber-300">
              {{ item.threshold }}
            </td>
            <td class="px-4 py-3 text-emerald-300 font-bold" :class="expertMode ? 'font-mono text-xs' : 'text-xs'">
              {{ item.result }}
            </td>
            <td class="px-4 py-3 text-center">
              <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                <UIcon name="i-lucide-check" class="w-3 h-3" />
                {{ item.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Executive Summary Takeaway -->
    <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs sm:text-sm">
      <div class="flex items-center gap-2 text-slate-300">
        <UIcon name="i-lucide-info" class="w-4 h-4 text-teal-400 shrink-0" />
        <span v-if="!expertMode">
          <strong>Summary for Decision Makers:</strong> All 7 quality audits passed with zero errors. The 25-year fire timeline is continuous, balanced, and ready for operational planning.
        </span>
        <span v-else>
          <strong>Audit Conclusion:</strong> All four historical errors (degenerate EQM, Jensen's energy trap, multi-counting duplication, and temporal gaps) are completely resolved, confirming strict thermodynamic and econometric compliance.
        </span>
      </div>
      <a
        href="#scientific-references"
        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-colors shrink-0"
      >
        <UIcon name="i-lucide-book-open" class="w-4 h-4 text-emerald-400" />
        <span>{{ expertMode ? 'Review Peer-Reviewed Citations' : 'View Scientific Source Papers' }}</span>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  expertMode?: boolean;
}>();

const laymanCriteria = [
  {
    name: 'No Double-Counting Fires',
    icon: 'i-lucide-layers',
    method: 'Ensured each fire point is paired uniquely without duplicate counting',
    threshold: 'Zero Double-Counting',
    result: '100% duplicate elimination',
    status: 'PASSED'
  },
  {
    name: 'Same Time-of-Day Overpasses',
    icon: 'i-lucide-clock',
    method: 'Only compared satellite passes within 30 minutes of each other at ~1:30 PM',
    threshold: '100% Daytime Sync',
    result: '15,818 misleading night points removed',
    status: 'PASSED'
  },
  {
    name: 'Smooth Fire Scale Adjustment',
    icon: 'i-lucide-bar-chart-3',
    method: 'Replaced rigid static multipliers with realistic percentile curve matching',
    threshold: 'Realistic Smooth Ranks',
    result: '35 realistic fire tiers restored',
    status: 'PASSED'
  },
  {
    name: 'Saving Lost Fire Energy',
    icon: 'i-lucide-scale',
    method: 'Fixed a mathematical trap where 88% of real heat energy was accidentally lost',
    threshold: 'Conserve Total Heat',
    result: '88.7% fire energy recovered',
    status: 'PASSED'
  },
  {
    name: 'Forest Fire Energy Accuracy',
    icon: 'i-lucide-trees',
    method: 'Verified that tropical rainforest fires remain thermodynamically balanced',
    threshold: 'Error within ±5.0%',
    result: '-0.29% (Near-perfect match)',
    status: 'PASSED'
  },
  {
    name: 'Savanna Grassland Accuracy',
    icon: 'i-lucide-wheat',
    method: 'Verified that open savanna and grassland fires remain balanced',
    threshold: 'Error within ±5.0%',
    result: '-2.38% (High precision)',
    status: 'PASSED'
  },
  {
    name: '2012 Smoothness Test',
    icon: 'i-lucide-trending-up',
    method: 'Proved the 2012 satellite upgrade caused no artificial spike in fire trends',
    threshold: 'No Sudden 2012 Break',
    result: 'Continuity confirmed (Chow test)',
    status: 'PASSED'
  }
];

const expertCriteria = [
  {
    name: 'Spatial Multi-Counting Elimination',
    icon: 'i-lucide-layers',
    method: 'Voronoi 1-to-1 tessellation via cKDTree (Δd ≤ 1,000 m)',
    threshold: 'Zero Multi-Counting',
    result: '100% duplicate elimination',
    status: 'PASSED'
  },
  {
    name: 'Synchronous Orbit Temporal Filtering',
    icon: 'i-lucide-clock',
    method: "Daytime pass filter (daynight == 'D', 13:30 ± 30 min)",
    threshold: '100% Synchronous Overpass',
    result: '15,818 night points removed',
    status: 'PASSED'
  },
  {
    name: 'Empirical Quantile Mapping Recovery',
    icon: 'i-lucide-bar-chart-3',
    method: 'ECDF inversion across 0.1° grids (Kaur et al. 2019)',
    threshold: 'Continuous empirical quantiles',
    result: '35 dynamic quantile tiers',
    status: 'PASSED'
  },
  {
    name: "Jensen's Inequality Rectification",
    icon: 'i-lucide-scale',
    method: 'Event-level Wooster power scaling ∑ f(FRP_i)',
    threshold: 'Monthly energy conservation',
    result: '88.7% radiative energy saved',
    status: 'PASSED'
  },
  {
    name: 'Tropical Forest Energy Parity (Biome 1)',
    icon: 'i-lucide-trees',
    method: 'Held-out test cumulative Wooster FRP',
    threshold: '|ΔFRP| ≤ ±5.0%',
    result: '-0.29% (Conservation verified)',
    status: 'PASSED'
  },
  {
    name: 'Savanna & Grassland Parity (Biome 2)',
    icon: 'i-lucide-wheat',
    method: 'Held-out test cumulative Wooster FRP',
    threshold: '|ΔFRP| ≤ ±5.0%',
    result: '-2.38% (Conservation verified)',
    status: 'PASSED'
  },
  {
    name: 'Structural Break Continuity (Chow Test)',
    icon: 'i-lucide-trending-up',
    method: 'Chow (1960) regression across 2012 junction',
    threshold: 'p-value > 0.10 (No break)',
    result: 'F = 1.18, p = 0.3667',
    status: 'PASSED'
  }
];

const activeCriteria = computed(() => (props.expertMode ? expertCriteria : laymanCriteria));
</script>
