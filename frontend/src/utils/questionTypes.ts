export interface QuestionTypeInfo {
  label: string
  icon: string
  group: string
}

export const QUESTION_TYPES: Record<string, QuestionTypeInfo> = {
  single_choice:    { label: '单选', icon: 'Select', group: '选择题' },
  multiple_choice:  { label: '多选', icon: 'Finished', group: '选择题' },
  dropdown:         { label: '下拉选择', icon: 'ArrowDown', group: '选择题' },
  image_choice:     { label: '图片选择', icon: 'Picture', group: '选择题' },
  text_single:      { label: '单行填空', icon: 'Edit', group: '填空题' },
  text_multi:       { label: '多行填空', icon: 'Document', group: '填空题' },
  rating:           { label: '评分', icon: 'Star', group: '评价题' },
  nps:              { label: 'NPS评分', icon: 'TrendCharts', group: '评价题' },
  matrix_single:    { label: '矩阵单选', icon: 'Grid', group: '矩阵题' },
  matrix_multi:     { label: '矩阵多选', icon: 'Grid', group: '矩阵题' },
  matrix_rating:    { label: '矩阵评分', icon: 'Grid', group: '矩阵题' },
  date:             { label: '日期', icon: 'Calendar', group: '高级题' },
  time:             { label: '时间', icon: 'Clock', group: '高级题' },
  ranking:          { label: '排序', icon: 'Sort', group: '高级题' },
  slider:           { label: '滑块', icon: 'Minus', group: '高级题' },
  file_upload:      { label: '文件上传', icon: 'Upload', group: '高级题' },
  cascading:        { label: '级联选择', icon: 'Connection', group: '高级题' },
  phone:            { label: '手机号', icon: 'Phone', group: '联系信息' },
  email:            { label: '邮箱', icon: 'Message', group: '联系信息' },
  address:          { label: '地址', icon: 'Location', group: '联系信息' },
  statement:        { label: '描述说明', icon: 'InfoFilled', group: '其他' },
}

export const QUESTION_GROUPS = ['选择题', '填空题', '评价题', '矩阵题', '高级题', '联系信息', '其他']

export function getDefaultConfig(type: string): Record<string, any> {
  switch (type) {
    case 'single_choice':
    case 'multiple_choice':
    case 'dropdown':
      return {
        options: [
          { id: 'opt_1', label: '选项1' },
          { id: 'opt_2', label: '选项2' },
        ],
        allow_other: false,
        layout: 'vertical',
      }
    case 'image_choice':
      return {
        options: [
          { id: 'opt_1', label: '选项1', image_url: '' },
          { id: 'opt_2', label: '选项2', image_url: '' },
        ],
        multiple: false,
      }
    case 'text_single':
      return { placeholder: '请输入', max_length: 200 }
    case 'text_multi':
      return { placeholder: '请输入', max_length: 2000, rows: 4 }
    case 'rating':
      return { max_rating: 5, icon: 'star', labels: {} }
    case 'nps':
      return { min_label: '完全不推荐', max_label: '极力推荐' }
    case 'matrix_single':
    case 'matrix_multi':
    case 'matrix_rating':
      return {
        rows: [
          { id: 'row_1', label: '行1' },
          { id: 'row_2', label: '行2' },
        ],
        columns: [
          { id: 'col_1', label: '列1' },
          { id: 'col_2', label: '列2' },
          { id: 'col_3', label: '列3' },
        ],
      }
    case 'ranking':
      return {
        items: [
          { id: 'item_1', label: '选项1' },
          { id: 'item_2', label: '选项2' },
          { id: 'item_3', label: '选项3' },
        ],
      }
    case 'slider':
      return { min: 0, max: 100, step: 1, show_value: true, labels: {} }
    case 'file_upload':
      return { accept: ['.pdf', '.jpg', '.png'], max_size_mb: 10, max_files: 3 }
    case 'cascading':
      return { options: [], levels: 3 }
    case 'date':
      return { format: 'YYYY-MM-DD' }
    case 'time':
      return { format: 'HH:mm' }
    case 'phone':
      return { placeholder: '请输入手机号', region: 'CN' }
    case 'email':
      return { placeholder: '请输入邮箱' }
    case 'address':
      return { detail_level: 'district', show_detail_input: true }
    case 'statement':
      return { content: '请输入说明文字', style: 'info' }
    default:
      return {}
  }
}
