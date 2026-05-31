<template>
  <div class="dropdown-renderer">
    <el-select
      :model-value="(modelValue?.selected || [])[0] || ''"
      @update:model-value="emit('update:modelValue', { selected: [$event] })"
      placeholder="请选择"
      style="width: 100%; max-width: 400px"
    >
      <el-option
        v-for="opt in question.config.options"
        :key="opt.id"
        :label="opt.label"
        :value="opt.id"
      />
    </el-select>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()
</script>
