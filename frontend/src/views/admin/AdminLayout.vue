<template>
  <el-container class="admin-layout">
    <el-header class="admin-header">
      <div class="logo">
        <el-icon :size="24"><DataAnalysis /></el-icon>
        <span>轻问 LiteSurvey</span>
      </div>
    </el-header>
    <el-main class="admin-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { DataAnalysis } from '@element-plus/icons-vue'
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  background: #f5f7fa;
}
.admin-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #409eff;
}
.admin-main {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
