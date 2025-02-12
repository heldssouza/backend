import { defineStore } from 'pinia'
import http from '@/infrastructure/http/axios'
import { jwtDecode } from 'jwt-decode'
import eventBus, { EventTypes } from '@/infrastructure/events/eventBus'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('accessToken'),
    refreshToken: localStorage.getItem('refreshToken'),
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    roles: JSON.parse(localStorage.getItem('roles') || '[]'),
    permissions: JSON.parse(localStorage.getItem('permissions') || '[]')
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    userRoles: (state) => state.roles,
    userPermissions: (state) => state.permissions,
    currentUser: (state) => state.user
  },

  actions: {
    async login(credentials) {
      try {
        const response = await http.post('/auth/login', credentials)
        this.setAuthData(response.data)
        return response
      } catch (error) {
        throw error
      }
    },

    async refreshToken() {
      try {
        const response = await http.post('/auth/refresh', {
          refresh_token: this.refreshToken
        })
        this.setAuthData(response.data)
        return response
      } catch (error) {
        this.clearAuth()
        throw error
      }
    },

    setAuthData(data) {
      this.accessToken = data.access_token
      this.refreshToken = data.refresh_token
      this.user = jwtDecode(data.access_token).user
      this.roles = data.roles || []
      this.permissions = data.permissions || []

      localStorage.setItem('accessToken', data.access_token)
      localStorage.setItem('refreshToken', data.refresh_token)
      localStorage.setItem('user', JSON.stringify(this.user))
      localStorage.setItem('roles', JSON.stringify(this.roles))
      localStorage.setItem('permissions', JSON.stringify(this.permissions))
    },

    clearAuth() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      this.roles = []
      this.permissions = []

      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      localStorage.removeItem('roles')
      localStorage.removeItem('permissions')
      localStorage.removeItem('currentTenant')

      eventBus.emit(EventTypes.SESSION_EXPIRED)
    },

    async logout() {
      try {
        await http.post('/auth/logout')
      } finally {
        this.clearAuth()
      }
    },

    hasPermission(permission) {
      return this.permissions.includes(permission)
    },

    hasRole(role) {
      return this.roles.includes(role)
    }
  }
})
