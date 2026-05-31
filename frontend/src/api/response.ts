import api from './index'

export function submitResponse(surveyId: string, answers: Record<string, any>) {
  return api.post(`/public/surveys/${surveyId}/responses`, { answers }) as Promise<any>
}

export function listResponses(surveyId: string, params: { page?: number; page_size?: number } = {}) {
  return api.get(`/surveys/${surveyId}/responses`, { params }) as Promise<any>
}

export function getResponse(surveyId: string, responseId: string) {
  return api.get(`/surveys/${surveyId}/responses/${responseId}`) as Promise<any>
}

export function deleteResponse(surveyId: string, responseId: string) {
  return api.delete(`/surveys/${surveyId}/responses/${responseId}`) as Promise<any>
}

export function getStats(surveyId: string) {
  return api.get(`/surveys/${surveyId}/stats`) as Promise<any>
}
