import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

// Cria a instância do app
const app = createApp(App)

// Configura o Pinia para gerenciamento de estado
const pinia = createPinia()
app.use(pinia)

// Configura o Vue Router
app.use(router)

// Monta o app
app.mount('#app')
