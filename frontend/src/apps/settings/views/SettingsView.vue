<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold">{{ $t('settings.title') }}</h1>
      <p class="text-gray-600">{{ $t('settings.description') }}</p>
    </div>

    <!-- Content -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Sidebar -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-lg shadow">
          <nav class="space-y-1">
            <RouterLink
              v-for="item in menuItems"
              :key="item.path"
              :to="item.path"
              class="flex items-center px-4 py-3 text-sm font-medium"
              :class="[
                isActive(item.path)
                  ? 'bg-primary/10 text-primary border-r-4 border-primary'
                  : 'text-gray-600 hover:bg-base-200'
              ]"
            >
              <component
                :is="item.icon"
                class="h-5 w-5 mr-3"
                :class="isActive(item.path) ? 'text-primary' : 'text-gray-400'"
              />
              {{ item.name }}
            </RouterLink>
          </nav>
        </div>
      </div>

      <!-- Main Content -->
      <div class="lg:col-span-3">
        <div class="bg-white rounded-lg shadow p-6">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  UserCircleIcon,
  Cog6ToothIcon,
  BellIcon,
  KeyIcon,
  DevicePhoneMobileIcon,
  ClockIcon,
  ArrowDownTrayIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const { t } = useI18n()

const menuItems = [
  {
    name: t('settings.profile'),
    path: '/settings/profile',
    icon: UserCircleIcon
  },
  {
    name: t('settings.preferences'),
    path: '/settings/preferences',
    icon: Cog6ToothIcon
  },
  {
    name: t('settings.notifications'),
    path: '/settings/notifications',
    icon: BellIcon,
    disabled: true
  },
  {
    name: t('settings.security'),
    path: '/settings/security',
    icon: KeyIcon,
    disabled: true
  },
  {
    name: t('settings.sessions'),
    path: '/settings/sessions',
    icon: DevicePhoneMobileIcon,
    disabled: true
  },
  {
    name: t('settings.activity'),
    path: '/settings/activity',
    icon: ClockIcon,
    disabled: true
  },
  {
    name: t('settings.export'),
    path: '/settings/export',
    icon: ArrowDownTrayIcon,
    disabled: true
  },
  {
    name: t('settings.deleteAccount'),
    path: '/settings/delete-account',
    icon: TrashIcon,
    disabled: true
  }
]

const isActive = (path) => {
  return route.path === path
}
</script>
