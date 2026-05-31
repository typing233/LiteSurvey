<template>
  <div class="text-renderer">
    <el-input
      v-if="question.type === 'text_single'"
      :model-value="modelValue?.text || ''"
      @update:model-value="emit('update:modelValue', { text: $event })"
      :placeholder="question.config.placeholder || '请输入'"
      :maxlength="question.config.max_length"
      show-word-limit
    />
    <el-input
      v-else
      type="textarea"
      :model-value="modelValue?.text || ''"
      @update:model-value="emit('update:modelValue', { text: $event })"
      :placeholder="question.config.placeholder || '请输入'"
      :rows="question.config.rows || 4"
      :maxlength="question.config.max_length"
      show-word-limit
    />
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()
</script>
