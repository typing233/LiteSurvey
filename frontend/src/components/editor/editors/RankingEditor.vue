<template>
  <div class="ranking-editor">
    <div class="items-list">
      <div v-for="(item, idx) in question.config.items" :key="item.id" class="item-row">
        <el-icon class="drag-icon"><Rank /></el-icon>
        <el-input v-model="item.label" :placeholder="`选项${idx+1}`" size="small" />
        <el-button size="small" text type="danger" @click="question.config.items.splice(idx, 1)">
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
    </div>
    <el-button size="small" @click="addItem">
      <el-icon><Plus /></el-icon>添加选项
    </el-button>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question }>()

function addItem() {
  const id = 'item_' + Math.random().toString(36).substring(2, 8)
  props.question.config.items.push({ id, label: '' })
}
</script>

<style scoped>
.items-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 8px; }
.item-row { display: flex; align-items: center; gap: 8px; }
.drag-icon { cursor: grab; color: #c0c4cc; }
</style>
