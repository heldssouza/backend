<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="page-title">{{ $t('dashboard.title') }}</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Card de Usuários -->
      <div class="card-container">
        <h2 class="text-lg font-medium text-gray-900 mb-2">{{ $t('dashboard.totalUsers') }}</h2>
        <div class="flex items-center">
          <div class="bg-primary/10 p-3 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <div class="ml-4">
            <span class="text-2xl font-semibold">{{ totalUsers }}</span>
          </div>
        </div>
      </div>

      <!-- Card de Inquilinos -->
      <div class="card-container">
        <h2 class="text-lg font-medium text-gray-900 mb-2">{{ $t('dashboard.activeTenants') }}</h2>
        <div class="flex items-center">
          <div class="bg-secondary/10 p-3 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <div class="ml-4">
            <span class="text-2xl font-semibold">{{ activeTenants }}</span>
          </div>
        </div>
      </div>

      <!-- Card de Atividade Recente -->
      <div class="card-container">
        <h2 class="text-lg font-medium text-gray-900 mb-2">{{ $t('dashboard.recentActivity') }}</h2>
        <div class="space-y-4">
          <div v-for="activity in recentActivities" :key="activity.id" class="flex items-start">
            <div class="bg-info/10 p-2 rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-info" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-gray-600">{{ activity.description }}</p>
              <p class="text-xs text-gray-400">{{ formatDate(activity.timestamp) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { format } from 'date-fns'
import { useAuthStore } from '@/core/store/auth'

const authStore = useAuthStore()

const totalUsers = ref(0)
const activeTenants = ref(0)
const recentActivities = ref([
  {
    id: 1,
    description: 'Novo usuário registrado',
    timestamp: new Date(Date.now() - 1000 * 60 * 30) // 30 minutos atrás
  },
  {
    id: 2,
    description: 'Inquilino atualizado',
    timestamp: new Date(Date.now() - 1000 * 60 * 60) // 1 hora atrás
  },
  {
    id: 3,
    description: 'Nova função criada',
    timestamp: new Date(Date.now() - 1000 * 60 * 120) // 2 horas atrás
  }
])

const formatDate = (date) => {
  return format(new Date(date), 'dd/MM/yyyy HH:mm')
}

onMounted(async () => {
  try {
    // Aqui você pode adicionar chamadas à API para buscar os dados reais
    totalUsers.value = 150
    activeTenants.value = 25
  } catch (error) {
    console.error('Erro ao carregar dados do dashboard:', error)
  }
})
</script>
