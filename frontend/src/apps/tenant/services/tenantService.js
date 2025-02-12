import http from '@/infrastructure/http/axios'

export const tenantService = {
  async getTenants(params) {
    return http.get('/tenants', { params })
  },

  async getTenantById(id) {
    return http.get(`/tenants/${id}`)
  },

  async createTenant(tenantData) {
    return http.post('/tenants', tenantData)
  },

  async updateTenant(id, tenantData) {
    return http.put(`/tenants/${id}`, tenantData)
  },

  async deleteTenant(id) {
    return http.delete(`/tenants/${id}`)
  },

  async activateTenant(id) {
    return http.post(`/tenants/${id}/activate`)
  },

  async deactivateTenant(id) {
    return http.post(`/tenants/${id}/deactivate`)
  },

  async getTenantStats(id) {
    return http.get(`/tenants/${id}/stats`)
  },

  async getTenantUsers(id, params) {
    return http.get(`/tenants/${id}/users`, { params })
  },

  async getTenantDatabases(id) {
    return http.get(`/tenants/${id}/databases`)
  },

  async createTenantDatabase(id, dbConfig) {
    return http.post(`/tenants/${id}/databases`, dbConfig)
  },

  async backupTenantDatabase(id) {
    return http.post(`/tenants/${id}/backup`)
  },

  async restoreTenantDatabase(id, backupId) {
    return http.post(`/tenants/${id}/restore/${backupId}`)
  },

  async getTenantBackups(id) {
    return http.get(`/tenants/${id}/backups`)
  },

  async getTenantLogs(id, params) {
    return http.get(`/tenants/${id}/logs`, { params })
  },

  async updateTenantConfig(id, config) {
    return http.put(`/tenants/${id}/config`, config)
  },

  async getTenantConfig(id) {
    return http.get(`/tenants/${id}/config`)
  },

  async validateDomain(domain) {
    return http.post('/tenants/validate-domain', { domain })
  }
}
