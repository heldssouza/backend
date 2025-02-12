import { defineStore } from 'pinia'
import { roleService } from '../services/roleService'

export const useRoleStore = defineStore('role', {
  state: () => ({
    roles: [],
    currentRole: null,
    availablePermissions: [],
    loading: false,
    error: null,
    pagination: {
      page: 1,
      perPage: 10,
      total: 0
    },
    filters: {
      search: '',
      sortBy: 'name',
      sortOrder: 'asc'
    }
  }),

  getters: {
    getRoleById: (state) => (id) => {
      return state.roles.find(role => role.id === id)
    },

    systemRoles: (state) => {
      return state.roles.filter(role => role.type === 'system')
    },

    customRoles: (state) => {
      return state.roles.filter(role => role.type === 'custom')
    },

    totalRoles: (state) => {
      return state.pagination.total
    },

    isLoading: (state) => state.loading,

    hasError: (state) => !!state.error,

    getPermissionsByCategory: (state) => {
      if (!state.availablePermissions.length) return {}

      return state.availablePermissions.reduce((acc, permission) => {
        if (!acc[permission.category]) {
          acc[permission.category] = []
        }
        acc[permission.category].push(permission)
        return acc
      }, {})
    }
  },

  actions: {
    async fetchRoles() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          page: this.pagination.page,
          per_page: this.pagination.perPage,
          search: this.filters.search,
          sort_by: this.filters.sortBy,
          sort_order: this.filters.sortOrder
        }

        const response = await roleService.getRoles(params)
        
        this.roles = response.data.items
        this.pagination.total = response.data.total
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchRoleById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await roleService.getRoleById(id)
        this.currentRole = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async createRole(roleData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await roleService.createRole(roleData)
        this.roles.unshift(response.data)
        this.pagination.total++
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateRole(id, roleData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await roleService.updateRole(id, roleData)
        const index = this.roles.findIndex(r => r.id === id)
        if (index !== -1) {
          this.roles[index] = response.data
        }
        if (this.currentRole?.id === id) {
          this.currentRole = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteRole(id) {
      this.loading = true
      this.error = null
      
      try {
        await roleService.deleteRole(id)
        this.roles = this.roles.filter(r => r.id !== id)
        this.pagination.total--
        if (this.currentRole?.id === id) {
          this.currentRole = null
        }
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchAvailablePermissions() {
      this.loading = true
      this.error = null
      
      try {
        const response = await roleService.getAvailablePermissions()
        this.availablePermissions = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateRolePermissions(roleId, permissions) {
      this.loading = true
      this.error = null
      
      try {
        const response = await roleService.updateRolePermissions(roleId, permissions)
        if (this.currentRole?.id === roleId) {
          this.currentRole.permissions = response.data.permissions
        }
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async assignRoleToUser(roleId, userId) {
      this.loading = true
      this.error = null
      
      try {
        return await roleService.assignRoleToUser(roleId, userId)
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async removeRoleFromUser(roleId, userId) {
      this.loading = true
      this.error = null
      
      try {
        return await roleService.removeRoleFromUser(roleId, userId)
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.page = 1 // Reset to first page when filters change
    },

    setPagination(pagination) {
      this.pagination = { ...this.pagination, ...pagination }
    },

    resetState() {
      this.roles = []
      this.currentRole = null
      this.availablePermissions = []
      this.loading = false
      this.error = null
      this.pagination = {
        page: 1,
        perPage: 10,
        total: 0
      }
      this.filters = {
        search: '',
        sortBy: 'name',
        sortOrder: 'asc'
      }
    }
  }
})
