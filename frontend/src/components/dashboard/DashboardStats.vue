<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <div v-for="stat in stats" :key="stat.name" 
         class="bg-white overflow-hidden shadow rounded-lg">
      <div class="p-5">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <component :is="stat.icon" 
                      :class="[stat.iconColor, 'h-6 w-6']" />
          </div>
          <div class="ml-5 w-0 flex-1">
            <dl>
              <dt class="text-sm font-medium text-gray-500 truncate">
                {{ stat.name }}
              </dt>
              <dd class="flex items-baseline">
                <div class="text-2xl font-semibold text-gray-900">
                  {{ stat.value }}
                </div>
                <div :class="[stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600',
                            'ml-2 flex items-baseline text-sm font-semibold']">
                  {{ stat.change }}
                </div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
      <div class="bg-gray-50 px-5 py-3">
        <div class="text-sm">
          <a :href="stat.href" class="font-medium text-blue-600 hover:text-blue-900">
            Ver detalhes
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Mock data - será substituída pela integração com a API
const stats = [
  {
    name: 'Usuários Ativos',
    value: '1,234',
    change: '+12%',
    changeType: 'increase',
    href: '#',
    iconColor: 'text-blue-500'
  },
  {
    name: 'Empresas',
    value: '42',
    change: '+8%',
    changeType: 'increase',
    href: '#',
    iconColor: 'text-green-500'
  },
  {
    name: 'Taxa de Conversão',
    value: '24.57%',
    change: '+3.2%',
    changeType: 'increase',
    href: '#',
    iconColor: 'text-purple-500'
  },
  {
    name: 'Tempo Médio',
    value: '2.4min',
    change: '-1.1%',
    changeType: 'decrease',
    href: '#',
    iconColor: 'text-yellow-500'
  }
]
</script>
