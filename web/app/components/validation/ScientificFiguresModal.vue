<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">4</span>
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
            Bộ Hình Vẽ Khoa Học Độc Lập (300 DPI Publication-Grade Figures)
          </h2>
          <p class="text-xs sm:text-sm text-slate-400">
            Trích xuất trực tiếp từ 100% dữ liệu vệ tinh thật NASA FIRMS &mdash; Nhấp vào hình để phóng to toàn màn hình
          </p>
        </div>
      </div>
    </div>

    <!-- Figure Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="(fig, idx) in figures"
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
              <span>Phóng to biểu đồ</span>
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
                <span>{{ openedCaptions.includes(idx) ? 'Thu gọn hướng dẫn' : 'Hướng dẫn đọc biểu đồ' }}</span>
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
                <strong>Ý nghĩa cốt lõi:</strong> {{ fig.keyTakeaway }}
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
          <span>Chuẩn ấn phẩm khoa học 300 DPI (Matplotlib / Sci-Academic Engine)</span>
          <a
            :href="selectedFigure.src"
            target="_blank"
            download
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition-colors"
          >
            <UIcon name="i-lucide-download" class="w-4 h-4" />
            <span>Tải Ảnh Gốc (PNG)</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
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

const figures: FigureItem[] = [
  {
    tag: 'HÌNH 1',
    title: 'Bảo Toàn Năng Lượng Wooster FRP & Hồi Quy Log-Log',
    shortDesc: 'Đường cong tương quan công suất bức xạ nhiệt theo 4 Biome và bảo toàn năng lượng tích lũy.',
    src: '/visualizations/fig1_frp_scaling_energy_conservation.png',
    keyTakeaway: 'Hàm lũy thừa Wooster kết hợp tính toán cấp sự kiện giúp sai số tích lũy trên tập test chỉ còn -0.29% đến +0.32%.',
    detailedGuide: [
      { label: 'Ô (a) Trái', desc: 'Đồ thị log-log giữa MODIS FRP (1 km) và tổng VIIRS FRP (375 m). Đường nét đứt đen là tương quan thô 1:1; các đường màu là hàm fit Wooster cho từng Biome.' },
      { label: 'Ô (b) Giữa', desc: 'Độ lệch phần dư trước và sau hiệu chuẩn. Dải màu xanh ngọc hội tụ sát trục số 0, triệt tiêu sai lệch.' },
      { label: 'Ô (c) Phải', desc: 'Biểu đồ cột so sánh tổng năng lượng nhiệt tích lũy. Cột đỏ (Calibrated) khớp chuẩn xác với cột xanh đậm (True VIIRS).' }
    ]
  },
  {
    tag: 'HÌNH 2',
    title: 'Ánh Xạ Phân Vị Thực Nghiệm (EQM) & Hệ Số Phóng Đại',
    shortDesc: 'Hàm xác suất tích lũy ECDF trên lưới không gian 0.1° và phân bố hệ số phóng đại phân giải sub-pixel.',
    src: '/visualizations/fig2_count_quantile_mapping_ecdf.png',
    keyTakeaway: 'Loại bỏ hoàn toàn lỗi suy biến m_counts = [1, 1, 1], tạo ra bảng tra cứu phân vị mượt mà 35 mức giá trị.',
    detailedGuide: [
      { label: 'Ô (a) Trái', desc: 'Đường cong ECDF thực nghiệm từ 17,771 ô lưới không gian thật. Đường MODIS (vàng nét đứt) dốc đứng hơn đường VIIRS (xanh nét liền).' },
      { label: 'Ô (b) Giữa', desc: 'Hàm chuyển đổi phi tuyến EQM theo từng Biome, uốn cong theo mật độ thực tế thay vì là đường thẳng nhân hằng số.' },
      { label: 'Ô (c) Phải', desc: 'Biểu đồ tần suất số điểm VIIRS nằm trong 1 footprint MODIS (Trung vị = 3x, Trung bình = 2.96x).' }
    ]
  },
  {
    tag: 'HÌNH 3',
    title: 'Đối Soát Đứt Gãy Cảm Biến Trên 5 Điểm Nóng Toàn Cầu',
    shortDesc: 'Số điểm cháy thô vs chuỗi đồng nhất tại Amazon, California, Đông Dương, Pantanal và Đông Nam Australia.',
    src: '/visualizations/fig3_sensor_fracture_time_series.png',
    keyTakeaway: 'Chứng minh hiện tượng đứt gãy cảm biến diễn ra trên mọi châu lục và FireHarmonize quy đổi đồng nhất thành công.',
    detailedGuide: [
      { label: 'Ô (a) Trái', desc: 'Số điểm cháy ngày thực tế: MODIS thô (xám), VIIRS thô (đỏ sẫm), và Chuỗi quy đổi Calibrated (san hô).' },
      { label: 'Ô (b) Giữa', desc: 'Tổng năng lượng nhiệt bức xạ phát ra (FRP theo đơn vị 1,000 MW) tại 5 vùng chiến dịch.' },
      { label: 'Ô (c) Phải', desc: 'Phân phối chỉ số dị thường SFAI Z-Score, phân định rõ các tháng hạn hán cực đoan vượt ngưỡng +1.0σ.' }
    ]
  },
  {
    tag: 'HÌNH 4',
    title: 'Phân Bố Không Gian & Cụm Nhiệt Sub-Pixel (Tây Nguyên)',
    shortDesc: 'Nghiên cứu thực địa ca cháy ngày 15–19/03/2023: MODIS 1 km vs VIIRS 375 m vs Mật độ nhiệt tích lũy.',
    src: '/visualizations/fig4_spatial_subpixel_granularity.png',
    keyTakeaway: 'VIIRS bắt được gấp 4.60x số điểm cháy do phát hiện các đốm dọn nương rẫy nhỏ dưới tán rừng khộp.',
    detailedGuide: [
      { label: 'Ô Trái (MODIS)', desc: 'Chỉ ghi nhận các điểm ô vuông to 1 km rải rác, bỏ sót các vệt cháy nhỏ.' },
      { label: 'Ô Giữa (VIIRS)', desc: 'Ghi nhận dày đặc các cụm cháy chi tiết 375 m dọc theo các lưu vực thung lũng.' },
      { label: 'Ô Phải (Calibrated)', desc: 'Bản đồ lục giác H3 tích hợp tổng công suất bức xạ nhiệt (MW), làm lộ rõ tâm điểm bùng phát nhiệt.' }
    ]
  },
  {
    tag: 'HÌNH 5',
    title: 'Bảng Điều Khiển Tổng Hợp Kiểm Định Khoa Học (Dashboard)',
    shortDesc: 'Tổng hợp 4 trục kiểm định: Parity alignment, EQM curves, Residual distribution và Scorecard Table.',
    src: '/visualizations/fig5_comprehensive_validation_dashboard.png',
    keyTakeaway: 'Minh chứng toàn diện đáp ứng tiêu chuẩn thẩm định của tạp chí Nature Geoscience / IEEE Transactions.',
    detailedGuide: [
      { label: 'Khung (a) & (b)', desc: 'Đường phân vị ngang giá 1:1 và tập hợp các hàm chuyển đổi ECDF theo sinh cảnh.' },
      { label: 'Khung (c)', desc: 'Phân phối sai số phần dư (Residuals): Đường xanh hội tụ quanh 0% so với độ lệch rộng của chuỗi thô.' },
      { label: 'Khung (d)', desc: 'Bảng chấm điểm nghiệm thu minh bạch từng tiêu chí định lượng.' }
    ]
  }
];
</script>
