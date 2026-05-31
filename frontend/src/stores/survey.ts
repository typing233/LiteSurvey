import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Question, Survey } from '@/types/survey'
import { getSurvey, createSurvey, updateSurvey } from '@/api/survey'
import { getDefaultConfig } from '@/utils/questionTypes'

export const useSurveyStore = defineStore('survey', () => {
  const survey = ref<Survey | null>(null)
  const loading = ref(false)
  const saving = ref(false)
  const activeQuestionId = ref<string | null>(null)

  function generateId() {
    return 'q_' + Math.random().toString(36).substring(2, 10)
  }

  async function loadSurvey(id: string) {
    loading.value = true
    try {
      const res = await getSurvey(id)
      survey.value = res.data
    } finally {
      loading.value = false
    }
  }

  function initNew() {
    survey.value = {
      id: '',
      title: '未命名问卷',
      description: '',
      status: 'draft',
      settings: {},
      questions: [],
      created_at: '',
      updated_at: '',
      published_at: null,
    }
  }

  function addQuestion(type: string) {
    if (!survey.value) return
    const q: Question = {
      id: generateId(),
      type,
      title: '未命名题目',
      description: '',
      required: false,
      order: survey.value.questions.length + 1,
      config: getDefaultConfig(type),
      validation: {},
    }
    survey.value.questions.push(q)
    activeQuestionId.value = q.id
  }

  function removeQuestion(id: string) {
    if (!survey.value) return
    survey.value.questions = survey.value.questions.filter(q => q.id !== id)
    reorder()
    if (activeQuestionId.value === id) {
      activeQuestionId.value = null
    }
  }

  function reorder() {
    if (!survey.value) return
    survey.value.questions.forEach((q, i) => {
      q.order = i + 1
    })
  }

  async function save() {
    if (!survey.value) return
    saving.value = true
    try {
      if (survey.value.id) {
        const res = await updateSurvey(survey.value.id, {
          title: survey.value.title,
          description: survey.value.description,
          settings: survey.value.settings,
          questions: survey.value.questions,
        })
        survey.value = res.data
      } else {
        const res = await createSurvey({
          title: survey.value.title,
          description: survey.value.description,
          settings: survey.value.settings,
          questions: survey.value.questions,
        })
        survey.value = res.data
      }
    } finally {
      saving.value = false
    }
  }

  return {
    survey, loading, saving, activeQuestionId,
    loadSurvey, initNew, addQuestion, removeQuestion, reorder, save,
  }
})
