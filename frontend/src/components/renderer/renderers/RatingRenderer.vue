<template>
  <div class="rating-renderer">
    <el-rate
      :model-value="modelValue?.value || 0"
      @update:model-value="emit('update:modelValue', { value: $event })"
      :max="question.config.max_rating || 5"
      :allow-half="false"
      show-score
    />
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()
</script>
