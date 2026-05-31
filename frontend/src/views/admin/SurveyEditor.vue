<template>
  <div class="survey-editor" v-loading="store.loading">
    <div class="editor-header">
      <el-button @click="$router.push('/admin/surveys')">
        <el-icon><ArrowLeft /></el-icon>返回
      </el-button>
      <div class="header-actions">
        <el-button @click="handleSave" :loading="store.saving">保存</el-button>
        <el-button type="primary" @click="handlePublish" v-if="store.survey?.status === 'draft'">
          发布
        </el-button>
        <el-button
          v-if="store.survey?.status === 'published'"
          @click="copyLink"
          type="success"
        >复制答题链接</el-button>
      </div>
    </div>

    <div class="editor-body" v-if="store.survey">
      <div class="survey-meta">
        <el-input
          v-model="store.survey.title"
          placeholder="问卷标题"
          class="title-input"
          size="large"
        />
        <el-input
          v-model="store.survey.description"
          placeholder="问卷说明（可选）"
          type="textarea"
          :rows="2"
        />
      </div>

      <div class="question-area">
        <div class="question-list" v-if="store.survey.questions.length > 0">
          <draggable
            v-model="store.survey.questions"
            item-key="id"
            handle=".drag-handle"
            @end="store.reorder()"
          >
            <template #item="{ element, index }">
              <div
                class="question-card"
                :class="{ active: store.activeQuestionId === element.id }"
                @click="store.activeQuestionId = element.id"
              >
                <div class="question-header">
                  <el-icon class="drag-handle"><Rank /></el-icon>
                  <span class="question-num">Q{{ index + 1 }}</span>
                  <el-tag size="small" type="info">{{ getTypeLabel(element.type) }}</el-tag>
                  <el-checkbox v-model="element.required" class="required-check">必填</el-checkbox>
                  <el-button
                    size="small"
                    type="danger"
                    text
                    @click.stop="store.removeQuestion(element.id)"
                  >
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
                <el-input
                  v-model="element.title"
                  placeholder="请输入题目标题"
                  class="question-title-input"
                />
                <el-input
                  v-model="element.description"
                  placeholder="题目描述（可选）"
                  size="small"
                  class="question-desc-input"
                />
                <div class="question-config" v-if="store.activeQuestionId === element.id">
                  <QuestionEditor :question="element" />
                </div>
              </div>
            </template>
          </draggable>
        </div>

        <div class="empty-state" v-else>
          <el-empty description="暂无题目，请点击下方按钮添加" />
        </div>

        <QuestionToolbar @add="store.addQuestion" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import draggable from 'vuedraggable'
import { useSurveyStore } from '@/stores/survey'
import { updateSurveyStatus } from '@/api/survey'
import { QUESTION_TYPES } from '@/utils/questionTypes'
import QuestionEditor from '@/components/editor/QuestionEditor.vue'
import QuestionToolbar from '@/components/editor/QuestionToolbar.vue'

const route = useRoute()
const router = useRouter()
const store = useSurveyStore()

function getTypeLabel(type: string) {
  return QUESTION_TYPES[type]?.label || type
}

async function handleSave() {
  await store.save()
  ElMessage.success('保存成功')
  if (!route.params.id && store.survey?.id) {
    router.replace(`/admin/surveys/${store.survey.id}/edit`)
  }
}

async function handlePublish() {
  await store.save()
  if (store.survey?.id) {
    await updateSurveyStatus(store.survey.id, 'published')
    store.survey.status = 'published'
    ElMessage.success('问卷已发布')
  }
}

function copyLink() {
  if (!store.survey) return
  const link = `${window.location.origin}/s/${store.survey.id}`
  navigator.clipboard.writeText(link)
  ElMessage.success('答题链接已复制')
}

onMounted(() => {
  const id = route.params.id as string | undefined
  if (id) {
    store.loadSurvey(id)
  } else {
    store.initNew()
  }
})
</script>

<style scoped>
.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  background: #fff;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.header-actions {
  display: flex;
  gap: 8px;
}
.survey-meta {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.title-input {
  margin-bottom: 12px;
}
.title-input :deep(.el-input__inner) {
  font-size: 18px;
  font-weight: 600;
}
.question-card {
  background: #fff;
  border: 2px solid transparent;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: border-color 0.2s;
}
.question-card.active {
  border-color: #409eff;
}
.question-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}
.drag-handle {
  cursor: grab;
  color: #c0c4cc;
}
.question-num {
  font-weight: 600;
  color: #606266;
}
.required-check {
  margin-left: auto;
}
.question-title-input {
  margin-bottom: 8px;
}
.question-desc-input {
  margin-bottom: 8px;
}
.question-config {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
}
.empty-state {
  background: #fff;
  border-radius: 8px;
  padding: 40px;
  margin-bottom: 16px;
}
</style>
