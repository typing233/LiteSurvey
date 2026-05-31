<template>
  <div class="choice-editor">
    <div class="option-list">
      <div v-for="(opt, idx) in question.config.options" :key="opt.id" class="option-item">
        <el-icon class="drag-icon"><Rank /></el-icon>
        <el-input v-model="opt.label" :placeholder="`选项${idx + 1}`" size="small" />
        <el-button size="small" text type="danger" @click="removeOption(idx)">
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
    </div>
    <el-button size="small" @click="addOption" class="add-btn">
      <el-icon><Plus /></el-icon>添加选项
    </el-button>
    <div class="extra-config">
      <el-checkbox v-model="question.config.allow_other">允许填写"其他"</el-checkbox>
      <el-select v-model="question.config.layout" size="small" style="width: 120px; margin-left: 16px">
        <el-option label="纵向排列" value="vertical" />
        <el-option label="横向排列" value="horizontal" />
      </el-select>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question }>()

function addOption() {
  const id = 'opt_' + Math.random().toString(36).substring(2, 8)
  props.question.config.options.push({ id, label: '' })
}

function removeOption(idx: number) {
  props.question.config.options.splice(idx, 1)
}
</script>

<style scoped>
.option-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 8px;
}
.option-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.drag-icon {
  cursor: grab;
  color: #c0c4cc;
}
.extra-config {
  margin-top: 12px;
  display: flex;
  align-items: center;
}
.add-btn {
  margin-top: 4px;
}
</style>
