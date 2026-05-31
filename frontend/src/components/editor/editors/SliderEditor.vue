<template>
  <div class="slider-editor">
    <el-form label-width="80px" size="small">
      <el-form-item label="最小值">
        <el-input-number v-model="question.config.min" />
      </el-form-item>
      <el-form-item label="最大值">
        <el-input-number v-model="question.config.max" />
      </el-form-item>
      <el-form-item label="步长">
        <el-input-number v-model="question.config.step" :min="1" />
      </el-form-item>
      <el-form-item label="显示数值">
        <el-switch v-model="question.config.show_value" />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question }>()
</script>
