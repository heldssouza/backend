<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo and primary navigation -->
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <img class="h-8 w-auto" src="@/assets/logo.svg" alt="Logo" />
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <!-- Navigation Links -->
              <router-link
                v-for="item in navigationItems"
                :key="item.path"
                :to="item.path"
                v-if="checkAccess(item)"
                class="inline-flex items-center px-1 pt-1 border-b-2"
                :class="[
                  $route.path.startsWith(item.path)
                    ? 'border-indigo-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                {{ $t(item.label) }}
              </router-link>
            </div>
          </div>

          <!-- Right side navigation -->
          <div class="flex items-center">
            <!-- Language Selector -->
            <LanguageSelector class="mr-4" />

            <!-- User Dropdown -->
            <UserMenu />
          </div>
        </div>
      </div>
    </nav>

    <!-- Page Content -->
    <main>
      <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- Breadcrumb -->
        <Breadcrumb />

        <!-- Content -->
        <div class="px-4 py-6 sm:px-0">
          <slot></slot>
        </div>
      </div>
    </main>

    <!-- Notification -->
    <NotificationToast />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/core/store/auth'
import LanguageSelector from '../common/LanguageSelector.vue'
import UserMenu from '../common/UserMenu.vue'
import Breadcrumb from '../common/Breadcrumb.vue'
import NotificationToast from '../common/NotificationToast.vue'

const authStore = useAuthStore()

const navigationItems = ref([
  {
    path: '/dashboard',
    label: 'nav.dashboard',
    permission: 'view_dashboard'
  },
  {
    path: '/users',
    label: 'nav.users',
    permission: 'manage_users'
  },
  {
    path: '/tenants',
    label: 'nav.tenants',
    permission: 'manage_tenants'
  },
  {
    path: '/roles',
    label: 'nav.roles',
    permission: 'manage_roles'
  }
])

const checkAccess = (item) => {
  if (!item.permission) return true
  return authStore.hasPermission(item.permission)
}
</script>
