import http from '@/infrastructure/http/axios'

export const settingsService = {
  async getUserProfile() {
    return http.get('/settings/profile')
  },

  async updateUserProfile(profileData) {
    return http.put('/settings/profile', profileData)
  },

  async updatePassword(passwordData) {
    return http.put('/settings/password', passwordData)
  },

  async updateAvatar(formData) {
    return http.put('/settings/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  async deleteAvatar() {
    return http.delete('/settings/avatar')
  },

  async getPreferences() {
    return http.get('/settings/preferences')
  },

  async updatePreferences(preferences) {
    return http.put('/settings/preferences', preferences)
  },

  async getNotificationSettings() {
    return http.get('/settings/notifications')
  },

  async updateNotificationSettings(settings) {
    return http.put('/settings/notifications', settings)
  },

  async getTwoFactorStatus() {
    return http.get('/settings/2fa/status')
  },

  async enableTwoFactor() {
    return http.post('/settings/2fa/enable')
  },

  async disableTwoFactor(code) {
    return http.post('/settings/2fa/disable', { code })
  },

  async verifyTwoFactor(code) {
    return http.post('/settings/2fa/verify', { code })
  },

  async getBackupCodes() {
    return http.get('/settings/2fa/backup-codes')
  },

  async regenerateBackupCodes() {
    return http.post('/settings/2fa/backup-codes/regenerate')
  },

  async getActiveSessions() {
    return http.get('/settings/sessions')
  },

  async revokeSession(sessionId) {
    return http.delete(`/settings/sessions/${sessionId}`)
  },

  async revokeAllSessions() {
    return http.delete('/settings/sessions')
  },

  async getActivityLog(params) {
    return http.get('/settings/activity', { params })
  },

  async exportData() {
    return http.post('/settings/export')
  },

  async deleteAccount(password) {
    return http.post('/settings/delete-account', { password })
  }
}
