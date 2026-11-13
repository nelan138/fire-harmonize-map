<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-3 flex items-center gap-3">
      <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold font-mono">1</span>
      <div>
        <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">
          Nghịch Lý Đứt Gãy Cảm Biến Vệ Tinh 2012 (The Great Sensor Fracture)
        </h2>
        <p class="text-xs sm:text-sm text-slate-400">
          Vì sao việc đổi vệ tinh khiến số điểm cháy toàn cầu nhảy vọt gấp 4 lần nếu không có FireHarmonize?
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      <!-- Left Column: Explanation & Analogy -->
      <div class="lg:col-span-6 space-y-4 text-slate-300 text-sm leading-relaxed">
        <p>
          Vào cuối năm 2011, NASA phóng vệ tinh Suomi-NPP mang cảm biến <strong class="text-white">VIIRS</strong> để kế thừa cảm biến tiền nhiệm <strong class="text-white">MODIS</strong> (trên vệ tinh Terra &amp; Aqua). Bước nhảy vọt về quang học đã tạo ra một sự thiên lệch thị giác khổng lồ:
        </p>

        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 font-mono text-xs sm:text-sm space-y-2">
          <div class="flex items-center justify-between border-b border-slate-800 pb-2">
            <span class="text-slate-400">Cảm biến MODIS (Aqua/Terra):</span>
            <span class="text-amber-300 font-bold">1,000 m &times; 1,000 m = 1.00 km&sup2;</span>
          </div>
          <div class="flex items-center justify-between border-b border-slate-800 pb-2">
            <span class="text-slate-400">Cảm biến VIIRS (Suomi-NPP):</span>
            <span class="text-teal-300 font-bold">375 m &times; 375 m = 0.14 km&sup2;</span>
          </div>
          <div class="flex items-center justify-between text-rose-400 font-bold pt-1">
            <span>Tỷ lệ diện tích điểm ảnh:</span>
            <span>MODIS lớn gấp 7.11&times; so với VIIRS!</span>
          </div>
        </div>

        <p>
          Do điểm ảnh nhỏ hơn 7 lần kết hợp thuật toán kênh nhiệt $I_4$ ($3.74\,\mu\text{m}$) có độ nhạy vượt trội,
          VIIRS phát hiện được các đám cháy nhỏ dưới $100\,\text{m}^2$ (như dọn nương rẫy, đốt rơm rạ mùa khô) mà MODIS coi là nền đen bình thường.
        </p>

        <!-- Beginner Analogy Card -->
        <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-xs sm:text-sm space-y-2">
          <div class="font-bold text-emerald-300 flex items-center gap-2">
            <UIcon name="i-lucide-lightbulb" class="w-4 h-4 text-amber-400" />
            <span>Dành Cho Mọi Người: Ẩn Dụ Về Chiếc Điện Thoại 1 MP vs 8 MP</span>
          </div>
          <p class="text-slate-300">
            Hãy tưởng tượng bạn chụp ảnh sườn đồi bằng chiếc điện thoại cũ <strong>1 Megapixel (MODIS)</strong>, sau đó đổi sang điện thoại mới <strong>8 Megapixel (VIIRS)</strong>. Bức ảnh mới sắc nét hơn gấp 7 lần và nhìn rõ từng đốm lửa nhỏ li ti dưới tán cây.
          </p>
          <p class="text-slate-300 font-medium">
            Số đốm lửa đếm được nhảy vọt gấp 3–5 lần, nhưng <em class="text-amber-200">ngọn đồi không hề cháy nhiều hơn</em>, chỉ vì <em class="text-emerald-200">ống kính của bạn nhạy hơn</em>! FireHarmonize chế tạo "bộ quy đổi quang học" để chuỗi 25 năm liền mạch như thể được chụp bằng cùng một chiếc máy ảnh.
          </p>
        </div>
      </div>

      <!-- Right Column: Interactive Resolution Slider -->
      <div class="lg:col-span-6 space-y-3">
        <div class="flex items-center justify-between text-xs font-mono">
          <span class="flex items-center gap-1.5 text-amber-400 font-semibold">
            <UIcon name="i-lucide-eye" class="w-4 h-4" />
            <span>&larr; Kéo sang Trái: MODIS Aqua 1 km</span>
          </span>
          <span class="flex items-center gap-1.5 text-teal-400 font-semibold">
            <span>VIIRS SNPP 375 m &rarr;</span>
            <UIcon name="i-lucide-flame" class="w-4 h-4" />
          </span>
        </div>

        <div
          ref="sliderContainer"
          class="relative w-full h-[360px] sm:h-[400px] rounded-xl overflow-hidden border border-slate-700 shadow-2xl select-none cursor-ew-resize group"
          @mousedown="startDragging"
          @touchstart="startDragging"
        >
          <!-- Background Image: VIIRS (Right Side) -->
          <img
            src="/imagery/indochina_VIIRS_SNPP_2023-03-15.jpg"
            alt="VIIRS 375m Satellite View"
            class="absolute inset-0 w-full h-full object-cover pointer-events-none"
          />

          <!-- Foreground Image: MODIS (Left Side, Clipped) -->
          <div
            class="absolute inset-0 overflow-hidden pointer-events-none border-r-2 border-emerald-400 shadow-[2px_0_12px_rgba(0,0,0,0.8)]"
            :style="{ width: `${sliderPos}%` }"
          >
            <img
              src="/imagery/indochina_MODIS_Aqua_2023-03-15.jpg"
              alt="MODIS 1km Satellite View"
              class="absolute top-0 left-0 h-full max-w-none object-cover"
              :style="{ width: containerWidth ? `${containerWidth}px` : '100%' }"
            />
          </div>

          <!-- Divider Handle -->
          <div
            class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-10 h-10 rounded-full bg-emerald-400 text-slate-950 flex items-center justify-center shadow-[0_0_20px_rgba(52,211,153,0.8)] z-20 pointer-events-none group-hover:scale-110 transition-transform"
            :style="{ left: `${sliderPos}%` }"
          >
            <UIcon name="i-lucide-move-horizontal" class="w-5 h-5 font-bold" />
          </div>

          <!-- Overlay Badge Labels -->
          <div class="absolute bottom-3 left-3 z-30 px-2.5 py-1 rounded-md bg-slate-950/80 backdrop-blur-sm border border-slate-700 text-[11px] font-mono text-amber-300">
            MODIS Aqua 1 km (15/03/2023)
          </div>
          <div class="absolute bottom-3 right-3 z-30 px-2.5 py-1 rounded-md bg-slate-950/80 backdrop-blur-sm border border-slate-700 text-[11px] font-mono text-teal-300">
            VIIRS S-NPP 375 m (15/03/2023)
          </div>
        </div>

        <p class="text-xs text-slate-400 text-center italic">
          Quan trắc cùng lúc tại Tây Nguyên ngày 15/03/2023: Kéo thanh trượt để đối chiếu sự khác biệt giữa điểm ảnh 1 km và 375 m.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const sliderContainer = ref<HTMLElement | null>(null);
const sliderPos = ref(50);
const containerWidth = ref(0);
let isDragging = false;

const updateWidth = () => {
  if (sliderContainer.value) {
    containerWidth.value = sliderContainer.value.offsetWidth;
  }
};

const handleMove = (clientX: number) => {
  if (!sliderContainer.value) return;
  const rect = sliderContainer.value.getBoundingClientRect();
  const offsetX = clientX - rect.left;
  const percentage = Math.max(5, Math.min(95, (offsetX / rect.width) * 100));
  sliderPos.value = percentage;
};

const onMouseMove = (e: MouseEvent) => {
  if (!isDragging) return;
  handleMove(e.clientX);
};

const onTouchMove = (e: TouchEvent) => {
  if (!isDragging || !e.touches[0]) return;
  handleMove(e.touches[0].clientX);
};

const stopDragging = () => {
  isDragging = false;
  window.removeEventListener('mousemove', onMouseMove);
  window.removeEventListener('mouseup', stopDragging);
  window.removeEventListener('touchmove', onTouchMove);
  window.removeEventListener('touchend', stopDragging);
};

const startDragging = (e: MouseEvent | TouchEvent) => {
  isDragging = true;
  if ('touches' in e && e.touches[0]) {
    handleMove(e.touches[0].clientX);
  } else if ('clientX' in e) {
    handleMove(e.clientX);
  }
  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseup', stopDragging);
  window.addEventListener('touchmove', onTouchMove);
  window.addEventListener('touchend', stopDragging);
};

onMounted(() => {
  updateWidth();
  window.addEventListener('resize', updateWidth);
});

onUnmounted(() => {
  window.removeEventListener('resize', updateWidth);
  stopDragging();
});
</script>
