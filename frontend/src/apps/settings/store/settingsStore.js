import { defineStore } from 'pinia'
import { settingsService } from '../services/settingsService'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    profile: null,
    preferences: null,
    notificationSettings: null,
    twoFactorStatus: null,
    activeSessions: [],
    activityLog: [],
    loading: {
      profile: false,
      preferences: false,
      notifications: false,
      twoFactor: false,
      sessions: false,
      activity: false
    },
    error: null,
    activityPagination: {
      page: 1,
      perPage: 20,
      total: 0
    }
  }),

  getters: {
    isLoading: (state) => Object.values(state.loading).some(loading => loading),
    
    hasError: (state) => !!state.error,
    
    isTwoFactorEnabled: (state) => state.twoFactorStatus?.enabled || false,
    
    hasAvatar: (state) => !!state.profile?.avatar,
    
    getPreference: (state) => (key) => {
      return state.preferences?.[key]
    },

    isNotificationEnabled: (state) => (type) => {
      return state.notificationSettings?.[type]?.enabled || false
    },

    currentDeviceSession: (state) => {
      return state.activeSessions.find(session => session.current)
    },

    otherDeviceSessions: (state) => {
      return state.activeSessions.filter(session => !session.current)
    }
  },

  actions: {
    async fetchUserProfile() {
      this.loading.profile = true
      this.error = null
      
      try {
        const response = await settingsService.getUserProfile()
        this.profile = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.profile = false
      }
    },

    async updateUserProfile(profileData) {
      this.loading.profile = true
      this.error = null
      
      try {
        const response = await settingsService.updateUserProfile(profileData)
        this.profile = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.profile = false
      }
    },

    async updatePassword(passwordData) {
      this.loading.profile = true
      this.error = null
      
      try {
        await settingsService.updatePassword(passwordData)
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.profile = false
      }
    },

    async updateAvatar(formData) {
      this.loading.profile = true
      this.error = null
      
      try {
        const response = await settingsService.updateAvatar(formData)
        this.profile.avatar = response.data.avatar
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.profile = false
      }
    },

    async deleteAvatar() {
      this.loading.profile = true
      this.error = null
      
      try {
        await settingsService.deleteAvatar()
        this.profile.avatar = null
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.profile = false
      }
    },

    async fetchPreferences() {
      this.loading.preferences = true
      this.error = null
      
      try {
        const response = await settingsService.getPreferences()
        this.preferences = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.preferences = false
      }
    },

    async updatePreferences(preferences) {
      this.loading.preferences = true
      this.error = null
      
      try {
        const response = await settingsService.updatePreferences(preferences)
        this.preferences = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.preferences = false
      }
    },

    async fetchNotificationSettings() {
      this.loading.notifications = true
      this.error = null
      
      try {
        const response = await settingsService.getNotificationSettings()
        this.notificationSettings = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.notifications = false
      }
    },

    async updateNotificationSettings(settings) {
      this.loading.notifications = true
      this.error = null
      
      try {
        const response = await settingsService.updateNotificationSettings(settings)
        this.notificationSettings = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.notifications = false
      }
    },

    async fetchTwoFactorStatus() {
      this.loading.twoFactor = true
      this.error = null
      
      try {
        const response = await settingsService.getTwoFactorStatus()
        this.twoFactorStatus = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.twoFactor = false
      }
    },

    async enableTwoFactor() {
      this.loading.twoFactor = true
      this.error = null
      
      try {
        const response = await settingsService.enableTwoFactor()
        this.twoFactorStatus = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.twoFactor = false
      }
    },

    async disableTwoFactor(code) {
      this.loading.twoFactor = true
      this.error = null
      
      try {
        await settingsService.disableTwoFactor(code)
        this.twoFactorStatus.enabled = false
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.twoFactor = false
      }
    },

    async fetchActiveSessions() {
      this.loading.sessions = true
      this.error = null
      
      try {
        const response = await settingsService.getActiveSessions()
        this.activeSessions = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.sessions = false
      }
    },

    async revokeSession(sessionId) {
      this.loading.sessions = true
      this.error = null
      
      try {
        await settingsService.revokeSession(sessionId)
        this.activeSessions = this.activeSessions.filter(
          session => session.id !== sessionId
        )
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.sessions = false
      }
    },

    async revokeAllSessions() {
      this.loading.sessions = true
      this.error = null
      
      try {
        await settingsService.revokeAllSessions()
        this.activeSessions = this.activeSessions.filter(
          session => session.current
        )
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.sessions = false
      }
    },

    async fetchActivityLog() {
      this.loading.activity = true
      this.error = null
      
      try {
        const params = {
          page: this.activityPagination.page,
          per_page: this.activityPagination.perPage
        }
        const response = await settingsService.getActivityLog(params)
        this.activityLog = response.data.items
        this.activityPagination.total = response.data.total
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.activity = false
      }
    },

    setActivityPagination(pagination) {
      this.activityPagination = { ...this.activityPagination, ...pagination }
    },

    resetState() {
      this.profile = null
      this.preferences = null
      this.notificationSettings = null
      this.twoFactorStatus = null
      this.activeSessions = []
      this.activityLog = []
      this.loading = {
        profile: false,
        preferences: false,
        notifications: false,
        twoFactor: false,
        sessions: false,
        activity: false
      }
      this.error = null
      this.activityPagination = {
        page: 1,
        perPage: 20,
        total: 0
      }
    }
  }
})
