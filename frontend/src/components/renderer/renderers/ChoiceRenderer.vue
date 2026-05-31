<template>
  <div class="choice-renderer">
    <template v-if="question.type === 'single_choice'">
      <el-radio-group
        :model-value="(modelValue?.selected || [])[0] || ''"
        @update:model-value="emit('update:modelValue', { selected: [$event] })"
        :class="{ horizontal: question.config.layout === 'horizontal' }"
      >
        <el-radio
          v-for="opt in question.config.options"
          :key="opt.id"
          :value="opt.id"
        >{{ opt.label }}</el-radio>
      </el-radio-group>
    </template>
    <template v-else>
      <el-checkbox-group
        :model-value="modelValue?.selected || []"
        @update:model-value="emit('update:modelValue', { selected: $event })"
        :class="{ horizontal: question.config.layout === 'horizontal' }"
      >
        <el-checkbox
          v-for="opt in question.config.options"
          :key="opt.id"
          :value="opt.id"
          :label="opt.label"
        />
      </el-checkbox-group>
    </template>
    <div v-if="question.config.allow_other" class="other-input">
      <el-input
        v-model="otherText"
        placeholder="其他..."
        size="small"
        @input="updateOther"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()

const otherText = ref(props.modelValue?.other_text || '')

function updateOther() {
  emit('update:modelValue', {
    ...props.modelValue,
    other_text: otherText.value,
  })
}
</script>

<style scoped>
.horizontal :deep(.el-radio), .horizontal :deep(.el-checkbox) {
  margin-right: 16px;
}
.other-input {
  margin-top: 8px;
  max-width: 300px;
}
</style>
