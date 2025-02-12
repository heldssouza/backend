import http from '@/infrastructure/http/axios'

export const authService = {
  async login(credentials) {
    return http.post('/auth/login', credentials)
  },

  async register(userData) {
    return http.post('/auth/register', userData)
  },

  async forgotPassword(email) {
    return http.post('/auth/forgot-password', { email })
  },

  async resetPassword(token, password) {
    return http.post('/auth/reset-password', { token, password })
  },

  async verifyEmail(token) {
    return http.post('/auth/verify-email', { token })
  },

  async refreshToken(token) {
    return http.post('/auth/refresh', { refresh_token: token })
  },

  async logout() {
    return http.post('/auth/logout')
  },

  async verify2FA(code) {
    return http.post('/auth/verify-2fa', { code })
  },

  async enable2FA() {
    return http.post('/auth/enable-2fa')
  },

  async disable2FA() {
    return http.post('/auth/disable-2fa')
  },

  async validateResetToken(token) {
    return http.post('/auth/validate-reset-token', { token })
  },

  async changePassword(currentPassword, newPassword) {
    return http.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword
    })
  },

  async getUserSessions() {
    return http.get('/auth/sessions')
  },

  async revokeSession(sessionId) {
    return http.delete(`/auth/sessions/${sessionId}`)
  },

  async revokeAllSessions() {
    return http.delete('/auth/sessions')
  }
}
