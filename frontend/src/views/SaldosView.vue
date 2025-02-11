<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">Saldos</h1>
      <div class="flex space-x-4">
        <input
          v-model="filtroData"
          type="date"
          class="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        >
        <button
          @click="fetchSaldos"
          class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          Atualizar
        </button>
      </div>
    </div>

    <!-- Loading e Error states -->
    <div v-if="loading" class="text-center py-4">Carregando...</div>
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Tabela de Saldos -->
    <DataTable
      :data="saldos"
      :columns="columns"
      :selectable="false"
      :actions="false"
      @sort="handleSort"
    >
      <template #valor="{ item }">
        <span :class="item.valor >= 0 ? 'text-green-600' : 'text-red-600'">
          {{ formatCurrency(item.valor) }}
        </span>
      </template>
    </DataTable>

    <!-- Resumo dos Saldos -->
    <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-medium text-gray-900">Total Ativos</h3>
        <p class="mt-2 text-3xl font-semibold text-green-600">
          {{ formatCurrency(totalAtivos) }}
        </p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-medium text-gray-900">Total Passivos</h3>
        <p class="mt-2 text-3xl font-semibold text-red-600">
          {{ formatCurrency(totalPassivos) }}
        </p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-medium text-gray-900">Saldo Líquido</h3>
        <p class="mt-2 text-3xl font-semibold" :class="saldoLiquido >= 0 ? 'text-green-600' : 'text-red-600'">
          {{ formatCurrency(saldoLiquido) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSaldosStore } from '@/stores/saldos'
import DataTable from '@/components/DataTable.vue'

const saldosStore = useSaldosStore()
const filtroData = ref(new Date().toISOString().split('T')[0])

const columns = [
  { key: 'conta_codigo', label: 'Código', sortable: true },
  { key: 'conta_descricao', label: 'Descrição', sortable: true },
  { key: 'tipo', label: 'Tipo', sortable: true },
  { key: 'valor', label: 'Saldo', sortable: true }
]

const { saldos, loading, error } = saldosStore

const totalAtivos = computed(() => {
  return saldos.value
    ?.filter(s => s.tipo === 'ATIVO')
    .reduce((acc, curr) => acc + curr.valor, 0) || 0
})

const totalPassivos = computed(() => {
  return saldos.value
    ?.filter(s => s.tipo === 'PASSIVO')
    .reduce((acc, curr) => acc + curr.valor, 0) || 0
})

const saldoLiquido = computed(() => {
  return totalAtivos.value - totalPassivos.value
})

onMounted(() => {
  fetchSaldos()
})

async function fetchSaldos() {
  try {
    await saldosStore.fetchSaldos({ data: filtroData.value })
  } catch (err) {
    console.error('Erro ao carregar saldos:', err)
  }
}

function handleSort({ key, order }) {
  // Implementar ordenação se necessário
  console.log('Ordenar por:', key, 'ordem:', order)
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}
</script>
