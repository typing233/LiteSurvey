export interface Question {
  id: string
  type: string
  title: string
  description: string
  required: boolean
  order: number
  config: Record<string, any>
  validation: Record<string, any>
}

export interface Survey {
  id: string
  title: string
  description: string
  status: 'draft' | 'published' | 'closed'
  settings: Record<string, any>
  questions: Question[]
  created_at: string
  updated_at: string
  published_at: string | null
}

export interface SurveyListItem {
  id: string
  title: string
  description: string
  status: string
  question_count: number
  response_count: number
  created_at: string
  updated_at: string
  published_at: string | null
}

export interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

export interface SurveyListResponse {
  code: number
  message: string
  data: SurveyListItem[]
  pagination: Pagination
}
