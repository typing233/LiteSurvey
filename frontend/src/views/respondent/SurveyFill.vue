<template>
  <div class="survey-fill" v-loading="loading">
    <div class="fill-container" v-if="survey">
      <div class="survey-header">
        <h1>{{ survey.title }}</h1>
        <p v-if="survey.description">{{ survey.description }}</p>
      </div>

      <div class="questions">
        <QuestionRenderer
          v-for="question in survey.questions"
          :key="question.id"
          :question="question"
          v-model="answers[question.id]"
        />
      </div>

      <div class="submit-area">
        <el-button
          type="primary"
          size="large"
          @click="handleSubmit"
          :loading="submitting"
        >提交问卷</el-button>
      </div>
    </div>

    <div v-else-if="!loading" class="not-found">
      <el-empty description="问卷不存在或未发布" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getPublicSurvey } from '@/api/survey'
import { submitResponse } from '@/api/response'
import QuestionRenderer from '@/components/renderer/QuestionRenderer.vue'

const route = useRoute()
const router = useRouter()
const survey = ref<any>(null)
const loading = ref(true)
const submitting = ref(false)
const answers = reactive<Record<string, any>>({})

onMounted(async () => {
  try {
    const res = await getPublicSurvey(route.params.id as string)
    survey.value = res.data
  } catch {
    survey.value = null
  } finally {
    loading.value = false
  }
})

async function handleSubmit() {
  const required = survey.value?.questions?.filter((q: any) => q.required) || []
  for (const q of required) {
    if (!answers[q.id] || Object.keys(answers[q.id]).length === 0) {
      ElMessage.warning(`请完成必填题目：${q.title}`)
      return
    }
  }

  submitting.value = true
  try {
    await submitResponse(route.params.id as string, answers)
    router.push(`/s/${route.params.id}/success`)
  } catch (err: any) {
    const errors = err?.errors
    if (Array.isArray(errors)) {
      ElMessage.error(errors[0])
    } else {
      ElMessage.error(typeof err === 'string' ? err : '提交失败，请重试')
    }
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.survey-fill {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 24px 16px;
}
.fill-container {
  max-width: 720px;
  margin: 0 auto;
}
.survey-header {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.survey-header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #303133;
}
.survey-header p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}
.questions {
  background: #fff;
  border-radius: 12px;
  padding: 16px 32px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.questions > * + * {
  border-top: 1px solid #ebeef5;
}
.submit-area {
  text-align: center;
  padding: 24px 0;
}
.not-found {
  max-width: 720px;
  margin: 80px auto;
}
</style>
