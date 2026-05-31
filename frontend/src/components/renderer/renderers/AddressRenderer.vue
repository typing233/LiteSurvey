<template>
  <div class="address-renderer">
    <div class="address-selects">
      <el-input
        :model-value="modelValue?.address?.province || ''"
        @update:model-value="updateField('province', $event)"
        placeholder="省/直辖市"
        style="width: 120px"
      />
      <el-input
        v-if="['city','district','street'].includes(question.config.detail_level)"
        :model-value="modelValue?.address?.city || ''"
        @update:model-value="updateField('city', $event)"
        placeholder="市"
        style="width: 120px"
      />
      <el-input
        v-if="['district','street'].includes(question.config.detail_level)"
        :model-value="modelValue?.address?.district || ''"
        @update:model-value="updateField('district', $event)"
        placeholder="区/县"
        style="width: 120px"
      />
    </div>
    <el-input
      v-if="question.config.show_detail_input"
      :model-value="modelValue?.address?.detail || ''"
      @update:model-value="updateField('detail', $event)"
      placeholder="详细地址"
      style="margin-top: 8px"
    />
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()

function updateField(field: string, value: string) {
  const address = { ...(props.modelValue?.address || {}), [field]: value }
  emit('update:modelValue', { address })
}
</script>

<style scoped>
.address-selects {
  display: flex;
  gap: 8px;
}
</style>
