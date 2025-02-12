import { defineStore } from 'pinia'
import { metricsService } from '../services/metricsService'

export const useMetricsStore = defineStore('metrics', {
  state: () => ({
    tenantMetrics: null,
    userMetrics: null,
    activityMetrics: null,
    resourceMetrics: null,
    performanceMetrics: null,
    auditMetrics: null,
    storageMetrics: null,
    databaseMetrics: null,
    cacheMetrics: null,
    apiMetrics: null,
    loading: {
      tenants: false,
      users: false,
      activity: false,
      resources: false,
      performance: false,
      audit: false,
      storage: false,
      database: false,
      cache: false,
      api: false
    },
    error: null,
    lastUpdated: null
  }),

  getters: {
    isLoading: (state) => Object.values(state.loading).some(loading => loading),
    
    activeTenants: (state) => state.tenantMetrics?.active || 0,
    totalTenants: (state) => state.tenantMetrics?.total || 0,
    
    activeUsers: (state) => state.userMetrics?.active || 0,
    totalUsers: (state) => state.userMetrics?.total || 0,
    
    storageUsed: (state) => state.storageMetrics?.used || 0,
    storageTotal: (state) => state.storageMetrics?.total || 0,
    storagePercentage: (state) => {
      if (!state.storageMetrics) return 0
      return (state.storageMetrics.used / state.storageMetrics.total) * 100
    },

    databaseHealth: (state) => state.databaseMetrics?.health || 'unknown',
    cacheHitRate: (state) => state.cacheMetrics?.hitRate || 0,
    apiSuccessRate: (state) => state.apiMetrics?.successRate || 0
  },

  actions: {
    async fetchAllMetrics() {
      this.error = null
      
      try {
        await Promise.all([
          this.fetchTenantMetrics(),
          this.fetchUserMetrics(),
          this.fetchActivityMetrics(),
          this.fetchResourceMetrics(),
          this.fetchPerformanceMetrics(),
          this.fetchStorageMetrics(),
          this.fetchDatabaseMetrics(),
          this.fetchCacheMetrics(),
          this.fetchApiMetrics()
        ])
        
        this.lastUpdated = new Date()
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async fetchTenantMetrics() {
      this.loading.tenants = true
      try {
        const response = await metricsService.getTenantMetrics()
        this.tenantMetrics = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.tenants = false
      }
    },

    async fetchUserMetrics() {
      this.loading.users = true
      try {
        const response = await metricsService.getUserMetrics()
        this.userMetrics = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.users = false
      }
    },

    async fetchActivityMetrics(params) {
      this.loading.activity = true
      try {
        const response = await metricsService.getActivityMetrics(params)
        this.activityMetrics = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.activity = false
      }
    },

    async fetchResourceMetrics() {
      this.loading.resources = true
      try {
        const response = await metricsService.getResourceMetrics()
        this.resourceMetrics = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.resources = false
      }
    },

    async fetchPerformanceMetrics() {
      this.loading.performance = true
      try {
        const response = await metricsService.getPerformanceMetrics()
        this.performanceMetrics = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.performance = false
      }
    },

    async fetchStorageMetrics() {
      this.loading.storage = true
      try {
        const response = await metricsService.getStorageMetrics()
        this.storageMetrics = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.storage = false
      }
    },

    async fetchDatabaseMetrics() {
      this.loading.database = true
      try {
        const response = await metricsService.getDatabaseMetrics()
        this.databaseMetrics = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.database = false
      }
    },

    async fetchCacheMetrics() {
      this.loading.cache = true
      try {
        const response = await metricsService.getCacheMetrics()
        this.cacheMetrics = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.cache = false
      }
    },

    async fetchApiMetrics(params) {
      this.loading.api = true
      try {
        const response = await metricsService.getApiMetrics(params)
        this.apiMetrics = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading.api = false
      }
    },

    resetState() {
      this.tenantMetrics = null
      this.userMetrics = null
      this.activityMetrics = null
      this.resourceMetrics = null
      this.performanceMetrics = null
      this.auditMetrics = null
      this.storageMetrics = null
      this.databaseMetrics = null
      this.cacheMetrics = null
      this.apiMetrics = null
      this.loading = {
        tenants: false,
        users: false,
        activity: false,
        resources: false,
        performance: false,
        audit: false,
        storage: false,
        database: false,
        cache: false,
        api: false
      }
      this.error = null
      this.lastUpdated = null
    }
  }
})
