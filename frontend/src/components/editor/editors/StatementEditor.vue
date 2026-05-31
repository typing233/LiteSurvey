<template>
  <div class="statement-editor">
    <el-form label-width="80px" size="small">
      <el-form-item label="说明内容">
        <el-input v-model="question.config.content" type="textarea" :rows="3" />
      </el-form-item>
      <el-form-item label="样式">
        <el-radio-group v-model="question.config.style">
          <el-radio value="info">提示</el-radio>
          <el-radio value="warning">警告</el-radio>
          <el-radio value="highlight">高亮</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question }>()
</script>
