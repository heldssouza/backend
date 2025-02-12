import http from '@/infrastructure/http/axios'

export const userService = {
  async getUsers(params) {
    return http.get('/users', { params })
  },

  async getUserById(id) {
    return http.get(`/users/${id}`)
  },

  async createUser(userData) {
    return http.post('/users', userData)
  },

  async updateUser(id, userData) {
    return http.put(`/users/${id}`, userData)
  },

  async deleteUser(id) {
    return http.delete(`/users/${id}`)
  },

  async assignRole(userId, roleId) {
    return http.post(`/users/${userId}/roles`, { role_id: roleId })
  },

  async removeRole(userId, roleId) {
    return http.delete(`/users/${userId}/roles/${roleId}`)
  },

  async getUserRoles(userId) {
    return http.get(`/users/${userId}/roles`)
  },

  async updateUserStatus(userId, status) {
    return http.patch(`/users/${userId}/status`, { status })
  },

  async resetUserPassword(userId) {
    return http.post(`/users/${userId}/reset-password`)
  },

  async force2FAEnable(userId) {
    return http.post(`/users/${userId}/force-2fa`)
  },

  async exportUsers(format = 'csv') {
    return http.get('/users/export', {
      params: { format },
      responseType: 'blob'
    })
  },

  async importUsers(file) {
    const formData = new FormData()
    formData.append('file', file)
    return http.post('/users/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}
