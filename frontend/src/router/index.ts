import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/admin/surveys',
    },
    {
      path: '/admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      children: [
        { path: 'surveys', name: 'SurveyList', component: () => import('@/views/admin/SurveyList.vue') },
        { path: 'surveys/new', name: 'SurveyCreate', component: () => import('@/views/admin/SurveyEditor.vue') },
        { path: 'surveys/:id/edit', name: 'SurveyEdit', component: () => import('@/views/admin/SurveyEditor.vue') },
        { path: 'surveys/:id/responses', name: 'ResponseList', component: () => import('@/views/admin/ResponseList.vue') },
        { path: 'surveys/:id/responses/:rid', name: 'ResponseDetail', component: () => import('@/views/admin/ResponseDetail.vue') },
      ],
    },
    {
      path: '/s/:id',
      name: 'SurveyFill',
      component: () => import('@/views/respondent/SurveyFill.vue'),
    },
    {
      path: '/s/:id/success',
      name: 'SubmitSuccess',
      component: () => import('@/views/respondent/SubmitSuccess.vue'),
    },
  ],
})

export default router
