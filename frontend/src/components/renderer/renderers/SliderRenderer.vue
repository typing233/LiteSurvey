<template>
  <div class="slider-renderer">
    <el-slider
      :model-value="modelValue?.value ?? question.config.min ?? 0"
      @update:model-value="emit('update:modelValue', { value: $event })"
      :min="question.config.min || 0"
      :max="question.config.max || 100"
      :step="question.config.step || 1"
      :show-tooltip="question.config.show_value !== false"
      show-input
    />
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()
</script>

<style scoped>
.slider-renderer {
  padding: 0 12px;
  max-width: 500px;
}
</style>
