<template>
  <div class="cascading-editor">
    <el-form label-width="80px" size="small">
      <el-form-item label="层级数">
        <el-input-number v-model="question.config.levels" :min="2" :max="5" />
      </el-form-item>
      <el-form-item label="选项数据">
        <el-input
          v-model="optionsJson"
          type="textarea"
          :rows="6"
          placeholder='[{"id":"1","label":"省份","children":[{"id":"1-1","label":"城市","children":[]}]}]'
          @blur="parseOptions"
        />
        <el-text type="info" size="small">JSON格式，支持嵌套的children结构</el-text>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question }>()
const optionsJson = ref(JSON.stringify(props.question.config.options || [], null, 2))

function parseOptions() {
  try {
    props.question.config.options = JSON.parse(optionsJson.value)
  } catch {
    ElMessage.warning('JSON格式不正确')
  }
}
</script>
