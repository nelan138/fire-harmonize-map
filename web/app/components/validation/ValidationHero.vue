<template>
  <div class="relative overflow-hidden rounded-2xl bg-gradient-to-b from-slate-900/80 via-slate-900/50 to-slate-950/80 p-6 sm:p-8 border border-slate-800 shadow-2xl backdrop-blur-md">
    <!-- Glow Effect -->
    <div class="absolute -top-24 -left-24 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
    <div class="absolute -top-24 -right-24 w-72 h-72 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

    <div class="relative z-10 max-w-5xl mx-auto text-center space-y-4">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 text-xs font-medium text-slate-300">
        <UIcon name="i-lucide-shield-check" class="w-4 h-4 text-emerald-400" />
        <span>NASA Space Apps Challenge 2026 &bull; Earth Science & Satellite Data Harmonization</span>
      </div>

      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
        Khoa Học Hiệu Chuẩn Vật Lý &amp; <br class="hidden sm:inline" />
        <span class="bg-gradient-to-r from-emerald-400 via-teal-300 to-amber-300 bg-clip-text text-transparent">
          Khử Đứt Gãy Cảm Biến Vệ Tinh (2000–2026)
        </span>
      </h1>

      <p class="text-sm sm:text-base text-slate-400 max-w-3xl mx-auto leading-relaxed">
        Bằng chứng kiểm định độc lập về thuật toán ánh xạ phân vị <strong class="text-slate-200">Stratified EQM</strong>,
        bảo toàn năng lượng bức xạ nhiệt <strong class="text-slate-200">Wooster FRP</strong>, phá bẫy
        <strong class="text-slate-200">bất đẳng thức Jensen</strong>, và bộ kiểm định định lượng
        <strong class="text-slate-200">Chow &amp; KS Test</strong> trên 100% dữ liệu vệ tinh thật của NASA.
      </p>

      <!-- Key Metrics Counters -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 pt-4 text-left">
        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-emerald-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Dữ Liệu Sự Kiện 25 Năm</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">7,744,594</div>
          <div class="text-xs text-emerald-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-check-circle-2" class="w-3.5 h-3.5" />
            <span>100% NASA FIRMS API</span>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-teal-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Cụm Khớp Cặp Voronoi</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">220,725</div>
          <div class="text-xs text-teal-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-layers" class="w-3.5 h-3.5" />
            <span>Khử 100% đếm trùng</span>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-amber-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Kiểm Định Chow Test</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">p = 0.3667</div>
          <div class="text-xs text-amber-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-trending-up" class="w-3.5 h-3.5" />
            <span>Bác bỏ đứt gãy 2012 (&gt; 0.10)</span>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 border-l-4 border-l-rose-500 hover:border-slate-700 transition-colors">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-mono">Bảo Toàn Năng Lượng FRP</div>
          <div class="text-2xl sm:text-3xl font-extrabold text-white mt-1">&le; &plusmn;2.38%</div>
          <div class="text-xs text-rose-400 mt-1 flex items-center gap-1 font-medium">
            <UIcon name="i-lucide-zap" class="w-3.5 h-3.5" />
            <span>Đạt chuẩn an toàn &le; &plusmn;5%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>
