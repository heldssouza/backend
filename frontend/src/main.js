import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './core/router'
import { i18n } from './core/i18n'
import './shared/styles/index.css'

// Create Vue app
const app = createApp(App)

// Use plugins
app.use(createPinia())
app.use(router)
app.use(i18n)

// Mount app
app.mount('#app')
