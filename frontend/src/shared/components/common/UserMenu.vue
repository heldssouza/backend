<template>
  <div class="relative">
    <button
      @click="toggleMenu"
      class="flex items-center space-x-2 text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      <img
        class="h-8 w-8 rounded-full"
        :src="userAvatar"
        :alt="user?.name || 'User'"
      />
      <span class="hidden md:inline-block text-gray-700">{{ user?.name }}</span>
      <svg
        class="h-5 w-5 text-gray-400"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
          clip-rule="evenodd"
        />
      </svg>
    </button>

    <!-- Dropdown Menu -->
    <div
      v-if="isOpen"
      class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100"
    >
      <!-- User Info -->
      <div class="px-4 py-3">
        <p class="text-sm">{{ $t('common.signedInAs') }}</p>
        <p class="text-sm font-medium text-gray-900 truncate">
          {{ user?.email }}
        </p>
      </div>

      <!-- Menu Items -->
      <div class="py-1">
        <router-link
          :to="{ name: 'Profile' }"
          class="menu-item"
          @click="isOpen = false"
        >
          {{ $t('common.profile') }}
        </router-link>
        <router-link
          :to="{ name: 'Settings' }"
          class="menu-item"
          @click="isOpen = false"
        >
          {{ $t('common.settings') }}
        </router-link>
      </div>

      <!-- Logout -->
      <div class="py-1">
        <button
          @click="handleLogout"
          class="menu-item text-red-700 hover:bg-red-50 w-full text-left"
        >
          {{ $t('common.logout') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/core/store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const isOpen = ref(false)

const user = computed(() => authStore.user)
const userAvatar = computed(() => {
  return user.value?.avatar || 'https://www.gravatar.com/avatar/?d=mp'
})

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push({ name: 'Login' })
  } catch (error) {
    console.error('Erro ao fazer logout:', error)
  }
}

// Fecha o menu quando clicar fora dele
const handleClickOutside = (event) => {
  if (isOpen.value && !event.target.closest('.relative')) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.menu-item {
  @apply block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left;
}
</style>
