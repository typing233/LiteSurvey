<template>
  <div class="survey-list">
    <div class="page-header">
      <h2>问卷管理</h2>
      <el-button type="primary" @click="$router.push('/admin/surveys/new')">
        <el-icon><Plus /></el-icon>新建问卷
      </el-button>
    </div>

    <el-card shadow="never">
      <div class="filter-bar">
        <el-radio-group v-model="statusFilter" @change="loadData">
          <el-radio-button value="">全部</el-radio-button>
          <el-radio-button value="draft">草稿</el-radio-button>
          <el-radio-button value="published">已发布</el-radio-button>
          <el-radio-button value="closed">已关闭</el-radio-button>
        </el-radio-group>
      </div>

      <el-table :data="surveys" v-loading="loading" style="width: 100%">
        <el-table-column prop="title" label="问卷标题" min-width="200">
          <template #default="{ row }">
            <router-link :to="`/admin/surveys/${row.id}/edit`" class="survey-title">
              {{ row.title }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">
              {{ statusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="question_count" label="题目数" width="80" align="center" />
        <el-table-column prop="response_count" label="回收量" width="80" align="center" />
        <el-table-column prop="created_at" label="创建时间" width="170">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/admin/surveys/${row.id}/responses`)">
              数据
            </el-button>
            <el-button size="small" @click="handleDuplicate(row.id)">复制</el-button>
            <el-dropdown trigger="click" @command="(cmd: string) => handleCommand(cmd, row)">
              <el-button size="small">更多</el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-if="row.status === 'draft'" command="publish">发布</el-dropdown-item>
                  <el-dropdown-item v-if="row.status === 'published'" command="close">关闭</el-dropdown-item>
                  <el-dropdown-item v-if="row.status !== 'draft'" command="draft">设为草稿</el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <el-button
              v-if="row.status === 'published'"
              size="small"
              type="success"
              @click="copyLink(row.id)"
            >链接</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap" v-if="pagination.total > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          :page-size="pagination.page_size"
          :total="pagination.total"
          layout="total, prev, pager, next"
          @current-change="loadData"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listSurveys, deleteSurvey, updateSurveyStatus, duplicateSurvey } from '@/api/survey'
import type { SurveyListItem, Pagination } from '@/types/survey'

const surveys = ref<SurveyListItem[]>([])
const loading = ref(false)
const statusFilter = ref('')
const pagination = ref<Pagination>({ page: 1, page_size: 20, total: 0, total_pages: 0 })

function statusTagType(status: string) {
  return { draft: 'info', published: 'success', closed: 'warning' }[status] || 'info'
}

function statusLabel(status: string) {
  return { draft: '草稿', published: '已发布', closed: '已关闭' }[status] || status
}

function formatDate(str: string) {
  if (!str) return ''
  return new Date(str).toLocaleString('zh-CN')
}

async function loadData() {
  loading.value = true
  try {
    const res = await listSurveys({
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      status: statusFilter.value || undefined,
    })
    surveys.value = res.data
    if (res.pagination) pagination.value = res.pagination
  } finally {
    loading.value = false
  }
}

async function handleDuplicate(id: string) {
  await duplicateSurvey(id)
  ElMessage.success('复制成功')
  loadData()
}

async function handleCommand(cmd: string, row: SurveyListItem) {
  if (cmd === 'delete') {
    await ElMessageBox.confirm('确认删除该问卷？删除后不可恢复', '提示', { type: 'warning' })
    await deleteSurvey(row.id)
    ElMessage.success('已删除')
    loadData()
  } else if (['publish', 'close', 'draft'].includes(cmd)) {
    const statusMap: Record<string, string> = { publish: 'published', close: 'closed', draft: 'draft' }
    await updateSurveyStatus(row.id, statusMap[cmd])
    ElMessage.success('状态已更新')
    loadData()
  }
}

function copyLink(id: string) {
  const link = `${window.location.origin}/s/${id}`
  navigator.clipboard.writeText(link)
  ElMessage.success('链接已复制')
}

onMounted(loadData)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.page-header h2 {
  margin: 0;
  font-size: 20px;
}
.filter-bar {
  margin-bottom: 16px;
}
.survey-title {
  color: #409eff;
  text-decoration: none;
  font-weight: 500;
}
.survey-title:hover {
  text-decoration: underline;
}
.pagination-wrap {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
