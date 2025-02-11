import { defineStore } from 'pinia'
import axios from '@/plugins/axios'

export const useContasStore = defineStore('contas', {
  state: () => ({
    contas: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchContas() {
      this.loading = true
      try {
        const response = await axios.get('/api/contas')
        this.contas = response.data
        this.error = null
      } catch (err) {
        this.error = err.message || 'Erro ao carregar contas'
        console.error('Erro ao carregar contas:', err.response?.data || err.message)
      } finally {
        this.loading = false
      }
    },

    async createConta(conta) {
      this.loading = true
      try {
        const response = await axios.post('/api/contas', conta)
        this.contas.push(response.data)
        this.error = null
        return response.data
      } catch (err) {
        this.error = err.message || 'Erro ao criar conta'
        console.error('Erro ao criar conta:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateConta(id, conta) {
      this.loading = true
      try {
        const response = await axios.put(`/api/contas/${id}`, conta)
        const index = this.contas.findIndex(c => c.id === id)
        if (index !== -1) {
          this.contas[index] = response.data
        }
        this.error = null
        return response.data
      } catch (err) {
        this.error = err.message || 'Erro ao atualizar conta'
        console.error('Erro ao atualizar conta:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteConta(id) {
      this.loading = true
      try {
        await axios.delete(`/api/contas/${id}`)
        this.contas = this.contas.filter(c => c.id !== id)
        this.error = null
      } catch (err) {
        this.error = err.message || 'Erro ao excluir conta'
        console.error('Erro ao excluir conta:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
