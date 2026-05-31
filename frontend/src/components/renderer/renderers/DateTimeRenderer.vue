<template>
  <div class="datetime-renderer">
    <el-date-picker
      v-if="question.type === 'date'"
      :model-value="modelValue?.value || ''"
      @update:model-value="emit('update:modelValue', { value: $event })"
      type="date"
      placeholder="请选择日期"
      value-format="YYYY-MM-DD"
      style="width: 240px"
    />
    <el-time-picker
      v-else
      :model-value="modelValue?.value || ''"
      @update:model-value="emit('update:modelValue', { value: $event })"
      placeholder="请选择时间"
      format="HH:mm"
      style="width: 200px"
    />
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()
</script>
