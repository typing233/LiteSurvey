import api from './index'
import type { Survey, SurveyListResponse } from '@/types/survey'

export function listSurveys(params: { page?: number; page_size?: number; status?: string } = {}) {
  return api.get('/surveys', { params }) as Promise<SurveyListResponse>
}

export function getSurvey(id: string) {
  return api.get(`/surveys/${id}`) as Promise<any>
}

export function createSurvey(data: Partial<Survey>) {
  return api.post('/surveys', data) as Promise<any>
}

export function updateSurvey(id: string, data: Partial<Survey>) {
  return api.put(`/surveys/${id}`, data) as Promise<any>
}

export function deleteSurvey(id: string) {
  return api.delete(`/surveys/${id}`) as Promise<any>
}

export function updateSurveyStatus(id: string, status: string) {
  return api.patch(`/surveys/${id}/status`, { status }) as Promise<any>
}

export function duplicateSurvey(id: string) {
  return api.post(`/surveys/${id}/duplicate`) as Promise<any>
}

export function getPublicSurvey(id: string) {
  return api.get(`/public/surveys/${id}`) as Promise<any>
}
