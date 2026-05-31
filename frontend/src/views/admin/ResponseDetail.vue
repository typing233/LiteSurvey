<template>
  <div class="response-detail" v-loading="loading">
    <div class="page-header">
      <el-button @click="$router.push(`/admin/surveys/${surveyId}/responses`)">
        <el-icon><ArrowLeft /></el-icon>返回列表
      </el-button>
      <h2>回答详情</h2>
    </div>

    <div v-if="response && survey" class="detail-content">
      <el-card shadow="never" class="meta-card">
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="提交时间">{{ formatDate(response.submitted_at) }}</el-descriptions-item>
          <el-descriptions-item label="IP地址">{{ response.metadata?.ip || '-' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card shadow="never" class="answers-card">
        <div v-for="question in survey.questions" :key="question.id" class="answer-item">
          <div class="question-label">
            <span class="q-num">Q{{ question.order }}.</span>
            {{ question.title }}
            <el-tag size="small" type="info" style="margin-left: 8px">{{ getTypeLabel(question.type) }}</el-tag>
          </div>
          <div class="answer-value">
            {{ formatAnswer(question, response.answers[question.id]) }}
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getSurvey } from '@/api/survey'
import { getResponse } from '@/api/response'
import { QUESTION_TYPES } from '@/utils/questionTypes'

const route = useRoute()
const surveyId = route.params.id as string
const responseId = route.params.rid as string
const survey = ref<any>(null)
const response = ref<any>(null)
const loading = ref(true)

function getTypeLabel(type: string) {
  return QUESTION_TYPES[type]?.label || type
}

function formatDate(str: string) {
  if (!str) return ''
  return new Date(str).toLocaleString('zh-CN')
}

function formatAnswer(question: any, answer: any): string {
  if (!answer) return '（未作答）'
  const type = question.type
  const config = question.config || {}

  if (['single_choice', 'multiple_choice', 'dropdown', 'image_choice'].includes(type)) {
    const selected = answer.selected || []
    const options = config.options || []
    const labels = selected.map((id: string) => options.find((o: any) => o.id === id)?.label || id)
    let result = labels.join(', ')
    if (answer.other_text) result += `; 其他: ${answer.other_text}`
    return result || '（未选择）'
  }
  if (['text_single', 'text_multi', 'phone', 'email'].includes(type)) {
    return answer.text || '（空）'
  }
  if (['rating', 'nps', 'slider'].includes(type)) {
    return String(answer.value ?? '（空）')
  }
  if (type === 'date' || type === 'time') {
    return answer.value || '（空）'
  }
  if (type.startsWith('matrix')) {
    const matrix = answer.matrix || {}
    const rows = config.rows || []
    const cols = config.columns || []
    return rows.map((r: any) => {
      const val = matrix[r.id]
      if (Array.isArray(val)) {
        const colLabels = val.map((cid: string) => cols.find((c: any) => c.id === cid)?.label || cid)
        return `${r.label}: ${colLabels.join(', ')}`
      }
      if (typeof val === 'number') return `${r.label}: ${val}分`
      const colLabel = cols.find((c: any) => c.id === val)?.label || val
      return `${r.label}: ${colLabel}`
    }).join(' | ')
  }
  if (type === 'ranking') {
    const items = config.items || []
    return (answer.ranked || []).map((id: string, i: number) => {
      const label = items.find((it: any) => it.id === id)?.label || id
      return `${i + 1}. ${label}`
    }).join(', ')
  }
  if (type === 'address') {
    const addr = answer.address || {}
    return [addr.province, addr.city, addr.district, addr.detail].filter(Boolean).join(' ')
  }
  if (type === 'cascading') {
    return (answer.cascading || []).join(' > ')
  }
  if (type === 'file_upload') {
    return (answer.files || []).join(', ') || '（无文件）'
  }
  if (type === 'statement') return '—'
  return JSON.stringify(answer)
}

onMounted(async () => {
  try {
    const [surveyRes, respRes] = await Promise.all([
      getSurvey(surveyId),
      getResponse(surveyId, responseId),
    ])
    survey.value = surveyRes.data
    response.value = respRes.data
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.page-header h2 {
  margin: 0;
  font-size: 18px;
}
.meta-card {
  margin-bottom: 16px;
}
.answer-item {
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}
.answer-item:last-child {
  border-bottom: none;
}
.question-label {
  font-weight: 500;
  margin-bottom: 6px;
  color: #303133;
}
.q-num {
  color: #606266;
}
.answer-value {
  color: #606266;
  padding-left: 20px;
}
</style>
