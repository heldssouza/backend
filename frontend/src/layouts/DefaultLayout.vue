<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Mobile menu button -->
    <button 
      @click="isSidebarOpen = !isSidebarOpen"
      class="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-md bg-white shadow-sm hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <Bars3Icon v-if="!isSidebarOpen" class="h-6 w-6 text-gray-600" />
      <XMarkIcon v-else class="h-6 w-6 text-gray-600" />
    </button>

    <div class="lg:grid lg:grid-cols-[auto,1fr]">
      <!-- Sidebar -->
      <aside 
        class="fixed lg:relative inset-y-0 left-0 z-40 w-64 transform transition-transform duration-300 ease-in-out bg-white border-r border-gray-200 overflow-y-auto"
        :class="[isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0']"
      >
        <Sidebar 
          :is-open="isSidebarOpen" 
          @close="isSidebarOpen = false"
        />
      </aside>

      <!-- Main content -->
      <main class="min-h-screen bg-gray-50">
        <div class="p-4 pt-16 lg:pt-4">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'
import Sidebar from '@/components/layout/Sidebar.vue'

const isSidebarOpen = ref(true)
</script>
