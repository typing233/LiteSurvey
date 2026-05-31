<template>
  <div class="contact-editor">
    <el-form label-width="80px" size="small">
      <el-form-item label="占位文字">
        <el-input v-model="question.config.placeholder" />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question }>()
</script>
