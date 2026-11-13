<template>
  <div class="max-w-7xl mx-auto space-y-12 pb-16">
    <!-- 1. Hero Banner with Key Metrics -->
    <ValidationHero />

    <!-- 2. Dual-Track Audience Toggle -->
    <AudienceToggle v-model="expertMode" />

    <!-- 3. Section 1: Visual Resolution Slider (1km vs 375m) & Fracture Explanation -->
    <ResolutionSlider />

    <!-- 4. Section 2: Transparent Verification Scorecard Table -->
    <ScorecardTable />

    <!-- 5. Section 3: Mathematical & Atmospheric Physics Deep Dive -->
    <ScientificDeepDive />

    <!-- 6. Section 4: Publication Figures Gallery with Modal Lightbox -->
    <ScientificFiguresModal />

    <!-- 7. Section 5: Live Calibration Playground Sandbox -->
    <CalibrationPlayground />

    <!-- 8. Section 6: Technical Downloads & Academic Citations -->
    <DownloadSection />
  </div>
</template>

<script setup lang="ts">
import ValidationHero from '~/components/validation/ValidationHero.vue';
import AudienceToggle from '~/components/validation/AudienceToggle.vue';
import ResolutionSlider from '~/components/validation/ResolutionSlider.vue';
import ScorecardTable from '~/components/validation/ScorecardTable.vue';
import ScientificDeepDive from '~/components/validation/ScientificDeepDive.vue';
import ScientificFiguresModal from '~/components/validation/ScientificFiguresModal.vue';
import CalibrationPlayground from '~/components/validation/CalibrationPlayground.vue';
import DownloadSection from '~/components/validation/DownloadSection.vue';

const expertMode = ref(false);

useHead({
  title: 'Minh Bạch Khoa Học & Nghiệm Thu | FireHarmonize',
  meta: [
    {
      name: 'description',
      content: 'Báo cáo kiểm định độc lập và minh chứng khoa học về việc đồng nhất dữ liệu vệ tinh MODIS & VIIRS 2000-2026.'
    }
  ]
});
</script>

<style scoped></style>
