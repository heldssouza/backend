import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
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
