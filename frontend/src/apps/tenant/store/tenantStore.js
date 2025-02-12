import { defineStore } from 'pinia'
import { tenantService } from '../services/tenantService'

export const useTenantStore = defineStore('tenant', {
  state: () => ({
    tenants: [],
    currentTenant: null,
    loading: false,
    error: null,
    pagination: {
      page: 1,
      perPage: 10,
      total: 0
    },
    filters: {
      search: '',
      status: '',
      sortBy: 'createdAt',
      sortOrder: 'desc'
    }
  }),

  getters: {
    getTenantById: (state) => (id) => {
      return state.tenants.find(tenant => tenant.id === id)
    },
    
    activeTenants: (state) => {
      return state.tenants.filter(tenant => tenant.status === 'active')
    },

    inactiveTenants: (state) => {
      return state.tenants.filter(tenant => tenant.status === 'inactive')
    },

    totalTenants: (state) => {
      return state.pagination.total
    },

    isLoading: (state) => state.loading,

    hasError: (state) => !!state.error
  },

  actions: {
    async fetchTenants() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          page: this.pagination.page,
          per_page: this.pagination.perPage,
          search: this.filters.search,
          status: this.filters.status,
          sort_by: this.filters.sortBy,
          sort_order: this.filters.sortOrder
        }

        const response = await tenantService.getTenants(params)
        
        this.tenants = response.data.items
        this.pagination.total = response.data.total
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchTenantById(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await tenantService.getTenantById(id)
        this.currentTenant = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async createTenant(tenantData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await tenantService.createTenant(tenantData)
        this.tenants.unshift(response.data)
        this.pagination.total++
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateTenant(id, tenantData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await tenantService.updateTenant(id, tenantData)
        const index = this.tenants.findIndex(t => t.id === id)
        if (index !== -1) {
          this.tenants[index] = response.data
        }
        if (this.currentTenant?.id === id) {
          this.currentTenant = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteTenant(id) {
      this.loading = true
      this.error = null
      
      try {
        await tenantService.deleteTenant(id)
        this.tenants = this.tenants.filter(t => t.id !== id)
        this.pagination.total--
        if (this.currentTenant?.id === id) {
          this.currentTenant = null
        }
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async toggleTenantStatus(id, activate) {
      this.loading = true
      this.error = null
      
      try {
        const response = await (activate
          ? tenantService.activateTenant(id)
          : tenantService.deactivateTenant(id))
        
        const index = this.tenants.findIndex(t => t.id === id)
        if (index !== -1) {
          this.tenants[index] = response.data
        }
        if (this.currentTenant?.id === id) {
          this.currentTenant = response.data
        }
        return response.data
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
      this.tenants = []
      this.currentTenant = null
      this.loading = false
      this.error = null
      this.pagination = {
        page: 1,
        perPage: 10,
        total: 0
      }
      this.filters = {
        search: '',
        status: '',
        sortBy: 'createdAt',
        sortOrder: 'desc'
      }
    }
  }
})
