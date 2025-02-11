<template>
  <div>
    <main>
      <div class="max-w-7xl mx-auto">
        <h1 class="text-2xl font-semibold text-gray-900 mb-6">Dashboard</h1>
        
        <!-- Stats Cards -->
        <DashboardStats />

        <!-- Recent Activity -->
        <div class="mt-8">
          <h2 class="text-lg font-medium text-gray-900 mb-4">Atividade Recente</h2>
          <div class="bg-white shadow overflow-hidden sm:rounded-md">
            <ul class="divide-y divide-gray-200">
              <li v-for="activity in recentActivities" :key="activity.id">
                <div class="px-4 py-4 sm:px-6">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-medium text-blue-600 truncate">
                      {{ activity.title }}
                    </p>
                    <div class="ml-2 flex-shrink-0 flex">
                      <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                         :class="activity.type === 'user' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'">
                        {{ activity.type }}
                      </p>
                    </div>
                  </div>
                  <div class="mt-2 sm:flex sm:justify-between">
                    <div class="sm:flex">
                      <p class="flex items-center text-sm text-gray-500">
                        {{ activity.description }}
                      </p>
                    </div>
                    <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                      <p>
                        {{ activity.time }}
                      </p>
                    </div>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DashboardStats from '@/components/dashboard/DashboardStats.vue'

const recentActivities = ref([
  {
    id: 1,
    title: 'Novo usuário registrado',
    description: 'João Silva se registrou na plataforma',
    type: 'user',
    time: '5 minutos atrás'
  },
  {
    id: 2,
    title: 'Nova empresa adicionada',
    description: 'Tech Solutions Ltd foi adicionada',
    type: 'company',
    time: '1 hora atrás'
  },
  {
    id: 3,
    title: 'Atualização de perfil',
    description: 'Maria Souza atualizou suas informações',
    type: 'user',
    time: '2 horas atrás'
  }
])
</script>
