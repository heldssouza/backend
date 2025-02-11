import { defineStore } from 'pinia'
import axios from '@/plugins/axios'

export const useSaldosStore = defineStore('saldos', {
  state: () => ({
    saldos: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchSaldos() {
      this.loading = true
      try {
        const response = await axios.get('/api/saldos')
        this.saldos = response.data
        this.error = null
      } catch (err) {
        this.error = err.message || 'Erro ao carregar saldos'
        console.error('Erro ao carregar saldos:', err.response?.data || err.message)
      } finally {
        this.loading = false
      }
    },

    async createSaldo(saldo) {
      this.loading = true
      try {
        const response = await axios.post('/api/saldos', saldo)
        this.saldos.push(response.data)
        this.error = null
        return response.data
      } catch (err) {
        this.error = err.message || 'Erro ao criar saldo'
        console.error('Erro ao criar saldo:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateSaldo(id, saldo) {
      this.loading = true
      try {
        const response = await axios.put(`/api/saldos/${id}`, saldo)
        const index = this.saldos.findIndex(s => s.id === id)
        if (index !== -1) {
          this.saldos[index] = response.data
        }
        this.error = null
        return response.data
      } catch (err) {
        this.error = err.message || 'Erro ao atualizar saldo'
        console.error('Erro ao atualizar saldo:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteSaldo(id) {
      this.loading = true
      try {
        await axios.delete(`/api/saldos/${id}`)
        this.saldos = this.saldos.filter(s => s.id !== id)
        this.error = null
      } catch (err) {
        this.error = err.message || 'Erro ao excluir saldo'
        console.error('Erro ao excluir saldo:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
