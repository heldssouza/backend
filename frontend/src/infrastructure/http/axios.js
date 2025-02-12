import axios from 'axios'
import { useAuthStore } from '@/core/store/auth'
import router from '@/core/router'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

http.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.accessToken

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    const tenant = localStorage.getItem('currentTenant')
    if (tenant) {
      config.headers['X-Tenant-ID'] = tenant
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

http.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore = useAuthStore()

    if (error.response?.status === 401) {
      try {
        await authStore.refreshToken()
        const originalRequest = error.config
        return http(originalRequest)
      } catch (e) {
        authStore.logout()
        router.push('/login')
        return Promise.reject(error)
      }
    }

    if (error.response?.status === 403) {
      router.push('/forbidden')
    }

    return Promise.reject(error)
  }
)

export default http
