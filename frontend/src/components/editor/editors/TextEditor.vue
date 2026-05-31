<template>
  <div class="text-editor">
    <el-form label-width="80px" size="small">
      <el-form-item label="占位文字">
        <el-input v-model="question.config.placeholder" />
      </el-form-item>
      <el-form-item label="最大字数">
        <el-input-number v-model="question.config.max_length" :min="1" :max="10000" />
      </el-form-item>
      <el-form-item label="行数" v-if="question.type === 'text_multi'">
        <el-input-number v-model="question.config.rows" :min="2" :max="20" />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question }>()
</script>
