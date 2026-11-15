<template>
  <div class="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-xl bg-slate-900/50 border border-slate-800">
    <div class="flex items-center gap-3">
      <div class="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
        <UIcon :name="modelValue ? 'i-lucide-binary' : 'i-lucide-sparkles'" class="w-5 h-5" />
      </div>
      <div>
        <div class="text-sm font-semibold text-white">
          Auditing Perspective: {{ modelValue ? 'Remote Sensing Scientists & Applied Statisticians' : 'General Audience & Decision Makers' }}
        </div>
        <div class="text-xs text-slate-400">
          {{ modelValue ? 'Full mathematical formulations, thermodynamic proofs, residual distributions, and p-value hypothesis tests.' : 'Visual camera lens analogies, interactive before/after satellite imagery, and high-level verification scorecards.' }}
        </div>
      </div>
    </div>

    <!-- Toggle Buttons -->
    <div class="inline-flex p-1 rounded-lg bg-slate-950 border border-slate-800">
      <button
        type="button"
        class="px-3.5 py-1.5 rounded-md text-xs font-medium transition-all flex items-center gap-1.5 cursor-pointer"
        :class="!modelValue ? 'bg-emerald-500 text-slate-950 font-bold shadow-md' : 'text-slate-400 hover:text-white'"
        @click="$emit('update:modelValue', false)"
      >
        <UIcon name="i-lucide-eye" class="w-3.5 h-3.5" />
        <span>General Track</span>
      </button>

      <button
        type="button"
        class="px-3.5 py-1.5 rounded-md text-xs font-medium transition-all flex items-center gap-1.5 cursor-pointer"
        :class="modelValue ? 'bg-emerald-500 text-slate-950 font-bold shadow-md' : 'text-slate-400 hover:text-white'"
        @click="$emit('update:modelValue', true)"
      >
        <UIcon name="i-lucide-graduation-cap" class="w-3.5 h-3.5" />
        <span>Scientific Deep Dive</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean;
}>();

defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
}>();
</script>
