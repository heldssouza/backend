<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold">{{ $t('tenants.title') }}</h1>
        <p class="text-gray-600">{{ $t('tenants.description') }}</p>
      </div>
      <button
        class="btn btn-primary"
        @click="showCreateModal = true"
      >
        <PlusIcon class="h-5 w-5 mr-2" />
        {{ $t('tenants.create') }}
      </button>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- Search -->
        <div>
          <label class="form-label">{{ $t('common.search') }}</label>
          <div class="relative">
            <input
              v-model="search"
              type="text"
              class="input input-bordered w-full pl-10"
              :placeholder="$t('tenants.searchPlaceholder')"
            />
            <MagnifyingGlassIcon class="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
          </div>
        </div>

        <!-- Status -->
        <div>
          <label class="form-label">{{ $t('common.status') }}</label>
          <select
            v-model="status"
            class="select select-bordered w-full"
          >
            <option value="">{{ $t('common.all') }}</option>
            <option value="active">{{ $t('common.active') }}</option>
            <option value="inactive">{{ $t('common.inactive') }}</option>
          </select>
        </div>

        <!-- Sort By -->
        <div>
          <label class="form-label">{{ $t('common.sortBy') }}</label>
          <select
            v-model="sortBy"
            class="select select-bordered w-full"
          >
            <option value="createdAt">{{ $t('common.createdAt') }}</option>
            <option value="name">{{ $t('common.name') }}</option>
            <option value="domain">{{ $t('tenants.domain') }}</option>
            <option value="status">{{ $t('common.status') }}</option>
          </select>
        </div>

        <!-- Sort Order -->
        <div>
          <label class="form-label">{{ $t('common.sortOrder') }}</label>
          <select
            v-model="sortOrder"
            class="select select-bordered w-full"
          >
            <option value="desc">{{ $t('common.descending') }}</option>
            <option value="asc">{{ $t('common.ascending') }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="overflow-x-auto">
        <table class="table w-full">
          <thead>
            <tr>
              <th>{{ $t('common.name') }}</th>
              <th>{{ $t('tenants.domain') }}</th>
              <th>{{ $t('common.status') }}</th>
              <th>{{ $t('tenants.users') }}</th>
              <th>{{ $t('common.createdAt') }}</th>
              <th>{{ $t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="tenantStore.loading">
              <td colspan="6" class="text-center py-4">
                <div class="loading loading-spinner loading-lg"></div>
              </td>
            </tr>
            <tr v-else-if="tenantStore.error">
              <td colspan="6" class="text-center py-4 text-error">
                {{ tenantStore.error }}
              </td>
            </tr>
            <tr v-else-if="!tenantStore.tenants.length">
              <td colspan="6" class="text-center py-4">
                {{ $t('tenants.noTenants') }}
              </td>
            </tr>
            <tr
              v-for="tenant in tenantStore.tenants"
              :key="tenant.id"
              class="hover"
            >
              <td>
                <div class="font-medium">{{ tenant.name }}</div>
                <div class="text-sm text-gray-500">{{ tenant.description }}</div>
              </td>
              <td>
                <a
                  :href="'https://' + tenant.domain"
                  target="_blank"
                  class="link link-primary"
                >
                  {{ tenant.domain }}
                </a>
              </td>
              <td>
                <span
                  class="badge"
                  :class="{
                    'badge-success': tenant.status === 'active',
                    'badge-error': tenant.status === 'inactive'
                  }"
                >
                  {{ tenant.status }}
                </span>
              </td>
              <td>{{ tenant.usersCount }}</td>
              <td>{{ formatDate(tenant.createdAt) }}</td>
              <td>
                <div class="flex items-center space-x-2">
                  <button
                    class="btn btn-ghost btn-sm"
                    @click="handleEdit(tenant)"
                  >
                    <PencilIcon class="h-4 w-4" />
                  </button>
                  <button
                    class="btn btn-ghost btn-sm"
                    @click="handleToggleStatus(tenant)"
                  >
                    <PowerIcon class="h-4 w-4" />
                  </button>
                  <button
                    class="btn btn-ghost btn-sm text-error"
                    @click="handleDelete(tenant)"
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
      <div class="p-4 border-t">
        <Pagination
          :total="tenantStore.pagination.total"
          :per-page="tenantStore.pagination.perPage"
          :current-page="tenantStore.pagination.page"
          @page-changed="handlePageChange"
        />
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <TenantModal
      v-if="showCreateModal || editingTenant"
      :tenant="editingTenant"
      @save="handleSave"
      @close="closeModal"
    />

    <!-- Confirmation Modal -->
    <ConfirmationModal
      v-if="showDeleteModal"
      :title="$t('tenants.deleteTitle')"
      :message="$t('tenants.deleteMessage', { name: deletingTenant?.name })"
      @confirm="confirmDelete"
      @cancel="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useTenantStore } from '../store/tenantStore'
import { useI18n } from 'vue-i18n'
import { useNotification } from '@/shared/composables/useNotification'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  PencilIcon,
  TrashIcon,
  PowerIcon
} from '@heroicons/vue/24/outline'
import Pagination from '@/shared/components/common/Pagination.vue'
import TenantModal from '../components/TenantModal.vue'
import ConfirmationModal from '@/shared/components/common/ConfirmationModal.vue'
import { formatDate } from '@/utils/dateUtils'

const { t } = useI18n()
const notification = useNotification()
const tenantStore = useTenantStore()

// Refs
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const editingTenant = ref(null)
const deletingTenant = ref(null)

// Search and filters
const search = ref('')
const status = ref('')
const sortBy = ref('createdAt')
const sortOrder = ref('desc')

// Watch for filter changes
watch([search, status, sortBy, sortOrder], () => {
  tenantStore.setFilters({
    search: search.value,
    status: status.value,
    sortBy: sortBy.value,
    sortOrder: sortOrder.value
  })
  loadTenants()
}, { debounce: 300 })

// Methods
const loadTenants = async () => {
  try {
    await tenantStore.fetchTenants()
  } catch (error) {
    notification.showError(error.message)
  }
}

const handlePageChange = (page) => {
  tenantStore.setPagination({ page })
  loadTenants()
}

const handleEdit = (tenant) => {
  editingTenant.value = tenant
}

const handleDelete = (tenant) => {
  deletingTenant.value = tenant
  showDeleteModal.value = true
}

const handleToggleStatus = async (tenant) => {
  try {
    await tenantStore.toggleTenantStatus(tenant.id, tenant.status === 'inactive')
    notification.showSuccess(t('tenants.statusChanged', { name: tenant.name }))
    loadTenants()
  } catch (error) {
    notification.showError(error.message)
  }
}

const handleSave = async (tenantData) => {
  try {
    if (editingTenant.value) {
      await tenantStore.updateTenant(editingTenant.value.id, tenantData)
      notification.showSuccess(t('tenants.updated'))
    } else {
      await tenantStore.createTenant(tenantData)
      notification.showSuccess(t('tenants.created'))
    }
    closeModal()
    loadTenants()
  } catch (error) {
    notification.showError(error.message)
  }
}

const confirmDelete = async () => {
  if (!deletingTenant.value) return

  try {
    await tenantStore.deleteTenant(deletingTenant.value.id)
    notification.showSuccess(t('tenants.deleted', { name: deletingTenant.value.name }))
    showDeleteModal.value = false
    deletingTenant.value = null
    loadTenants()
  } catch (error) {
    notification.showError(error.message)
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingTenant.value = null
}

// Lifecycle
onMounted(() => {
  loadTenants()
})
</script>
