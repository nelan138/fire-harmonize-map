<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">3</span>
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
            Nền Tảng Toán Học &amp; Vật Lý Khí Quyển
          </h2>
          <p class="text-xs sm:text-sm text-slate-400">
            Hàm chuyển đổi phân vị ECDF, định luật bảo toàn năng lượng Wooster FRP và nghiệm của bất đẳng thức Jensen
          </p>
        </div>
      </div>
    </div>

    <!-- Math Cards Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Card 1: Stratified EQM -->
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-binary" class="w-5 h-5 text-emerald-400" />
            <h3 class="font-bold text-white text-base">1. Ánh Xạ Phân Vị Thực Nghiệm (Stratified EQM)</h3>
          </div>
          <span class="text-xs font-mono text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">Non-Parametric</span>
        </div>

        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Thay vì nhân một hằng số chia trung bình toàn cầu (vốn làm méo mó các trận đại hỏa hoạn và phương sai lịch sử), thuật toán ánh xạ qua hàm phân phối xác suất tích lũy (ECDF) phân tầng theo 4 sinh cảnh sinh thái:
        </p>

        <!-- Equation Box -->
        <div class="p-3.5 rounded-lg bg-slate-950 border border-emerald-500/30 text-center font-mono space-y-1">
          <div class="text-emerald-300 text-sm sm:text-base font-bold">
            N̂<sub>VIIRS, b</sub> = F<sub>VIIRS, b</sub><sup>-1</sup> ( F<sub>MODIS, b</sub> ( N<sub>MODIS, b</sub> ) )
          </div>
          <div class="text-[11px] text-slate-400">
            Trong đó F<sub>MODIS, b</sub> là ECDF của MODIS trong Biome b, và F<sub>VIIRS, b</sub><sup>-1</sup> là phân vị nghịch đảo của VIIRS.
          </div>
        </div>

        <!-- 4 Biomes Table -->
        <div class="space-y-1.5 text-xs font-mono">
          <div class="text-slate-400 font-semibold mb-1">Hệ Số Phóng Đại Thực Tế Theo 4 Sinh Cảnh:</div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <div class="p-2 rounded bg-slate-950/80 border border-slate-800 text-center">
              <div class="text-emerald-400 font-bold">Biome 1</div>
              <div class="text-[10px] text-slate-400">Rừng Nhiệt Đới</div>
              <div class="text-amber-300 font-bold mt-1">2.20&times;</div>
            </div>
            <div class="p-2 rounded bg-slate-950/80 border border-slate-800 text-center">
              <div class="text-emerald-400 font-bold">Biome 2</div>
              <div class="text-[10px] text-slate-400">Savanna/Trảng Cỏ</div>
              <div class="text-amber-300 font-bold mt-1">2.43&times;</div>
            </div>
            <div class="p-2 rounded bg-slate-950/80 border border-slate-800 text-center">
              <div class="text-emerald-400 font-bold">Biome 3</div>
              <div class="text-[10px] text-slate-400">Đất Nông Nghiệp</div>
              <div class="text-coral-400 font-bold mt-1">3.03&times;</div>
            </div>
            <div class="p-2 rounded bg-slate-950/80 border border-slate-800 text-center">
              <div class="text-emerald-400 font-bold">Biome 4</div>
              <div class="text-[10px] text-slate-400">Cây Bụi Chaparral</div>
              <div class="text-rose-400 font-bold mt-1">3.66&times;</div>
            </div>
          </div>
        </div>

        <!-- Analogy Note -->
        <div class="p-3 rounded-lg bg-slate-950/50 border border-slate-800/80 text-xs text-slate-300 space-y-1">
          <span class="text-amber-300 font-semibold flex items-center gap-1">
            <UIcon name="i-lucide-lightbulb" class="w-3.5 h-3.5" />
            <span>Ẩn dụ quy đổi điểm thi đề khó vs đề dễ:</span>
          </span>
          <p>
            Giống như năm 2000 đề thi khó (MODIS), đạt 7 điểm đã lọt Top 5%; năm 2012 đề thi dễ hơn (VIIRS), muốn vào Top 5% phải đạt 9.5 điểm. EQM lấy thứ hạng phần trăm làm chuẩn, tự động quy đổi 7 điểm đề cũ thành 9.5 điểm đề mới mà không làm mất tính công bằng.
          </p>
        </div>
      </div>

      <!-- Card 2: Jensen's Law & FRP Power Scaling -->
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-zap" class="w-5 h-5 text-amber-400" />
            <h3 class="font-bold text-white text-base">2. Bảo Toàn Năng Lượng Wooster &amp; Bẫy Jensen</h3>
          </div>
          <span class="text-xs font-mono text-amber-400 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">Thermodynamics</span>
        </div>

        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Công suất bức xạ nhiệt (FRP - Megawatt) là đại lượng bảo toàn năng lượng vật lý. Xây dựng hàm tương quan log-log phi tuyến Wooster kết hợp hệ số điều chỉnh Baskerville:
        </p>

        <!-- Equation Box -->
        <div class="p-3.5 rounded-lg bg-slate-950 border border-amber-500/30 text-center font-mono space-y-1">
          <div class="text-amber-300 text-sm sm:text-base font-bold">
            FRP<sub>VIIRS</sub> = exp(β<sub>b</sub>) &times; ( FRP<sub>MODIS</sub> )<sup>α<sub>b</sub></sup>
          </div>
          <div class="text-[11px] text-slate-400">
            Với số mũ hồi quy α<sub>b</sub> &lt; 1.0 (hàm lõm vật lý do suy hao hấp thụ khí quyển và tán xạ mây).
          </div>
        </div>

        <!-- Jensen Inequality Alert -->
        <div class="p-3.5 rounded-lg bg-rose-950/20 border border-rose-500/30 text-xs text-slate-300 space-y-2">
          <div class="text-rose-400 font-bold flex items-center gap-1.5 font-mono">
            <UIcon name="i-lucide-alert-triangle" class="w-4 h-4 shrink-0" />
            <span>Khắc Phục Thất Thoát 88.7% Năng Lượng Do Bất Đẳng Thức Jensen:</span>
          </div>
          <p class="font-mono text-[11px] text-slate-300 bg-slate-950 p-2 rounded">
            ∑ f( FRP<sub>i</sub> ) &ne; f( ∑ FRP<sub>i</sub> ) &nbsp;[khi f(x) là hàm lõm α &lt; 1]
          </p>
          <p>
            Mã nguồn cũ đã cộng tổng FRP trước rồi mới scale tháng f(∑ FRP), khiến <strong class="text-white">88.7% tổng năng lượng bức xạ bị "bốc hơi"</strong>.
            FireHarmonize áp dụng hàm Wooster trực tiếp trên từng đám cháy riêng lẻ trước khi gom tháng: ∑ f(FRP<sub>i</sub>), đưa sai số bảo toàn nhiệt về mức an toàn tuyệt đối (<strong class="text-emerald-400">-0.29% đến +0.32%</strong>).
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>
