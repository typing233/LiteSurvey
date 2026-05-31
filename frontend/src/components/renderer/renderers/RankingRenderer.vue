<template>
  <div class="ranking-renderer">
    <p class="hint">拖拽排序（从上到下为优先级由高到低）</p>
    <draggable v-model="items" item-key="id" @end="emitValue" class="ranking-list">
      <template #item="{ element, index }">
        <div class="ranking-item">
          <span class="rank-num">{{ index + 1 }}</span>
          <el-icon class="drag-icon"><Rank /></el-icon>
          <span>{{ element.label }}</span>
        </div>
      </template>
    </draggable>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import draggable from 'vuedraggable'
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()

const items = ref<Array<{ id: string; label: string }>>([])

onMounted(() => {
  const ranked = props.modelValue?.ranked || []
  const allItems = props.question.config.items || []
  if (ranked.length > 0) {
    items.value = ranked.map((id: string) => allItems.find((it: any) => it.id === id) || { id, label: id })
  } else {
    items.value = [...allItems]
  }
  emitValue()
})

function emitValue() {
  emit('update:modelValue', { ranked: items.value.map(i => i.id) })
}
</script>

<style scoped>
.hint {
  font-size: 12px;
  color: #909399;
  margin: 0 0 8px 0;
}
.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.ranking-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: #f5f7fa;
  border-radius: 6px;
  cursor: grab;
}
.rank-num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #409eff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}
.drag-icon {
  color: #c0c4cc;
}
</style>
