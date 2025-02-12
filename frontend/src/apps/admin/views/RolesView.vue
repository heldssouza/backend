<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold">{{ $t('roles.title') }}</h1>
        <p class="text-gray-600">{{ $t('roles.description') }}</p>
      </div>
      <button
        class="btn btn-primary"
        @click="showCreateModal = true"
      >
        <PlusIcon class="h-5 w-5 mr-2" />
        {{ $t('roles.create') }}
      </button>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Search -->
        <div>
          <label class="form-label">{{ $t('common.search') }}</label>
          <div class="relative">
            <input
              v-model="search"
              type="text"
              class="input input-bordered w-full pl-10"
              :placeholder="$t('roles.searchPlaceholder')"
            />
            <MagnifyingGlassIcon class="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
          </div>
        </div>

        <!-- Sort By -->
        <div>
          <label class="form-label">{{ $t('common.sortBy') }}</label>
          <select
            v-model="sortBy"
            class="select select-bordered w-full"
          >
            <option value="name">{{ $t('common.name') }}</option>
            <option value="priority">{{ $t('roles.priority') }}</option>
            <option value="createdAt">{{ $t('common.createdAt') }}</option>
          </select>
        </div>

        <!-- Sort Order -->
        <div>
          <label class="form-label">{{ $t('common.sortOrder') }}</label>
          <select
            v-model="sortOrder"
            class="select select-bordered w-full"
          >
            <option value="asc">{{ $t('common.ascending') }}</option>
            <option value="desc">{{ $t('common.descending') }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Roles List -->
    <div class="space-y-6">
      <!-- System Roles -->
      <div>
        <h2 class="text-lg font-medium mb-4">{{ $t('roles.systemRoles') }}</h2>
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="overflow-x-auto">
            <table class="table w-full">
              <thead>
                <tr>
                  <th>{{ $t('common.name') }}</th>
                  <th>{{ $t('common.description') }}</th>
                  <th>{{ $t('roles.users') }}</th>
                  <th>{{ $t('roles.permissions') }}</th>
                  <th>{{ $t('roles.priority') }}</th>
                  <th>{{ $t('common.actions') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="roleStore.loading">
                  <td colspan="6" class="text-center py-4">
                    <div class="loading loading-spinner loading-lg"></div>
                  </td>
                </tr>
                <tr
                  v-else-if="roleStore.systemRoles.length"
                  v-for="role in roleStore.systemRoles"
                  :key="role.id"
                  class="hover"
                >
                  <td>
                    <div class="font-medium">{{ role.name }}</div>
                    <div
                      v-if="role.isDefault"
                      class="badge badge-sm badge-primary mt-1"
                    >
                      {{ $t('roles.default') }}
                    </div>
                  </td>
                  <td>{{ role.description }}</td>
                  <td>{{ role.usersCount }}</td>
                  <td>{{ role.permissions.length }}</td>
                  <td>{{ role.priority }}</td>
                  <td>
                    <button
                      class="btn btn-ghost btn-sm"
                      @click="handleEdit(role)"
                    >
                      <EyeIcon class="h-4 w-4" />
                    </button>
                  </td>
                </tr>
                <tr v-else>
                  <td colspan="6" class="text-center py-4">
                    {{ $t('roles.noSystemRoles') }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Custom Roles -->
      <div>
        <h2 class="text-lg font-medium mb-4">{{ $t('roles.customRoles') }}</h2>
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="overflow-x-auto">
            <table class="table w-full">
              <thead>
                <tr>
                  <th>{{ $t('common.name') }}</th>
                  <th>{{ $t('common.description') }}</th>
                  <th>{{ $t('roles.users') }}</th>
                  <th>{{ $t('roles.permissions') }}</th>
                  <th>{{ $t('roles.priority') }}</th>
                  <th>{{ $t('common.actions') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="roleStore.loading">
                  <td colspan="6" class="text-center py-4">
                    <div class="loading loading-spinner loading-lg"></div>
                  </td>
                </tr>
                <tr
                  v-else-if="roleStore.customRoles.length"
                  v-for="role in roleStore.customRoles"
                  :key="role.id"
                  class="hover"
                >
                  <td>
                    <div class="font-medium">{{ role.name }}</div>
                    <div
                      v-if="role.isDefault"
                      class="badge badge-sm badge-primary mt-1"
                    >
                      {{ $t('roles.default') }}
                    </div>
                  </td>
                  <td>{{ role.description }}</td>
                  <td>{{ role.usersCount }}</td>
                  <td>{{ role.permissions.length }}</td>
                  <td>{{ role.priority }}</td>
                  <td>
                    <div class="flex items-center space-x-2">
                      <button
                        class="btn btn-ghost btn-sm"
                        @click="handleEdit(role)"
                      >
                        <PencilIcon class="h-4 w-4" />
                      </button>
                      <button
                        class="btn btn-ghost btn-sm text-error"
                        @click="handleDelete(role)"
                      >
                        <TrashIcon class="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-else>
                  <td colspan="6" class="text-center py-4">
                    {{ $t('roles.noCustomRoles') }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="p-4 border-t">
            <Pagination
              :total="roleStore.pagination.total"
              :per-page="roleStore.pagination.perPage"
              :current-page="roleStore.pagination.page"
              @page-changed="handlePageChange"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <RoleModal
      v-if="showCreateModal || editingRole"
      :role="editingRole"
      @save="handleSave"
      @close="closeModal"
    />

    <!-- Confirmation Modal -->
    <ConfirmationModal
      v-if="showDeleteModal"
      :title="$t('roles.deleteTitle')"
      :message="$t('roles.deleteMessage', { name: deletingRole?.name })"
      @confirm="confirmDelete"
      @cancel="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRoleStore } from '../store/roleStore'
import { useI18n } from 'vue-i18n'
import { useNotification } from '@/shared/composables/useNotification'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon
} from '@heroicons/vue/24/outline'
import Pagination from '@/shared/components/common/Pagination.vue'
import RoleModal from '../components/RoleModal.vue'
import ConfirmationModal from '@/shared/components/common/ConfirmationModal.vue'

const { t } = useI18n()
const notification = useNotification()
const roleStore = useRoleStore()

// Refs
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const editingRole = ref(null)
const deletingRole = ref(null)

// Search and filters
const search = ref('')
const sortBy = ref('name')
const sortOrder = ref('asc')

// Watch for filter changes
watch([search, sortBy, sortOrder], () => {
  roleStore.setFilters({
    search: search.value,
    sortBy: sortBy.value,
    sortOrder: sortOrder.value
  })
  loadRoles()
}, { debounce: 300 })

// Methods
const loadRoles = async () => {
  try {
    await roleStore.fetchRoles()
  } catch (error) {
    notification.showError(error.message)
  }
}

const handlePageChange = (page) => {
  roleStore.setPagination({ page })
  loadRoles()
}

const handleEdit = (role) => {
  editingRole.value = role
}

const handleDelete = (role) => {
  deletingRole.value = role
  showDeleteModal.value = true
}

const handleSave = async (roleData) => {
  try {
    if (editingRole.value) {
      await roleStore.updateRole(editingRole.value.id, roleData)
      notification.showSuccess(t('roles.updated'))
    } else {
      await roleStore.createRole(roleData)
      notification.showSuccess(t('roles.created'))
    }
    closeModal()
  } catch (error) {
    notification.showError(error.message)
  }
}

const confirmDelete = async () => {
  if (!deletingRole.value) return

  try {
    await roleStore.deleteRole(deletingRole.value.id)
    notification.showSuccess(t('roles.deleted', { name: deletingRole.value.name }))
    showDeleteModal.value = false
    deletingRole.value = null
  } catch (error) {
    notification.showError(error.message)
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingRole.value = null
}

// Lifecycle
onMounted(async () => {
  try {
    await Promise.all([
      loadRoles(),
      roleStore.fetchAvailablePermissions()
    ])
  } catch (error) {
    notification.showError(error.message)
  }
})
</script>
