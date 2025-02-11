<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">Razão</h1>
      <button
        @click="openModal()"
        class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        Novo Lançamento
      </button>
    </div>

    <!-- Loading e Error states -->
    <div v-if="loading" class="text-center py-4">Carregando...</div>
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Tabela de Razão -->
    <DataTable
      :data="razao"
      :columns="columns"
      :selectable="true"
      :actions="true"
      v-model:selected="selectedItems"
      @sort="handleSort"
    >
      <template #actions="{ item }">
        <div class="flex justify-end space-x-2">
          <button
            @click="openModal(item)"
            class="text-indigo-600 hover:text-indigo-900"
          >
            Editar
          </button>
          <button
            @click="deleteItem(item.id)"
            class="text-red-600 hover:text-red-900"
          >
            Excluir
          </button>
        </div>
      </template>
    </DataTable>

    <!-- Modal de Criação/Edição -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h2 class="text-xl font-semibold mb-4">{{ editingItem ? 'Editar' : 'Novo' }} Lançamento</h2>
        <form @submit.prevent="saveItem">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Data</label>
              <input
                v-model="formData.data"
                type="date"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Conta</label>
              <select
                v-model="formData.conta_id"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              >
                <option v-for="conta in contas" :key="conta.id" :value="conta.id">
                  {{ conta.codigo }} - {{ conta.descricao }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Histórico</label>
              <input
                v-model="formData.historico"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Valor</label>
              <input
                v-model="formData.valor"
                type="number"
                step="0.01"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Tipo</label>
              <select
                v-model="formData.tipo"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              >
                <option value="DEBITO">Débito</option>
                <option value="CREDITO">Crédito</option>
              </select>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button
              type="button"
              @click="showModal = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
            >
              Salvar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRazaoStore } from '@/stores/razao'
import { useContasStore } from '@/stores/contas'
import DataTable from '@/components/DataTable.vue'

const razaoStore = useRazaoStore()
const contasStore = useContasStore()
const showModal = ref(false)
const editingItem = ref(null)
const selectedItems = ref([])

const columns = [
  { key: 'data', label: 'Data', sortable: true },
  { key: 'conta', label: 'Conta', sortable: true },
  { key: 'historico', label: 'Histórico', sortable: true },
  { key: 'valor', label: 'Valor', sortable: true },
  { key: 'tipo', label: 'Tipo', sortable: true }
]

const formData = ref({
  data: '',
  conta_id: '',
  historico: '',
  valor: 0,
  tipo: 'DEBITO'
})

const { razao, loading, error } = razaoStore
const { contas } = contasStore

onMounted(async () => {
  await razaoStore.fetchRazao()
  await contasStore.fetchContas()
})

function openModal(item = null) {
  if (item) {
    editingItem.value = item
    formData.value = {
      data: item.data,
      conta_id: item.conta_id,
      historico: item.historico,
      valor: item.valor,
      tipo: item.tipo
    }
  } else {
    editingItem.value = null
    formData.value = {
      data: new Date().toISOString().split('T')[0],
      conta_id: '',
      historico: '',
      valor: 0,
      tipo: 'DEBITO'
    }
  }
  showModal.value = true
}

async function saveItem() {
  try {
    if (editingItem.value) {
      await razaoStore.updateRazao(editingItem.value.id, formData.value)
    } else {
      await razaoStore.createRazao(formData.value)
    }
    showModal.value = false
  } catch (err) {
    console.error('Erro ao salvar lançamento:', err)
  }
}

async function deleteItem(id) {
  if (confirm('Tem certeza que deseja excluir este lançamento?')) {
    try {
      await razaoStore.deleteRazao(id)
    } catch (err) {
      console.error('Erro ao excluir lançamento:', err)
    }
  }
}

function handleSort({ key, order }) {
  // Implementar ordenação se necessário
  console.log('Ordenar por:', key, 'ordem:', order)
}
</script>
