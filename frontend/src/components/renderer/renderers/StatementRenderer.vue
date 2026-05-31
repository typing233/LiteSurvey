<template>
  <div class="statement-renderer" :class="question.config.style || 'info'">
    <p>{{ question.config.content }}</p>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question; modelValue: any }>()
</script>

<style scoped>
.statement-renderer {
  padding: 12px 16px;
  border-radius: 6px;
  font-size: 14px;
  line-height: 1.6;
}
.statement-renderer p { margin: 0; }
.info { background: #ecf5ff; color: #409eff; }
.warning { background: #fef0f0; color: #f56c6c; }
.highlight { background: #fdf6ec; color: #e6a23c; }
</style>
