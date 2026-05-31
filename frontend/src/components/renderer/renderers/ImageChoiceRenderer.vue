<template>
  <div class="image-choice-renderer">
    <div class="image-grid">
      <div
        v-for="opt in question.config.options"
        :key="opt.id"
        class="image-option"
        :class="{ selected: isSelected(opt.id) }"
        @click="toggle(opt.id)"
      >
        <img v-if="opt.image_url" :src="opt.image_url" class="option-image" />
        <div v-else class="placeholder-image">
          <el-icon :size="32"><Picture /></el-icon>
        </div>
        <span class="option-label">{{ opt.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()

function isSelected(id: string) {
  return (props.modelValue?.selected || []).includes(id)
}

function toggle(id: string) {
  const current = props.modelValue?.selected || []
  if (props.question.config.multiple) {
    const next = current.includes(id) ? current.filter((x: string) => x !== id) : [...current, id]
    emit('update:modelValue', { selected: next })
  } else {
    emit('update:modelValue', { selected: [id] })
  }
}
</script>

<style scoped>
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
}
.image-option {
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
}
.image-option.selected {
  border-color: #409eff;
  background: #ecf5ff;
}
.option-image {
  width: 100%;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}
.placeholder-image {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 4px;
  color: #c0c4cc;
}
.option-label {
  display: block;
  margin-top: 8px;
  font-size: 13px;
}
</style>
