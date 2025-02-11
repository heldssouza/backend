<template>
  <div class="overflow-x-auto bg-white rounded-lg shadow">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th v-if="selectable" scope="col" class="w-12 px-6 py-3">
            <input
              type="checkbox"
              class="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              :checked="allSelected"
              @change="toggleAll"
            />
          </th>
          <th
            v-for="column in columns"
            :key="column.key"
            scope="col"
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            :class="{ 'cursor-pointer': column.sortable }"
            @click="column.sortable && sort(column.key)"
          >
            {{ column.label }}
            <span v-if="column.sortable" class="ml-1">
              ↑↓
            </span>
          </th>
          <th v-if="actions" scope="col" class="relative px-6 py-3">
            <span class="sr-only">Ações</span>
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="item in paginatedData" :key="item.id" class="hover:bg-gray-50">
          <td v-if="selectable" class="px-6 py-4 whitespace-nowrap">
            <input
              type="checkbox"
              class="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              :checked="selectedItems.includes(item.id)"
              @change="toggleItem(item.id)"
            />
          </td>
          <td
            v-for="column in columns"
            :key="column.key"
            class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
          >
            {{ item[column.key] }}
          </td>
          <td v-if="actions" class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
            <slot name="actions" :item="item"></slot>
          </td>
        </tr>
      </tbody>
    </table>
    
    <!-- Paginação -->
    <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
      <div class="flex-1 flex justify-between sm:hidden">
        <button
          @click="previousPage"
          :disabled="currentPage === 1"
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
        >
          Anterior
        </button>
        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }"
        >
          Próximo
        </button>
      </div>
      <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700">
            Mostrando
            <span class="font-medium">{{ startIndex + 1 }}</span>
            a
            <span class="font-medium">{{ endIndex }}</span>
            de
            <span class="font-medium">{{ totalItems }}</span>
            resultados
          </p>
        </div>
        <div>
          <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
            <button
              @click="previousPage"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
              :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
            >
              Anterior
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
              :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }"
            >
              Próximo
            </button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  },
  itemsPerPage: {
    type: Number,
    default: 10
  },
  selectable: {
    type: Boolean,
    default: false
  },
  actions: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:selected', 'sort'])

const currentPage = ref(1)
const selectedItems = ref([])
const sortKey = ref('')
const sortOrder = ref('asc')

const totalItems = computed(() => props.data.length)
const totalPages = computed(() => Math.ceil(totalItems.value / props.itemsPerPage))
const startIndex = computed(() => (currentPage.value - 1) * props.itemsPerPage)
const endIndex = computed(() => Math.min(startIndex.value + props.itemsPerPage, totalItems.value))

const paginatedData = computed(() => {
  return props.data.slice(startIndex.value, endIndex.value)
})

const allSelected = computed(() => {
  return paginatedData.value.length > 0 && 
         paginatedData.value.every(item => selectedItems.value.includes(item.id))
})

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

function toggleAll() {
  if (allSelected.value) {
    selectedItems.value = selectedItems.value.filter(
      id => !paginatedData.value.some(item => item.id === id)
    )
  } else {
    const newSelected = new Set(selectedItems.value)
    paginatedData.value.forEach(item => newSelected.add(item.id))
    selectedItems.value = Array.from(newSelected)
  }
  emit('update:selected', selectedItems.value)
}

function toggleItem(id) {
  const index = selectedItems.value.indexOf(id)
  if (index === -1) {
    selectedItems.value.push(id)
  } else {
    selectedItems.value.splice(index, 1)
  }
  emit('update:selected', selectedItems.value)
}

function sort(key) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  emit('sort', { key, order: sortOrder.value })
}
</script>
