<template>
  <div class="question-editor">
    <component :is="editorComponent" :question="question" v-if="editorComponent" />
    <div v-else class="no-config">
      <el-text type="info">此题型无需额外配置</el-text>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'
import type { Question } from '@/types/survey'

const props = defineProps<{ question: Question }>()

const EDITOR_MAP: Record<string, any> = {
  single_choice: defineAsyncComponent(() => import('./editors/ChoiceEditor.vue')),
  multiple_choice: defineAsyncComponent(() => import('./editors/ChoiceEditor.vue')),
  dropdown: defineAsyncComponent(() => import('./editors/ChoiceEditor.vue')),
  image_choice: defineAsyncComponent(() => import('./editors/ImageChoiceEditor.vue')),
  text_single: defineAsyncComponent(() => import('./editors/TextEditor.vue')),
  text_multi: defineAsyncComponent(() => import('./editors/TextEditor.vue')),
  rating: defineAsyncComponent(() => import('./editors/RatingEditor.vue')),
  nps: defineAsyncComponent(() => import('./editors/NpsEditor.vue')),
  matrix_single: defineAsyncComponent(() => import('./editors/MatrixEditor.vue')),
  matrix_multi: defineAsyncComponent(() => import('./editors/MatrixEditor.vue')),
  matrix_rating: defineAsyncComponent(() => import('./editors/MatrixEditor.vue')),
  ranking: defineAsyncComponent(() => import('./editors/RankingEditor.vue')),
  slider: defineAsyncComponent(() => import('./editors/SliderEditor.vue')),
  file_upload: defineAsyncComponent(() => import('./editors/FileUploadEditor.vue')),
  cascading: defineAsyncComponent(() => import('./editors/CascadingEditor.vue')),
  date: defineAsyncComponent(() => import('./editors/DateTimeEditor.vue')),
  time: defineAsyncComponent(() => import('./editors/DateTimeEditor.vue')),
  phone: defineAsyncComponent(() => import('./editors/ContactEditor.vue')),
  email: defineAsyncComponent(() => import('./editors/ContactEditor.vue')),
  address: defineAsyncComponent(() => import('./editors/AddressEditor.vue')),
  statement: defineAsyncComponent(() => import('./editors/StatementEditor.vue')),
}

const editorComponent = computed(() => EDITOR_MAP[props.question.type] || null)
</script>

<style scoped>
.no-config {
  padding: 8px 0;
}
</style>
