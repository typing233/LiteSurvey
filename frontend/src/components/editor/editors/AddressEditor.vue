<template>
  <div class="address-editor">
    <el-form label-width="100px" size="small">
      <el-form-item label="详细级别">
        <el-select v-model="question.config.detail_level">
          <el-option label="省" value="province" />
          <el-option label="省/市" value="city" />
          <el-option label="省/市/区" value="district" />
          <el-option label="省/市/区/街道" value="street" />
        </el-select>
      </el-form-item>
      <el-form-item label="详细地址">
        <el-switch v-model="question.config.show_detail_input" />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/survey'
defineProps<{ question: Question }>()
</script>
