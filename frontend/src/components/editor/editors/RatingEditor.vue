<template>
  <div class="rating-editor">
    <el-form label-width="80px" size="small">
      <el-form-item label="最大分值">
        <el-input-number v-model="question.config.max_rating" :min="3" :max="10" />
      </el-form-item>
      <el-form-item label="图标">
        <el-radio-group v-model="question.config.icon">
          <el-radio value="star">星星</el-radio>
          <el-radio value="heart">爱心</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question }>()
</script>
