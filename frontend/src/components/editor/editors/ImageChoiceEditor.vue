<template>
  <div class="image-choice-editor">
    <div class="option-list">
      <div v-for="(opt, idx) in question.config.options" :key="opt.id" class="option-item">
        <el-input v-model="opt.label" placeholder="标签" size="small" style="width: 120px" />
        <el-input v-model="opt.image_url" placeholder="图片URL" size="small" />
        <el-button size="small" text type="danger" @click="removeOption(idx)">
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
    </div>
    <el-button size="small" @click="addOption">
      <el-icon><Plus /></el-icon>添加选项
    </el-button>
    <div class="extra-config">
      <el-checkbox v-model="question.config.multiple">允许多选</el-checkbox>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question }>()

function addOption() {
  const id = 'opt_' + Math.random().toString(36).substring(2, 8)
  props.question.config.options.push({ id, label: '', image_url: '' })
}

function removeOption(idx: number) {
  props.question.config.options.splice(idx, 1)
}
</script>

<style scoped>
.option-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 8px; }
.option-item { display: flex; align-items: center; gap: 8px; }
.extra-config { margin-top: 12px; }
</style>
