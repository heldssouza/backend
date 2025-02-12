import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notification: null
  }),

  actions: {
    setNotification(notification) {
      this.notification = notification
    },

    clearNotification() {
      this.notification = null
    }
  }
})
