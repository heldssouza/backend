<template>
  <div class="flex items-center justify-between">
    <!-- Mobile view -->
    <div class="flex flex-1 justify-between sm:hidden">
      <button
        class="btn btn-ghost btn-sm"
        :disabled="currentPage === 1"
        @click="handlePageChange(currentPage - 1)"
      >
        {{ $t('pagination.previous') }}
      </button>
      <button
        class="btn btn-ghost btn-sm"
        :disabled="currentPage === totalPages"
        @click="handlePageChange(currentPage + 1)"
      >
        {{ $t('pagination.next') }}
      </button>
    </div>

    <!-- Desktop view -->
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700">
          {{ $t('pagination.showing') }}
          <span class="font-medium">{{ startItem }}</span>
          {{ $t('pagination.to') }}
          <span class="font-medium">{{ endItem }}</span>
          {{ $t('pagination.of') }}
          <span class="font-medium">{{ total }}</span>
          {{ $t('pagination.results') }}
        </p>
      </div>

      <div>
        <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
          <!-- Previous -->
          <button
            class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
            :class="{ 'cursor-not-allowed opacity-50': currentPage === 1 }"
            :disabled="currentPage === 1"
            @click="handlePageChange(currentPage - 1)"
          >
            <span class="sr-only">{{ $t('pagination.previous') }}</span>
            <ChevronLeftIcon class="h-5 w-5" aria-hidden="true" />
          </button>

          <!-- Pages -->
          <template v-for="page in displayedPages" :key="page">
            <span
              v-if="page === '...'"
              class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-inset ring-gray-300"
            >
              ...
            </span>
            <button
              v-else
              class="relative inline-flex items-center px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300"
              :class="[
                currentPage === page
                  ? 'z-10 bg-primary text-white focus-visible:outline-offset-0'
                  : 'text-gray-900 hover:bg-gray-50'
              ]"
              @click="handlePageChange(page)"
            >
              {{ page }}
            </button>
          </template>

          <!-- Next -->
          <button
            class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
            :class="{ 'cursor-not-allowed opacity-50': currentPage === totalPages }"
            :disabled="currentPage === totalPages"
            @click="handlePageChange(currentPage + 1)"
          >
            <span class="sr-only">{{ $t('pagination.next') }}</span>
            <ChevronRightIcon class="h-5 w-5" aria-hidden="true" />
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/20/solid'

const props = defineProps({
  total: {
    type: Number,
    required: true
  },
  perPage: {
    type: Number,
    required: true
  },
  currentPage: {
    type: Number,
    required: true
  },
  maxVisiblePages: {
    type: Number,
    default: 5
  }
})

const emit = defineEmits(['page-changed'])

const totalPages = computed(() => Math.ceil(props.total / props.perPage))
const startItem = computed(() => ((props.currentPage - 1) * props.perPage) + 1)
const endItem = computed(() => Math.min(props.currentPage * props.perPage, props.total))

const displayedPages = computed(() => {
  const pages = []
  const maxPages = props.maxVisiblePages
  const halfMaxPages = Math.floor(maxPages / 2)

  let startPage = props.currentPage - halfMaxPages
  let endPage = props.currentPage + halfMaxPages

  if (startPage <= 0) {
    startPage = 1
    endPage = Math.min(maxPages, totalPages.value)
  }

  if (endPage > totalPages.value) {
    endPage = totalPages.value
    startPage = Math.max(1, endPage - maxPages + 1)
  }

  // Always show first page
  if (startPage > 1) {
    pages.push(1)
    if (startPage > 2) pages.push('...')
  }

  // Add pages
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }

  // Always show last page
  if (endPage < totalPages.value) {
    if (endPage < totalPages.value - 1) pages.push('...')
    pages.push(totalPages.value)
  }

  return pages
})

const handlePageChange = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    emit('page-changed', page)
  }
}
</script>
