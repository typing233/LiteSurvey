<template>
  <div class="submit-success">
    <div class="success-card">
      <el-icon :size="64" color="#67c23a"><SuccessFilled /></el-icon>
      <h2>提交成功</h2>
      <p>感谢您的参与！您的回答已成功提交。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SuccessFilled } from '@element-plus/icons-vue'
</script>

<style scoped>
.submit-success {
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
}
.success-card {
  background: #fff;
  border-radius: 12px;
  padding: 64px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.success-card h2 {
  margin: 24px 0 8px;
  font-size: 24px;
  color: #303133;
}
.success-card p {
  color: #606266;
  font-size: 16px;
}
</style>
