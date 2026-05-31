<template>
  <div class="response-list">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="$router.push('/admin/surveys')">
          <el-icon><ArrowLeft /></el-icon>返回
        </el-button>
        <h2>{{ surveyTitle }} - 回收数据</h2>
      </div>
    </div>

    <el-row :gutter="16" class="stats-row" v-if="stats">
      <el-col :span="8">
        <el-card shadow="never">
          <el-statistic title="总回收量" :value="stats.total_responses" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <el-statistic title="今日回收" :value="stats.today_responses" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <el-statistic title="问卷状态" :value="surveyStatus" />
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never" class="table-card">
      <el-table :data="responses" v-loading="loading" style="width: 100%">
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="submitted_at" label="提交时间" width="200">
          <template #default="{ row }">
            {{ formatDate(row.submitted_at) }}
          </template>
        </el-table-column>
        <el-table-column label="IP" width="140">
          <template #default="{ row }">
            {{ row.metadata?.ip || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/admin/surveys/${surveyId}/responses/${row.id}`)">
              查看详情
            </el-button>
            <el-button size="small" type="danger" text @click="handleDelete(row.id)">删除</el-button>
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
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getSurvey } from '@/api/survey'
import { listResponses, deleteResponse, getStats } from '@/api/response'
import type { Pagination } from '@/types/survey'

const route = useRoute()
const surveyId = route.params.id as string
const surveyTitle = ref('')
const surveyStatus = ref('')
const responses = ref<any[]>([])
const stats = ref<any>(null)
const loading = ref(false)
const pagination = ref<Pagination>({ page: 1, page_size: 20, total: 0, total_pages: 0 })

function formatDate(str: string) {
  if (!str) return ''
  return new Date(str).toLocaleString('zh-CN')
}

async function loadData() {
  loading.value = true
  try {
    const res = await listResponses(surveyId, {
      page: pagination.value.page,
      page_size: pagination.value.page_size,
    })
    responses.value = res.data
    if (res.pagination) pagination.value = res.pagination
  } finally {
    loading.value = false
  }
}

async function handleDelete(responseId: string) {
  await ElMessageBox.confirm('确认删除该回答？', '提示', { type: 'warning' })
  await deleteResponse(surveyId, responseId)
  ElMessage.success('已删除')
  loadData()
}

onMounted(async () => {
  const surveyRes = await getSurvey(surveyId)
  surveyTitle.value = surveyRes.data.title
  surveyStatus.value = { draft: '草稿', published: '已发布', closed: '已关闭' }[surveyRes.data.status as string] || ''
  const statsRes = await getStats(surveyId)
  stats.value = statsRes.data
  loadData()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.header-left h2 {
  margin: 0;
  font-size: 18px;
}
.stats-row {
  margin-bottom: 16px;
}
.table-card {
  margin-top: 0;
}
.pagination-wrap {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
