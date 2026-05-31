<template>
  <div class="matrix-editor">
    <el-form label-width="60px" size="small">
      <el-form-item label="行项目">
        <div class="items-list">
          <div v-for="(row, idx) in question.config.rows" :key="row.id" class="item-row">
            <el-input v-model="row.label" :placeholder="`行${idx+1}`" />
            <el-button text type="danger" @click="question.config.rows.splice(idx, 1)">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
          <el-button size="small" @click="addRow">添加行</el-button>
        </div>
      </el-form-item>
      <el-form-item label="列项目">
        <div class="items-list">
          <div v-for="(col, idx) in question.config.columns" :key="col.id" class="item-row">
            <el-input v-model="col.label" :placeholder="`列${idx+1}`" />
            <el-button text type="danger" @click="question.config.columns.splice(idx, 1)">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
          <el-button size="small" @click="addCol">添加列</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question }>()

function addRow() {
  const id = 'row_' + Math.random().toString(36).substring(2, 8)
  props.question.config.rows.push({ id, label: '' })
}

function addCol() {
  const id = 'col_' + Math.random().toString(36).substring(2, 8)
  props.question.config.columns.push({ id, label: '' })
}
</script>

<style scoped>
.items-list { display: flex; flex-direction: column; gap: 6px; }
.item-row { display: flex; align-items: center; gap: 6px; }
</style>
