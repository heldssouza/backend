<template>
  <aside
    class="fixed inset-y-0 left-0 z-40 transition-all duration-300 ease-in-out transform"
    :class="[
      isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
      'w-64'
    ]"
  >
    <!-- Backdrop for mobile -->
    <div
      v-if="isOpen"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 transition-opacity lg:hidden"
      @click="$emit('close')"
    />

    <!-- Sidebar content -->
    <div class="h-full bg-white border-r border-gray-200 shadow-sm flex flex-col">
      <!-- Logo -->
      <div class="flex items-center h-16 px-6 border-b border-gray-200">
        <h1 class="text-xl font-semibold text-gray-900">
          Dashboard
        </h1>
      </div>

      <!-- User profile -->
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center">
              <span class="text-sm font-medium text-white">{{ userInitials }}</span>
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">
              {{ user.name }}
            </p>
            <p class="text-xs text-gray-500 truncate">
              {{ user.company }}
            </p>
          </div>
        </div>
        <div class="mt-2">
          <span
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
            :class="roleColors[user.role]"
          >
            {{ user.role }}
          </span>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
        <router-link
          v-for="item in navigationItems"
          :key="item.name"
          :to="item.path"
          class="group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200"
          :class="[
            activePath === item.path
              ? 'bg-blue-50 text-blue-600'
              : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900',
          ]"
          @click="$emit('close')"
        >
          <component
            :is="item.icon"
            class="mr-3 h-5 w-5 flex-shrink-0"
            :class="activePath === item.path ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-500'"
            aria-hidden="true"
          />
          {{ item.name }}
        </router-link>
      </nav>

      <!-- Bottom actions -->
      <div class="p-4 border-t border-gray-200">
        <button
          @click="logout"
          class="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200"
        >
          <ArrowLeftOnRectangleIcon class="mr-2 h-5 w-5 text-gray-400" />
          Sair
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeIcon,
  UsersIcon,
  FolderIcon,
  CalendarIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  ArrowLeftOnRectangleIcon,
  BanknotesIcon,
  BookOpenIcon,
  ScaleIcon,
  FolderOpenIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])

const route = useRoute()
const activePath = computed(() => route.path)

// Mock user data
const user = {
  name: 'João Silva',
  company: 'Empresa ABC',
  role: 'ADMIN',
  permissions: ['VIEW_DASHBOARD', 'MANAGE_USERS', 'MANAGE_COMPANIES']
}

const userInitials = computed(() => {
  return user.name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const navigationItems = [
  { name: 'Dashboard', path: '/dashboard', icon: HomeIcon, permission: 'VIEW_DASHBOARD' },
  { name: 'Usuários', path: '/users', icon: UsersIcon, permission: 'MANAGE_USERS' },
  { name: 'Empresas', path: '/companies', icon: FolderIcon, permission: 'MANAGE_COMPANIES' },
  { name: 'Contas', path: '/contas', icon: BanknotesIcon, permission: 'MANAGE_COMPANIES' },
  { name: 'Razão', path: '/razao', icon: BookOpenIcon, permission: 'MANAGE_COMPANIES' },
  { name: 'Saldos', path: '/saldos', icon: ScaleIcon, permission: 'MANAGE_COMPANIES' },
  { name: 'Grupos de Contas', path: '/grupocontas', icon: FolderOpenIcon, permission: 'MANAGE_COMPANIES' },
]

const roleColors = {
  ADMIN: 'bg-purple-100 text-purple-800',
  MANAGER: 'bg-blue-100 text-blue-800',
  USER: 'bg-green-100 text-green-800'
}

const logout = async () => {
  // Implement logout logic
  console.log('Logout clicked')
}
</script>
