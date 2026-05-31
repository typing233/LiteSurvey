<template>
  <div class="datetime-editor">
    <el-form label-width="80px" size="small">
      <el-form-item label="格式">
        <el-input v-model="question.config.format" :placeholder="question.type === 'date' ? 'YYYY-MM-DD' : 'HH:mm'" />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question }>()
</script>
