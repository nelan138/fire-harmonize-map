<template>
  <div class="space-y-4">
    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">2</span>
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
            Bảng Nghiệm Thu Định Lượng Độc Lập (Audited Verification Scorecard)
          </h2>
          <p class="text-xs sm:text-sm text-slate-400">
            Kết quả kiểm thử tự động trên tập kiểm thử độc lập (Held-out Test Split 20% = 44,145 cụm thực tế)
          </p>
        </div>
      </div>
      <div class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-semibold">
        <UIcon name="i-lucide-check-circle" class="w-4 h-4" />
        <span>7/7 Tiêu Chí Nghiệm Thu ĐẠT CHUẨN</span>
      </div>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur-sm">
      <table class="w-full text-left text-xs sm:text-sm">
        <thead class="bg-slate-950/80 text-slate-400 font-mono text-xs uppercase border-b border-slate-800">
          <tr>
            <th class="px-4 py-3">Tiêu Chí Kiểm Thử</th>
            <th class="px-4 py-3">Phương Pháp Thực Hiện</th>
            <th class="px-4 py-3">Ngưỡng Chấp Nhận</th>
            <th class="px-4 py-3">Kết Quả Kiểm Định</th>
            <th class="px-4 py-3 text-center">Trạng Thái</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60 text-slate-300">
          <tr v-for="(item, idx) in criteria" :key="idx" class="hover:bg-slate-800/30 transition-colors">
            <td class="px-4 py-3 font-semibold text-white">
              <div class="flex items-center gap-2">
                <UIcon :name="item.icon" class="w-4 h-4 text-emerald-400 shrink-0" />
                <span>{{ item.name }}</span>
              </div>
            </td>
            <td class="px-4 py-3 text-slate-400 font-mono text-xs">{{ item.method }}</td>
            <td class="px-4 py-3 font-mono text-xs text-amber-300">{{ item.threshold }}</td>
            <td class="px-4 py-3 font-mono text-xs text-emerald-300 font-bold">{{ item.result }}</td>
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
        <span><strong>Kết luận thẩm định:</strong> Toàn bộ 4 sai số kỹ thuật trong phiên bản cũ (suy biến EQM, bẫy Jensen, đếm trùng multi-counting và thiếu dữ liệu) đã được khắc phục triệt để.</span>
      </div>
      <a
        href="/docs/validation_report_member_a.pdf"
        target="_blank"
        download
        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-colors shrink-0"
      >
        <UIcon name="i-lucide-file-text" class="w-4 h-4 text-emerald-400" />
        <span>Tải Báo Cáo Kỹ Thuật (PDF)</span>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
const criteria = [
  {
    name: 'Khử đếm trùng lặp (Multi-Counting)',
    icon: 'i-lucide-layers',
    method: 'Voronoi 1-to-1 qua cKDTree (Δd ≤ 1,000m)',
    threshold: 'Zero Multi-Counting',
    result: 'Triệt tiêu 100% đếm trùng lặp',
    status: 'ĐẠT XUẤT SẮC'
  },
  {
    name: 'Lọc khung giờ quan trắc đồng nhất',
    icon: 'i-lucide-clock',
    method: "Bộ lọc daynight == 'D' (Trưa 13:30 ± 30m)",
    threshold: '100% Khung giờ trưa',
    result: 'Loại bỏ hoàn toàn 15,818 điểm đêm',
    status: 'ĐẠT XUẤT SẮC'
  },
  {
    name: 'Phục hồi hàm phân vị EQM',
    icon: 'i-lucide-bar-chart-3',
    method: 'Fit ECDF trên lưới không gian 0.1°',
    threshold: 'Phân vị biến thiên thực tế',
    result: '35 mức phân vị (Hết suy biến 1.0)',
    status: 'ĐẠT XUẤT SẮC'
  },
  {
    name: 'Khắc phục Bất đẳng thức Jensen',
    icon: 'i-lucide-scale',
    method: 'Hàm scaling Wooster áp dụng cấp sự kiện',
    threshold: 'Bảo toàn năng lượng tháng',
    result: 'Phục hồi 88.7% năng lượng nhiệt',
    status: 'ĐẠT XUẤT SẮC'
  },
  {
    name: 'Bảo toàn năng lượng Rừng (Biome 1)',
    icon: 'i-lucide-trees',
    method: 'Cumulative Wooster FRP (Hold-out Test)',
    threshold: '|ΔFRP| ≤ ±5.0%',
    result: '-0.29% (Ngưỡng an toàn)',
    status: 'ĐẠT XUẤT SẮC'
  },
  {
    name: 'Bảo toàn năng lượng Savanna (Biome 2)',
    icon: 'i-lucide-wheat',
    method: 'Cumulative Wooster FRP (Hold-out Test)',
    threshold: '|ΔFRP| ≤ ±5.0%',
    result: '-2.38% (Ngưỡng an toàn)',
    status: 'ĐẠT XUẤT SẮC'
  },
  {
    name: 'Kiểm định đứt gãy Chow Test (2012)',
    icon: 'i-lucide-trending-up',
    method: 'Phân tích Structural Break tại điểm nối 2012',
    threshold: 'p-value > 0.10 (Bác bỏ đứt gãy)',
    result: 'F = 1.18, p = 0.3667',
    status: 'ĐẠT XUẤT SẮC'
  }
];
</script>
