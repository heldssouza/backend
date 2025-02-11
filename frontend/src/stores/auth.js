import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token')
  }),

  getters: {
    userRole: (state) => state.user?.role || 'guest',
    userPermissions: (state) => state.user?.permissions || []
  },

  actions: {
    async login({ email, password, remember }) {
      try {
        // Simular login - substituir pela chamada real à API
        const response = await new Promise((resolve) => {
          setTimeout(() => {
            resolve({
              data: {
                token: 'fake-jwt-token',
                user: {
                  id: 1,
                  email,
                  name: 'Admin User',
                  role: 'admin',
                  permissions: ['read:all', 'write:all']
                }
              }
            })
          }, 1000)
        })

        const { token, user } = response.data
        
        this.token = token
        this.user = user
        this.isAuthenticated = true
        
        if (remember) {
          localStorage.setItem('token', token)
        }
        
        return true
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
    },

    async checkAuth() {
      if (!this.token) return false

      try {
        // Simular verificação - substituir pela chamada real à API
        const response = await new Promise((resolve) => {
          setTimeout(() => {
            resolve({
              data: {
                user: {
                  id: 1,
                  email: 'admin@example.com',
                  name: 'Admin User',
                  role: 'admin',
                  permissions: ['read:all', 'write:all']
                }
              }
            })
          }, 500)
        })

        this.user = response.data.user
        this.isAuthenticated = true
        return true
      } catch (error) {
        this.logout()
        return false
      }
    }
  }
})
