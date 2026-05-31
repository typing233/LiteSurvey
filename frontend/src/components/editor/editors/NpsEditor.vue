<template>
  <div class="nps-editor">
    <el-form label-width="100px" size="small">
      <el-form-item label="最低分标签">
        <el-input v-model="question.config.min_label" />
      </el-form-item>
      <el-form-item label="最高分标签">
        <el-input v-model="question.config.max_label" />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question }>()
</script>
