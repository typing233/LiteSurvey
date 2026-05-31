<template>
  <div class="question-toolbar">
    <el-divider content-position="center">添加题目</el-divider>
    <div class="type-groups">
      <div v-for="group in QUESTION_GROUPS" :key="group" class="type-group">
        <span class="group-label">{{ group }}</span>
        <div class="type-buttons">
          <el-button
            v-for="(info, type) in getGroupTypes(group)"
            :key="type"
            size="small"
            @click="emit('add', type)"
          >
            <el-icon><component :is="info.icon" /></el-icon>
            {{ info.label }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { QUESTION_TYPES, QUESTION_GROUPS } from '@/utils/questionTypes'
import type { QuestionTypeInfo } from '@/utils/questionTypes'

const emit = defineEmits<{ (e: 'add', type: string): void }>()

function getGroupTypes(group: string): Record<string, QuestionTypeInfo> {
  const result: Record<string, QuestionTypeInfo> = {}
  for (const [type, info] of Object.entries(QUESTION_TYPES)) {
    if (info.group === group) result[type] = info
  }
  return result
}
</script>

<style scoped>
.question-toolbar {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.type-groups {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.type-group {
  flex: 1;
  min-width: 200px;
}
.group-label {
  font-size: 12px;
  color: #909399;
  display: block;
  margin-bottom: 8px;
}
.type-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
</style>
