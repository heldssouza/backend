<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">Gerenciamento de Contas</h1>
      <button
        @click="openModal()"
        class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        Nova Conta
      </button>
    </div>

    <!-- Loading e Error states -->
    <div v-if="loading" class="text-center py-4">Carregando...</div>
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Tabela de Contas -->
    <DataTable
      :data="contas"
      :columns="columns"
      :selectable="true"
      :actions="true"
      v-model:selected="selectedContas"
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
            @click="deleteConta(item.id)"
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
        <h2 class="text-xl font-semibold mb-4">{{ editingConta ? 'Editar' : 'Nova' }} Conta</h2>
        <form @submit.prevent="saveConta">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Código</label>
              <input
                v-model="formData.codigo"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Descrição</label>
              <input
                v-model="formData.descricao"
                type="text"
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
                <option value="ATIVO">Ativo</option>
                <option value="PASSIVO">Passivo</option>
                <option value="RECEITA">Receita</option>
                <option value="DESPESA">Despesa</option>
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
import { useContasStore } from '@/stores/contas'
import DataTable from '@/components/DataTable.vue'

const contasStore = useContasStore()
const showModal = ref(false)
const editingConta = ref(null)
const selectedContas = ref([])

const columns = [
  { key: 'codigo', label: 'Código', sortable: true },
  { key: 'descricao', label: 'Descrição', sortable: true },
  { key: 'tipo', label: 'Tipo', sortable: true }
]

const formData = ref({
  codigo: '',
  descricao: '',
  tipo: 'ATIVO'
})

const { contas, loading, error } = contasStore

onMounted(() => {
  contasStore.fetchContas()
})

function openModal(conta = null) {
  if (conta) {
    editingConta.value = conta
    formData.value = { ...conta }
  } else {
    editingConta.value = null
    formData.value = {
      codigo: '',
      descricao: '',
      tipo: 'ATIVO'
    }
  }
  showModal.value = true
}

async function saveConta() {
  try {
    if (editingConta.value) {
      await contasStore.updateConta(editingConta.value.id, formData.value)
    } else {
      await contasStore.createConta(formData.value)
    }
    showModal.value = false
  } catch (err) {
    console.error('Erro ao salvar conta:', err)
  }
}

async function deleteConta(id) {
  if (confirm('Tem certeza que deseja excluir esta conta?')) {
    try {
      await contasStore.deleteConta(id)
    } catch (err) {
      console.error('Erro ao excluir conta:', err)
    }
  }
}

function handleSort({ key, order }) {
  // Implementar ordenação se necessário
  console.log('Ordenar por:', key, 'ordem:', order)
}
</script>
