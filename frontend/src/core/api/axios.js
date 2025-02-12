import axios from 'axios'
import { useAuthStore } from '@/core/store/auth'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.accessToken

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore = useAuthStore()

    // Handle 401 Unauthorized
    if (error.response?.status === 401) {
      authStore.logout()
    }

    return Promise.reject(error)
  }
)

export default axiosInstance
