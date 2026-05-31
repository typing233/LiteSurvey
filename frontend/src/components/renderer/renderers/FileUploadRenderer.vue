<template>
  <div class="file-upload-renderer">
    <el-upload
      :action="uploadUrl"
      :limit="maxFiles"
      :accept="acceptStr"
      :before-upload="beforeUpload"
      :on-success="handleSuccess"
      :on-exceed="handleExceed"
      :on-error="handleError"
      :file-list="fileList"
      list-type="text"
    >
      <el-button size="small" type="primary">
        <el-icon><Upload /></el-icon>上传文件
      </el-button>
      <template #tip>
        <div class="el-upload__tip">
          最多{{ maxFiles }}个文件，
          单个不超过{{ maxSizeMb }}MB
          <template v-if="acceptStr">，允许类型: {{ acceptStr }}</template>
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { UploadRawFile } from 'element-plus'
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question; modelValue: any }>()
const emit = defineEmits<{ (e: 'update:modelValue', val: any): void }>()

const fileList = ref<any[]>([])

const maxFiles = computed(() => props.question.config.max_files || 3)
const maxSizeMb = computed(() => props.question.config.max_size_mb || 10)
const acceptStr = computed(() => (props.question.config.accept || []).join(','))
const uploadUrl = computed(() => `/api/v1/uploads?max_size_mb=${maxSizeMb.value}`)

function beforeUpload(file: UploadRawFile) {
  const maxBytes = maxSizeMb.value * 1024 * 1024
  if (file.size > maxBytes) {
    ElMessage.error(`文件大小不能超过${maxSizeMb.value}MB`)
    return false
  }

  const allowedExts = props.question.config.accept || []
  if (allowedExts.length > 0) {
    const ext = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!allowedExts.includes(ext)) {
      ElMessage.error(`不支持的文件类型: ${ext}，允许: ${allowedExts.join(', ')}`)
      return false
    }
  }

  return true
}

function handleSuccess(response: any) {
  const files = [...(props.modelValue?.files || [])]
  files.push(response.data.id)
  emit('update:modelValue', { files })
}

function handleExceed() {
  ElMessage.warning(`最多上传${maxFiles.value}个文件`)
}

function handleError() {
  ElMessage.error('上传失败，请重试')
}
</script>
