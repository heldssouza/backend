import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true
})

// Interceptor para tratar erros globalmente
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    const { response } = error
    
    if (response && response.status === 500) {
      console.error('Erro interno do servidor:', response.data)
    }

    return Promise.reject(error)
  }
)

export default axiosInstance
