<template>
  <div class="file-upload-editor">
    <el-form label-width="100px" size="small">
      <el-form-item label="最大文件数">
        <el-input-number v-model="question.config.max_files" :min="1" :max="10" />
      </el-form-item>
      <el-form-item label="最大大小(MB)">
        <el-input-number v-model="question.config.max_size_mb" :min="1" :max="100" />
      </el-form-item>
      <el-form-item label="允许类型">
        <el-select v-model="question.config.accept" multiple size="small" style="width: 100%">
          <el-option label=".pdf" value=".pdf" />
          <el-option label=".jpg" value=".jpg" />
          <el-option label=".png" value=".png" />
          <el-option label=".doc" value=".doc" />
          <el-option label=".docx" value=".docx" />
          <el-option label=".xls" value=".xls" />
          <el-option label=".xlsx" value=".xlsx" />
        </el-select>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question }>()
</script>
