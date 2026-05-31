import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
})

api.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const msg = err.response?.data?.detail || err.message
    return Promise.reject(msg)
  }
)

export default api
