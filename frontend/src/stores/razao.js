import { defineStore } from 'pinia'
import axios from '@/plugins/axios'

export const useRazaoStore = defineStore('razao', {
  state: () => ({
    razao: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchRazao() {
      this.loading = true
      try {
        const response = await axios.get('/api/razao')
        this.razao = response.data
        this.error = null
      } catch (err) {
        this.error = err.message || 'Erro ao carregar razão'
        console.error('Erro ao carregar razão:', err.response?.data || err.message)
      } finally {
        this.loading = false
      }
    },

    async createRazao(razao) {
      this.loading = true
      try {
        const response = await axios.post('/api/razao', razao)
        this.razao.push(response.data)
        this.error = null
        return response.data
      } catch (err) {
        this.error = err.message || 'Erro ao criar lançamento'
        console.error('Erro ao criar lançamento:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateRazao(id, razao) {
      this.loading = true
      try {
        const response = await axios.put(`/api/razao/${id}`, razao)
        const index = this.razao.findIndex(r => r.id === id)
        if (index !== -1) {
          this.razao[index] = response.data
        }
        this.error = null
        return response.data
      } catch (err) {
        this.error = err.message || 'Erro ao atualizar lançamento'
        console.error('Erro ao atualizar lançamento:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteRazao(id) {
      this.loading = true
      try {
        await axios.delete(`/api/razao/${id}`)
        this.razao = this.razao.filter(r => r.id !== id)
        this.error = null
      } catch (err) {
        this.error = err.message || 'Erro ao excluir lançamento'
        console.error('Erro ao excluir lançamento:', err.response?.data || err.message)
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
