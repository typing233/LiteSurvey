<template>
  <div class="contact-renderer">
    <el-input
      :model-value="modelValue?.text || ''"
      @update:model-value="emit('update:modelValue', { text: $event })"
      :placeholder="question.config.placeholder || (question.type === 'phone' ? '请输入手机号' : '请输入邮箱')"
      :maxlength="question.type === 'phone' ? 11 : 100"
      style="max-width: 360px"
    />
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()
</script>
