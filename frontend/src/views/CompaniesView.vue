<template>
  <div>
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-semibold text-gray-900">Empresas</h1>
        <button
          @click="openAddCompanyModal"
          class="btn-primary flex items-center"
        >
          <span class="mr-2">Adicionar Empresa</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Grid de Empresas -->
      <div class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div v-for="company in companies" :key="company.id" class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <img class="h-12 w-12 rounded-full" :src="company.logo || 'https://ui-avatars.com/api/?name=' + company.name" alt="" />
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">{{ company.name }}</h3>
                <p class="text-sm text-gray-500">{{ company.industry }}</p>
              </div>
            </div>
            <div class="mt-4">
              <p class="text-sm text-gray-500">{{ company.description }}</p>
            </div>
            <div class="mt-4">
              <div class="flex space-x-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {{ company.size }} funcionários
                </span>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  {{ company.status }}
                </span>
              </div>
            </div>
            <div class="mt-4 flex justify-end space-x-4">
              <button @click="editCompany(company)" class="text-blue-600 hover:text-blue-900">Editar</button>
              <button @click="deleteCompany(company)" class="text-red-600 hover:text-red-900">Excluir</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Adicionar/Editar Empresa -->
    <div v-if="showModal" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
              {{ editingCompany ? 'Editar Empresa' : 'Adicionar Empresa' }}
            </h3>
            <div class="mt-2">
              <form @submit.prevent="saveCompany">
                <div class="space-y-4">
                  <div>
                    <label for="name" class="block text-sm font-medium text-gray-700">Nome</label>
                    <input type="text" id="name" v-model="companyForm.name" class="input-primary" required />
                  </div>
                  <div>
                    <label for="industry" class="block text-sm font-medium text-gray-700">Indústria</label>
                    <input type="text" id="industry" v-model="companyForm.industry" class="input-primary" required />
                  </div>
                  <div>
                    <label for="description" class="block text-sm font-medium text-gray-700">Descrição</label>
                    <textarea id="description" v-model="companyForm.description" rows="3" class="input-primary"></textarea>
                  </div>
                  <div>
                    <label for="size" class="block text-sm font-medium text-gray-700">Tamanho</label>
                    <select id="size" v-model="companyForm.size" class="input-primary" required>
                      <option value="1-10">1-10</option>
                      <option value="11-50">11-50</option>
                      <option value="51-200">51-200</option>
                      <option value="201-500">201-500</option>
                      <option value="500+">500+</option>
                    </select>
                  </div>
                </div>
                <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                  <button type="submit" class="btn-primary">
                    {{ editingCompany ? 'Salvar' : 'Adicionar' }}
                  </button>
                  <button type="button" @click="closeModal" class="mt-3 sm:mt-0 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:col-start-1 sm:text-sm">
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '@/components/layout/Sidebar.vue'

const companies = ref([
  {
    id: 1,
    name: 'Tech Corp',
    industry: 'Tecnologia',
    description: 'Empresa líder em soluções tecnológicas',
    size: '51-200',
    status: 'Ativa',
    logo: null
  },
  {
    id: 2,
    name: 'Green Energy',
    industry: 'Energia',
    description: 'Soluções sustentáveis em energia',
    size: '11-50',
    status: 'Ativa',
    logo: null
  },
  {
    id: 3,
    name: 'Global Finance',
    industry: 'Finanças',
    description: 'Serviços financeiros globais',
    size: '201-500',
    status: 'Ativa',
    logo: null
  }
])

const showModal = ref(false)
const editingCompany = ref(null)
const companyForm = ref({
  name: '',
  industry: '',
  description: '',
  size: '1-10'
})

const openAddCompanyModal = () => {
  editingCompany.value = null
  companyForm.value = {
    name: '',
    industry: '',
    description: '',
    size: '1-10'
  }
  showModal.value = true
}

const editCompany = (company) => {
  editingCompany.value = company
  companyForm.value = { ...company }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingCompany.value = null
}

const saveCompany = () => {
  if (editingCompany.value) {
    const index = companies.value.findIndex(c => c.id === editingCompany.value.id)
    companies.value[index] = { ...editingCompany.value, ...companyForm.value }
  } else {
    companies.value.push({
      id: companies.value.length + 1,
      ...companyForm.value,
      status: 'Ativa',
      logo: null
    })
  }
  closeModal()
}

const deleteCompany = (company) => {
  if (confirm(`Tem certeza que deseja excluir a empresa ${company.name}?`)) {
    companies.value = companies.value.filter(c => c.id !== company.id)
  }
}
</script>
