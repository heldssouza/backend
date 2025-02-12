import http from '@/infrastructure/http/axios'

export const metricsService = {
  async getTenantMetrics() {
    return http.get('/metrics/tenants')
  },

  async getUserMetrics() {
    return http.get('/metrics/users')
  },

  async getActivityMetrics(params) {
    return http.get('/metrics/activity', { params })
  },

  async getResourceMetrics() {
    return http.get('/metrics/resources')
  },

  async getPerformanceMetrics() {
    return http.get('/metrics/performance')
  },

  async getAuditMetrics(params) {
    return http.get('/metrics/audit', { params })
  },

  async getStorageMetrics() {
    return http.get('/metrics/storage')
  },

  async getDatabaseMetrics() {
    return http.get('/metrics/database')
  },

  async getCacheMetrics() {
    return http.get('/metrics/cache')
  },

  async getApiMetrics(params) {
    return http.get('/metrics/api', { params })
  }
}
