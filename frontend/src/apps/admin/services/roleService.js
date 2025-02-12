import http from '@/infrastructure/http/axios'

export const roleService = {
  async getRoles(params) {
    return http.get('/roles', { params })
  },

  async getRoleById(id) {
    return http.get(`/roles/${id}`)
  },

  async createRole(roleData) {
    return http.post('/roles', roleData)
  },

  async updateRole(id, roleData) {
    return http.put(`/roles/${id}`, roleData)
  },

  async deleteRole(id) {
    return http.delete(`/roles/${id}`)
  },

  async assignRoleToUser(roleId, userId) {
    return http.post(`/roles/${roleId}/users/${userId}`)
  },

  async removeRoleFromUser(roleId, userId) {
    return http.delete(`/roles/${roleId}/users/${userId}`)
  },

  async getRoleUsers(roleId, params) {
    return http.get(`/roles/${roleId}/users`, { params })
  },

  async getRolePermissions(roleId) {
    return http.get(`/roles/${roleId}/permissions`)
  },

  async updateRolePermissions(roleId, permissions) {
    return http.put(`/roles/${roleId}/permissions`, { permissions })
  },

  async getAvailablePermissions() {
    return http.get('/permissions')
  },

  async validateRoleName(name) {
    return http.post('/roles/validate-name', { name })
  }
}
