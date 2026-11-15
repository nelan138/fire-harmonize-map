<template>
  <div class="max-w-7xl mx-auto space-y-12 pb-16">
    <!-- 1. Hero Banner with Perspective-Aware Key Metrics -->
    <ValidationHero :expert-mode="expertMode" />

    <!-- 2. Dual-Track Audience Toggle -->
    <AudienceToggle v-model="expertMode" />

    <!-- 3. Section 1: Visual Resolution Slider (1km vs 375m) & Fracture Explanation -->
    <ResolutionSlider :expert-mode="expertMode" />

    <!-- 4. Section 2: Verification Scorecard Table (General vs Scientific Track) -->
    <ScorecardTable :expert-mode="expertMode" />

    <!-- 5. Section 3: Physical & Mathematical Deep Dive -->
    <ScientificDeepDive :expert-mode="expertMode" />

    <!-- 6. Section 4: Publication Figures Gallery with Modal Lightbox -->
    <ScientificFiguresModal :expert-mode="expertMode" />

    <!-- 7. Section 5: Live Calibration Playground Sandbox -->
    <CalibrationPlayground :expert-mode="expertMode" />

    <!-- 8. Section 6: Peer-Reviewed Citations & Open Data Access -->
    <DownloadSection :expert-mode="expertMode" />
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
  title: 'Scientific Validation & Sensor Harmonization | FireHarmonize',
  meta: [
    {
      name: 'description',
      content: 'Empirical validation and rigorous physical proof of the 2000–2026 MODIS & VIIRS active fire sensor harmonization algorithm.'
    }
  ]
});
</script>

<style scoped></style>
