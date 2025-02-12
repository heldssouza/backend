import api from './axios'

const API_URL = '/api/v1'

export const authApi = {
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  register: async (userData) => {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  forgotPassword: async (email) => {
    const response = await api.post('/auth/forgot-password', { email })
    return response.data
  },

  resetPassword: async (token, password) => {
    const response = await api.post('/auth/reset-password', { token, password })
    return response.data
  },

  refreshToken: async () => {
    const response = await api.post('/auth/refresh-token')
    return response.data
  },

  logout: async () => {
    const response = await api.post('/auth/logout')
    return response.data
  }
}

export default authApi
