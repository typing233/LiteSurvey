<template>
  <div class="cascading-renderer">
    <el-cascader
      :model-value="modelValue?.cascading || []"
      @update:model-value="emit('update:modelValue', { cascading: $event })"
      :options="cascaderOptions"
      :props="{ value: 'id', label: 'label', children: 'children' }"
      placeholder="请选择"
      clearable
      style="width: 100%; max-width: 400px"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()

const cascaderOptions = computed(() => props.question.config.options || [])
</script>
