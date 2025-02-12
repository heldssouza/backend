<template>
  <div
    v-if="notification"
    class="fixed bottom-4 right-4 z-50"
    @click="dismissNotification"
  >
    <div
      class="alert shadow-lg"
      :class="{
        'alert-success': notification.type === 'success',
        'alert-error': notification.type === 'error',
        'alert-warning': notification.type === 'warning',
        'alert-info': notification.type === 'info'
      }"
    >
      <div class="flex items-center">
        <!-- Success Icon -->
        <svg
          v-if="notification.type === 'success'"
          xmlns="http://www.w3.org/2000/svg"
          class="stroke-current flex-shrink-0 h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>

        <!-- Error Icon -->
        <svg
          v-if="notification.type === 'error'"
          xmlns="http://www.w3.org/2000/svg"
          class="stroke-current flex-shrink-0 h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>

        <!-- Warning Icon -->
        <svg
          v-if="notification.type === 'warning'"
          xmlns="http://www.w3.org/2000/svg"
          class="stroke-current flex-shrink-0 h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>

        <!-- Info Icon -->
        <svg
          v-if="notification.type === 'info'"
          xmlns="http://www.w3.org/2000/svg"
          class="stroke-current flex-shrink-0 h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>

        <span>{{ notification.message }}</span>

        <!-- Close Button -->
        <button
          class="btn btn-ghost btn-sm"
          @click.stop="dismissNotification"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useNotificationStore } from '@/core/store/notification'

const notificationStore = useNotificationStore()
const notification = ref(null)
let timeout = null

// Atualiza a notificação quando o store é atualizado
const unsubscribe = notificationStore.$subscribe((mutation, state) => {
  if (state.notification) {
    showNotification(state.notification)
  }
})

const showNotification = (newNotification) => {
  notification.value = newNotification

  // Limpa o timeout anterior se existir
  if (timeout) {
    clearTimeout(timeout)
  }

  // Define um novo timeout para remover a notificação após 5 segundos
  timeout = setTimeout(() => {
    dismissNotification()
  }, 5000)
}

const dismissNotification = () => {
  notification.value = null
  notificationStore.clearNotification()
  if (timeout) {
    clearTimeout(timeout)
    timeout = null
  }
}

onUnmounted(() => {
  unsubscribe()
  if (timeout) {
    clearTimeout(timeout)
  }
})
</script>
