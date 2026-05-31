<template>
  <div class="nps-renderer">
    <div class="nps-labels">
      <span>{{ question.config.min_label || '完全不推荐' }}</span>
      <span>{{ question.config.max_label || '极力推荐' }}</span>
    </div>
    <div class="nps-buttons">
      <button
        v-for="n in 11"
        :key="n - 1"
        class="nps-btn"
        :class="{ active: modelValue?.value === n - 1 }"
        @click="emit('update:modelValue', { value: n - 1 })"
      >{{ n - 1 }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()
</script>

<style scoped>
.nps-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
}
.nps-buttons {
  display: flex;
  gap: 4px;
}
.nps-btn {
  width: 36px;
  height: 36px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}
.nps-btn:hover {
  border-color: #409eff;
}
.nps-btn.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}
</style>
