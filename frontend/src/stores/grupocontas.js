import { defineStore } from 'pinia'
import axios from '@/plugins/axios'

export const useGrupoContasStore = defineStore('grupocontas', {
  state: () => ({
    grupoContas: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchGrupoContas() {
      this.loading = true
      try {
        const response = await axios.get('/api/grupocontas')
        this.grupoContas = response.data
        this.error = null
      } catch (err) {
        this.error = err.message || 'Erro ao carregar grupos de contas'
        console.error('Erro ao carregar grupos de contas:', err.response?.data || err.message)
      } finally {
        this.loading = false
      }
    },

    async createGrupoConta(grupoConta) {
      this.loading = true
      try {
        const response = await axios.post('/api/grupocontas', grupoConta)
        this.grupoContas.push(response.data)
        this.error = null
        return response.data
      } catch (err) {
        this.error = err.message || 'Erro ao criar grupo de contas'
        console.error('Erro ao criar grupo de contas:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateGrupoConta(id, grupoConta) {
      this.loading = true
      try {
        const response = await axios.put(`/api/grupocontas/${id}`, grupoConta)
        const index = this.grupoContas.findIndex(g => g.id === id)
        if (index !== -1) {
          this.grupoContas[index] = response.data
        }
        this.error = null
        return response.data
      } catch (err) {
        this.error = err.message || 'Erro ao atualizar grupo de contas'
        console.error('Erro ao atualizar grupo de contas:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteGrupoConta(id) {
      this.loading = true
      try {
        await axios.delete(`/api/grupocontas/${id}`)
        this.grupoContas = this.grupoContas.filter(g => g.id !== id)
        this.error = null
      } catch (err) {
        this.error = err.message || 'Erro ao excluir grupo de contas'
        console.error('Erro ao excluir grupo de contas:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
