<template>
  <div class="file-upload-renderer">
    <el-upload
      action="/api/v1/uploads"
      :limit="question.config.max_files || 3"
      :accept="(question.config.accept || []).join(',')"
      :on-success="handleSuccess"
      :on-exceed="handleExceed"
      :file-list="fileList"
      list-type="text"
    >
      <el-button size="small" type="primary">
        <el-icon><Upload /></el-icon>上传文件
      </el-button>
      <template #tip>
        <div class="el-upload__tip">
          最多{{ question.config.max_files || 3 }}个文件，
          单个不超过{{ question.config.max_size_mb || 10 }}MB
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()

const fileList = ref<any[]>([])

function handleSuccess(response: any) {
  const files = props.modelValue?.files || []
  files.push(response.data.id)
  emit('update:modelValue', { files })
}

function handleExceed() {
  ElMessage.warning(`最多上传${props.question.config.max_files || 3}个文件`)
}
</script>
