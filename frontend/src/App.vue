<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './core/store/auth'
import eventBus, { EventTypes } from './infrastructure/events/eventBus'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  // Listen for session expiration
  eventBus.on(EventTypes.SESSION_EXPIRED, () => {
    router.push('/auth/login')
  })
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
