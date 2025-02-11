<template>
  <div>
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-semibold text-gray-900">Usuários</h1>
        <button
          @click="openAddUserModal"
          class="btn-primary flex items-center"
        >
          <span class="mr-2">Adicionar Usuário</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Tabela de Usuários -->
      <div class="mt-8 flex flex-col">
        <div class="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Nome</th>
                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Email</th>
                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Cargo</th>
                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Status</th>
                    <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span class="sr-only">Ações</span>
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 bg-white">
                  <tr v-for="user in users" :key="user.id">
                    <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm">
                      <div class="flex items-center">
                        <div class="h-10 w-10 flex-shrink-0">
                          <img class="h-10 w-10 rounded-full" :src="user.avatar || 'https://ui-avatars.com/api/?name=' + user.name" alt="" />
                        </div>
                        <div class="ml-4">
                          <div class="font-medium text-gray-900">{{ user.name }}</div>
                        </div>
                      </div>
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ user.email }}</td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ user.role }}</td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                      <span :class="[
                        user.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800',
                        'inline-flex rounded-full px-2 text-xs font-semibold leading-5'
                      ]">
                        {{ user.status }}
                      </span>
                    </td>
                    <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                      <button @click="editUser(user)" class="text-blue-600 hover:text-blue-900 mr-4">Editar</button>
                      <button @click="deleteUser(user)" class="text-red-600 hover:text-red-900">Excluir</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Adicionar/Editar Usuário -->
    <div v-if="showModal" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
              {{ editingUser ? 'Editar Usuário' : 'Adicionar Usuário' }}
            </h3>
            <div class="mt-2">
              <form @submit.prevent="saveUser">
                <div class="space-y-4">
                  <div>
                    <label for="name" class="block text-sm font-medium text-gray-700">Nome</label>
                    <input type="text" id="name" v-model="userForm.name" class="input-primary" required />
                  </div>
                  <div>
                    <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                    <input type="email" id="email" v-model="userForm.email" class="input-primary" required />
                  </div>
                  <div>
                    <label for="role" class="block text-sm font-medium text-gray-700">Cargo</label>
                    <select id="role" v-model="userForm.role" class="input-primary" required>
                      <option value="admin">Admin</option>
                      <option value="manager">Gerente</option>
                      <option value="user">Usuário</option>
                    </select>
                  </div>
                </div>
                <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                  <button type="submit" class="btn-primary">
                    {{ editingUser ? 'Salvar' : 'Adicionar' }}
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
import { ref, onMounted } from 'vue'
import Sidebar from '@/components/layout/Sidebar.vue'

const users = ref([
  {
    id: 1,
    name: 'Admin User',
    email: 'admin@example.com',
    role: 'admin',
    status: 'active',
  },
  {
    id: 2,
    name: 'Manager User',
    email: 'manager@example.com',
    role: 'manager',
    status: 'active',
  },
  {
    id: 3,
    name: 'Regular User',
    email: 'user@example.com',
    role: 'user',
    status: 'inactive',
  },
])

const showModal = ref(false)
const editingUser = ref(null)
const userForm = ref({
  name: '',
  email: '',
  role: 'user',
})

const openAddUserModal = () => {
  editingUser.value = null
  userForm.value = {
    name: '',
    email: '',
    role: 'user',
  }
  showModal.value = true
}

const editUser = (user) => {
  editingUser.value = user
  userForm.value = { ...user }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingUser.value = null
}

const saveUser = () => {
  if (editingUser.value) {
    const index = users.value.findIndex(u => u.id === editingUser.value.id)
    users.value[index] = { ...editingUser.value, ...userForm.value }
  } else {
    users.value.push({
      id: users.value.length + 1,
      ...userForm.value,
      status: 'active',
    })
  }
  closeModal()
}

const deleteUser = (user) => {
  if (confirm(`Tem certeza que deseja excluir o usuário ${user.name}?`)) {
    users.value = users.value.filter(u => u.id !== user.id)
  }
}
</script>
