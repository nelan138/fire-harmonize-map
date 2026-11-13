<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">6</span>
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
            Minh Bạch Dữ Liệu &amp; Báo Cáo Nghiệm Thu Độc Lập
          </h2>
          <p class="text-xs sm:text-sm text-slate-400">
            Tải về đầy đủ báo cáo kỹ thuật định dạng PDF, bảng dữ liệu Parquet và trích dẫn khoa học chuẩn tắc
          </p>
        </div>
      </div>
    </div>

    <!-- Downloads Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- PDF Download Card -->
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-start gap-4">
        <div class="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400 shrink-0">
          <UIcon name="i-lucide-file-text" class="w-6 h-6" />
        </div>
        <div class="space-y-2 flex-1">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-white text-sm">Báo Cáo Nghiệm Thu Kỹ Thuật (PDF)</h4>
            <span class="text-[11px] font-mono text-slate-400">256 KB</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Tài liệu khoa học hoàn chỉnh biên dịch từ LaTeX (Member A), bao gồm đầy đủ phương pháp luận phân vùng Voronoi, hồi quy Wooster, chứng minh kiểm định Chow Test và các bảng số liệu 5 điểm nóng toàn cầu.
          </p>
          <div class="pt-1">
            <a
              href="/docs/validation_report_member_a.pdf"
              target="_blank"
              download
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition-colors"
            >
              <UIcon name="i-lucide-download" class="w-3.5 h-3.5" />
              <span>Tải Báo Cáo PDF</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Parquet Data Download Card -->
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-start gap-4">
        <div class="w-12 h-12 rounded-xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400 shrink-0">
          <UIcon name="i-lucide-database" class="w-6 h-6" />
        </div>
        <div class="space-y-2 flex-1">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-white text-sm">Bảng Tra Cứu Hiệu Chuẩn (Parquet)</h4>
            <span class="text-[11px] font-mono text-slate-400">5.4 KB</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Tệp Parquet chuẩn nén Zstandard gồm 396 dòng (4 biomes &times; 99 phân vị) chứa toàn bộ các hệ số ECDF không suy biến và tham số hồi quy năng lượng Wooster (&alpha;, &beta;), sẵn sàng nạp vào DuckDB.
          </p>
          <div class="pt-1">
            <a
              href="/data/calibration_lookup.parquet"
              download
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold text-xs transition-colors"
            >
              <UIcon name="i-lucide-download" class="w-3.5 h-3.5 text-teal-400" />
              <span>Tải calibration_lookup.parquet</span>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- BibTeX Citation Box -->
    <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
      <div class="flex items-center justify-between text-xs">
        <span class="font-mono text-slate-400 uppercase tracking-wider font-semibold">Trích Dẫn Học Thuật (BibTeX Citation):</span>
        <span class="text-[11px] text-emerald-400 font-mono">NASA Space Apps 2026</span>
      </div>
      <pre class="p-3 rounded-lg bg-slate-900 font-mono text-[11px] text-slate-300 overflow-x-auto leading-relaxed border border-slate-800/80"><code>@misc{fireharmonize2026,
  author = {FireHarmonize Technical Team},
  title  = {Harmonization of Historical MODIS and VIIRS Active Fire Observations (2000--2026)},
  year   = {2026},
  howpublished = {NASA Space Apps Challenge 2026 Global Project Repository},
  note   = {Bi-sensor Wooster FRP power scaling and stratified quantile mapping}
}</code></pre>
    </div>
  </div>
</template>

<script setup lang="ts"></script>
