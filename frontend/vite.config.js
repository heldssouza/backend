import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@shared': path.resolve(__dirname, './src/shared'),
      '@core': path.resolve(__dirname, './src/core'),
      '@apps': path.resolve(__dirname, './src/apps'),
    }
  },
  server: {
    port: 5000,
    proxy: {
      '^/api/v1': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/v1/, '')
      }
    }
  },
  define: {
    'process.env': {
      VUE_APP_API_URL: '/api/v1'
    }
  },
  optimizeDeps: {
    exclude: ['vue-demi']
  }
})
