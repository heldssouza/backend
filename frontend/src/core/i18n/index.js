import { createI18n } from 'vue-i18n'
import ptBR from './locales/pt-BR'
import enUS from './locales/en-US'

export const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('language') || 'pt-BR',
  fallbackLocale: 'en-US',
  messages: {
    'pt-BR': ptBR,
    'en-US': enUS
  },
  numberFormats: {
    'pt-BR': {
      currency: {
        style: 'currency',
        currency: 'BRL'
      }
    },
    'en-US': {
      currency: {
        style: 'currency',
        currency: 'USD'
      }
    }
  },
  datetimeFormats: {
    'pt-BR': {
      short: {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      },
      long: {
        year: 'numeric',
        month: 'long',
        day: '2-digit',
        weekday: 'long',
        hour: '2-digit',
        minute: '2-digit'
      }
    },
    'en-US': {
      short: {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      },
      long: {
        year: 'numeric',
        month: 'long',
        day: '2-digit',
        weekday: 'long',
        hour: '2-digit',
        minute: '2-digit'
      }
    }
  }
})
