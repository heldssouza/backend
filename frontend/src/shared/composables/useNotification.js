import { useNotificationStore } from '@/core/store/notification'

export function useNotification() {
  const notificationStore = useNotificationStore()

  const showNotification = (message, type = 'info') => {
    notificationStore.setNotification({ message, type })
  }

  const showSuccess = (message) => {
    showNotification(message, 'success')
  }

  const showError = (message) => {
    showNotification(message, 'error')
  }

  const showWarning = (message) => {
    showNotification(message, 'warning')
  }

  const showInfo = (message) => {
    showNotification(message, 'info')
  }

  return {
    showNotification,
    showSuccess,
    showError,
    showWarning,
    showInfo
  }
}
