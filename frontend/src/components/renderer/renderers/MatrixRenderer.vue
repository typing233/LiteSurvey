<template>
  <div class="matrix-renderer">
    <table class="matrix-table">
      <thead>
        <tr>
          <th></th>
          <th v-for="col in question.config.columns" :key="col.id">{{ col.label }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in question.config.rows" :key="row.id">
          <td class="row-label">{{ row.label }}</td>
          <td v-for="col in question.config.columns" :key="col.id" class="cell">
            <template v-if="question.type === 'matrix_single'">
              <el-radio
                :model-value="matrixData[row.id] || ''"
                :value="col.id"
                @update:model-value="setCell(row.id, col.id)"
              >&nbsp;</el-radio>
            </template>
            <template v-else-if="question.type === 'matrix_multi'">
              <el-checkbox
                :model-value="(matrixData[row.id] || []).includes(col.id)"
                @change="toggleMulti(row.id, col.id, $event as boolean)"
              >&nbsp;</el-checkbox>
            </template>
            <template v-else>
              <el-rate
                :model-value="matrixData[row.id] || 0"
                @update:model-value="setCell(row.id, $event)"
                :max="5"
                size="small"
              />
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()

const matrixData = computed(() => props.modelValue?.matrix || {})

function setCell(rowId: string, value: any) {
  const matrix = { ...matrixData.value, [rowId]: value }
  emit('update:modelValue', { matrix })
}

function toggleMulti(rowId: string, colId: string, checked: boolean) {
  const current = matrixData.value[rowId] || []
  const next = checked ? [...current, colId] : current.filter((x: string) => x !== colId)
  setCell(rowId, next)
}
</script>

<style scoped>
.matrix-table {
  width: 100%;
  border-collapse: collapse;
}
.matrix-table th, .matrix-table td {
  padding: 8px 12px;
  text-align: center;
  border-bottom: 1px solid #ebeef5;
}
.row-label {
  text-align: left;
  font-weight: 500;
}
.cell {
  min-width: 60px;
}
</style>
