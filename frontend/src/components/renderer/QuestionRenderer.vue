<template>
  <div class="question-renderer">
    <div class="question-block">
      <div class="question-title">
        <span class="q-num">{{ question.order }}.</span>
        <span>{{ question.title }}</span>
        <span v-if="question.required" class="required">*</span>
      </div>
      <p v-if="question.description" class="question-desc">{{ question.description }}</p>
      <component
        :is="rendererComponent"
        :question="question"
        :modelValue="modelValue"
        @update:modelValue="$emit('update:modelValue', $event)"
        v-if="rendererComponent"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'
import type { Question } from '@/types/survey'

const props = defineProps<{
  question: Question
  modelValue: any
}>()

defineEmits<{ (e: 'update:modelValue', val: any): void }>()

const RENDERER_MAP: Record<string, any> = {
  single_choice: defineAsyncComponent(() => import('./renderers/ChoiceRenderer.vue')),
  multiple_choice: defineAsyncComponent(() => import('./renderers/ChoiceRenderer.vue')),
  dropdown: defineAsyncComponent(() => import('./renderers/DropdownRenderer.vue')),
  image_choice: defineAsyncComponent(() => import('./renderers/ImageChoiceRenderer.vue')),
  text_single: defineAsyncComponent(() => import('./renderers/TextRenderer.vue')),
  text_multi: defineAsyncComponent(() => import('./renderers/TextRenderer.vue')),
  rating: defineAsyncComponent(() => import('./renderers/RatingRenderer.vue')),
  nps: defineAsyncComponent(() => import('./renderers/NpsRenderer.vue')),
  matrix_single: defineAsyncComponent(() => import('./renderers/MatrixRenderer.vue')),
  matrix_multi: defineAsyncComponent(() => import('./renderers/MatrixRenderer.vue')),
  matrix_rating: defineAsyncComponent(() => import('./renderers/MatrixRenderer.vue')),
  date: defineAsyncComponent(() => import('./renderers/DateTimeRenderer.vue')),
  time: defineAsyncComponent(() => import('./renderers/DateTimeRenderer.vue')),
  ranking: defineAsyncComponent(() => import('./renderers/RankingRenderer.vue')),
  slider: defineAsyncComponent(() => import('./renderers/SliderRenderer.vue')),
  file_upload: defineAsyncComponent(() => import('./renderers/FileUploadRenderer.vue')),
  cascading: defineAsyncComponent(() => import('./renderers/CascadingRenderer.vue')),
  phone: defineAsyncComponent(() => import('./renderers/ContactRenderer.vue')),
  email: defineAsyncComponent(() => import('./renderers/ContactRenderer.vue')),
  address: defineAsyncComponent(() => import('./renderers/AddressRenderer.vue')),
  statement: defineAsyncComponent(() => import('./renderers/StatementRenderer.vue')),
}

const rendererComponent = computed(() => RENDERER_MAP[props.question.type] || null)
</script>

<style scoped>
.question-block {
  padding: 20px 0;
}
.question-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #303133;
}
.q-num {
  color: #606266;
  margin-right: 4px;
}
.required {
  color: #f56c6c;
  margin-left: 4px;
}
.question-desc {
  font-size: 13px;
  color: #909399;
  margin: 0 0 12px 0;
}
</style>
