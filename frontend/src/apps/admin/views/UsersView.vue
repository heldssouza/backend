<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="page-title">{{ $t('users.title') }}</h1>
      <div class="flex space-x-3">
        <button
          v-if="hasPermission('import_users')"
          class="btn btn-outline btn-primary"
          @click="importModal = true"
        >
          <ArrowUpTrayIcon class="h-5 w-5 mr-2" />
          {{ $t('users.import') }}
        </button>
        <button
          v-if="hasPermission('export_users')"
          class="btn btn-outline btn-primary"
          @click="exportUsers"
        >
          <ArrowDownTrayIcon class="h-5 w-5 mr-2" />
          {{ $t('users.export') }}
        </button>
        <button
          v-if="hasPermission('create_users')"
          class="btn btn-primary"
          @click="openUserModal()"
        >
          <PlusIcon class="h-5 w-5 mr-2" />
          {{ $t('users.create') }}
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="card-container">
      <Form @submit="handleFilter" class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="form-label">{{ $t('users.search') }}</label>
          <Field
            name="search"
            type="text"
            class="input-primary"
            :placeholder="$t('users.searchPlaceholder')"
          />
        </div>
        <div>
          <label class="form-label">{{ $t('users.role') }}</label>
          <Field
            name="role"
            as="select"
            class="input-primary"
          >
            <option value="">{{ $t('users.allRoles') }}</option>
            <option v-for="role in roles" :key="role.id" :value="role.id">
              {{ role.name }}
            </option>
          </Field>
        </div>
        <div>
          <label class="form-label">{{ $t('users.status') }}</label>
          <Field
            name="status"
            as="select"
            class="input-primary"
          >
            <option value="">{{ $t('users.allStatuses') }}</option>
            <option value="active">{{ $t('users.active') }}</option>
            <option value="inactive">{{ $t('users.inactive') }}</option>
          </Field>
        </div>
      </Form>
    </div>

    <!-- Users Table -->
    <div class="card-container">
      <div class="overflow-x-auto">
        <table class="table w-full">
          <thead>
            <tr>
              <th>{{ $t('users.name') }}</th>
              <th>{{ $t('users.email') }}</th>
              <th>{{ $t('users.roles') }}</th>
              <th>{{ $t('users.status') }}</th>
              <th>{{ $t('users.lastLogin') }}</th>
              <th>{{ $t('users.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>
                <div class="flex items-center space-x-3">
                  <div class="avatar placeholder">
                    <div class="bg-neutral text-neutral-content rounded-full w-8">
                      <span class="text-xs">{{ getUserInitials(user.name) }}</span>
                    </div>
                  </div>
                  <div>{{ user.name }}</div>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="role in user.roles"
                    :key="role.id"
                    class="badge badge-primary badge-sm"
                  >
                    {{ role.name }}
                  </span>
                </div>
              </td>
              <td>
                <span
                  class="badge"
                  :class="{
                    'badge-success': user.status === 'active',
                    'badge-error': user.status === 'inactive'
                  }"
                >
                  {{ $t(`users.${user.status}`) }}
                </span>
              </td>
              <td>{{ formatDate(user.last_login) }}</td>
              <td>
                <div class="flex space-x-2">
                  <button
                    v-if="hasPermission('edit_users')"
                    class="btn btn-ghost btn-sm"
                    @click="openUserModal(user)"
                  >
                    <PencilIcon class="h-4 w-4" />
                  </button>
                  <button
                    v-if="hasPermission('delete_users')"
                    class="btn btn-ghost btn-sm text-error"
                    @click="confirmDelete(user)"
                  >
                    <TrashIcon class="h-4 w-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="mt-4">
        <Pagination
          :total="totalItems"
          :per-page="perPage"
          :current-page="currentPage"
          @page-changed="handlePageChange"
        />
      </div>
    </div>

    <!-- User Modal -->
    <UserModal
      v-if="showUserModal"
      :user="selectedUser"
      :roles="roles"
      @close="closeUserModal"
      @save="handleSaveUser"
    />

    <!-- Import Modal -->
    <ImportModal
      v-if="showImportModal"
      @close="closeImportModal"
      @import="handleImport"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      v-if="showDeleteModal"
      :title="$t('users.deleteTitle')"
      :message="$t('users.deleteMessage', { name: selectedUser?.name })"
      @confirm="handleDelete"
      @cancel="closeDeleteModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Form, Field } from 'vee-validate'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { userService } from '../services/userService'
import { useAuthStore } from '@/core/store/auth'
import { useNotification } from '@/shared/composables/useNotification'
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  ArrowUpTrayIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'
import UserModal from '../components/UserModal.vue'
import ImportModal from '../components/ImportModal.vue'
import ConfirmationModal from '@/shared/components/common/ConfirmationModal.vue'
import Pagination from '@/shared/components/common/Pagination.vue'

const authStore = useAuthStore()
const notification = useNotification()

// State
const users = ref([])
const roles = ref([])
const selectedUser = ref(null)
const showUserModal = ref(false)
const showImportModal = ref(false)
const showDeleteModal = ref(false)
const currentPage = ref(1)
const perPage = ref(10)
const totalItems = ref(0)
const filters = ref({
  search: '',
  role: '',
  status: ''
})

// Methods
const hasPermission = (permission) => {
  return authStore.hasPermission(permission)
}

const getUserInitials = (name) => {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const formatDate = (date) => {
  if (!date) return '-'
  return format(new Date(date), 'dd/MM/yyyy HH:mm', { locale: ptBR })
}

const fetchUsers = async () => {
  try {
    const params = {
      page: currentPage.value,
      per_page: perPage.value,
      ...filters.value
    }
    const response = await userService.getUsers(params)
    users.value = response.data.items
    totalItems.value = response.data.total
  } catch (error) {
    notification.error(error.message)
  }
}

const fetchRoles = async () => {
  try {
    const response = await roleService.getRoles()
    roles.value = response.data
  } catch (error) {
    notification.error(error.message)
  }
}

const handleFilter = (values) => {
  filters.value = values
  currentPage.value = 1
  fetchUsers()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchUsers()
}

const openUserModal = (user = null) => {
  selectedUser.value = user
  showUserModal.value = true
}

const closeUserModal = () => {
  selectedUser.value = null
  showUserModal.value = false
}

const handleSaveUser = async (userData) => {
  try {
    if (selectedUser.value) {
      await userService.updateUser(selectedUser.value.id, userData)
      notification.success('users.updateSuccess')
    } else {
      await userService.createUser(userData)
      notification.success('users.createSuccess')
    }
    closeUserModal()
    fetchUsers()
  } catch (error) {
    notification.error(error.message)
  }
}

const confirmDelete = (user) => {
  selectedUser.value = user
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  selectedUser.value = null
  showDeleteModal.value = false
}

const handleDelete = async () => {
  try {
    await userService.deleteUser(selectedUser.value.id)
    notification.success('users.deleteSuccess')
    closeDeleteModal()
    fetchUsers()
  } catch (error) {
    notification.error(error.message)
  }
}

const exportUsers = async () => {
  try {
    const response = await userService.exportUsers()
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'users.csv')
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    notification.error(error.message)
  }
}

const handleImport = async (file) => {
  try {
    await userService.importUsers(file)
    notification.success('users.importSuccess')
    closeImportModal()
    fetchUsers()
  } catch (error) {
    notification.error(error.message)
  }
}

// Lifecycle
onMounted(() => {
  fetchUsers()
  fetchRoles()
})
</script>
