<template>
  <div class="file-upload-editor">
    <el-form label-width="100px" size="small">
      <el-form-item label="最大文件数">
        <el-input-number v-model="question.config.max_files" :min="1" :max="10" />
      </el-form-item>
      <el-form-item label="最大大小(MB)">
        <el-input-number v-model="question.config.max_size_mb" :min="1" :max="serverMaxSizeMb" />
        <el-text type="info" size="small" style="margin-left: 8px">
          服务器上限: {{ serverMaxSizeMb }}MB
        </el-text>
      </el-form-item>
      <el-form-item label="允许类型">
        <el-select v-model="question.config.accept" multiple size="small" style="width: 100%">
          <el-option label=".pdf" value=".pdf" />
          <el-option label=".jpg" value=".jpg" />
          <el-option label=".jpeg" value=".jpeg" />
          <el-option label=".png" value=".png" />
          <el-option label=".gif" value=".gif" />
          <el-option label=".webp" value=".webp" />
          <el-option label=".doc" value=".doc" />
          <el-option label=".docx" value=".docx" />
          <el-option label=".xls" value=".xls" />
          <el-option label=".xlsx" value=".xlsx" />
          <el-option label=".txt" value=".txt" />
          <el-option label=".csv" value=".csv" />
        </el-select>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import api from '@/api/index'
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question }>()

const serverMaxSizeMb = ref(10)

onMounted(async () => {
  try {
    const res = await api.get('/uploads/config') as any
    serverMaxSizeMb.value = res.data.max_size_mb
  } catch {}
})

watch(() => props.question.config.max_size_mb, (val) => {
  if (val > serverMaxSizeMb.value) {
    props.question.config.max_size_mb = serverMaxSizeMb.value
  }
})
</script>
