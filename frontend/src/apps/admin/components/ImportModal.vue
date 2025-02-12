<template>
  <div class="modal modal-open">
    <div class="modal-box">
      <button
        class="btn btn-sm btn-circle absolute right-2 top-2"
        @click="$emit('close')"
      >
        ✕
      </button>
      
      <h3 class="text-lg font-bold mb-4">
        {{ $t('users.importUsers') }}
      </h3>

      <div class="space-y-4">
        <!-- Instructions -->
        <div class="bg-info/10 p-4 rounded-lg">
          <h4 class="font-medium mb-2">{{ $t('users.importInstructions') }}</h4>
          <ul class="list-disc list-inside text-sm space-y-1">
            <li>{{ $t('users.importFormat') }}</li>
            <li>{{ $t('users.importRequired') }}</li>
            <li>{{ $t('users.importLimit') }}</li>
          </ul>
        </div>

        <!-- File Upload -->
        <div class="space-y-2">
          <label class="form-label">{{ $t('users.selectFile') }}</label>
          <div
            class="border-2 border-dashed border-gray-300 rounded-lg p-6"
            :class="{ 'border-primary': isDragging }"
            @dragenter.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @dragover.prevent
            @drop.prevent="handleDrop"
          >
            <div class="text-center">
              <CloudArrowUpIcon
                class="mx-auto h-12 w-12 text-gray-400"
                aria-hidden="true"
              />
              <div class="mt-2">
                <label
                  for="file-upload"
                  class="btn btn-ghost btn-sm normal-case"
                >
                  {{ $t('users.selectFileButton') }}
                </label>
                <input
                  id="file-upload"
                  type="file"
                  class="hidden"
                  accept=".csv"
                  @change="handleFileSelect"
                />
              </div>
              <p class="text-xs text-gray-500 mt-2">
                {{ $t('users.dragAndDrop') }}
              </p>
            </div>
          </div>
        </div>

        <!-- Selected File -->
        <div v-if="selectedFile" class="flex items-center justify-between p-2 bg-base-200 rounded">
          <div class="flex items-center space-x-2">
            <DocumentIcon class="h-5 w-5 text-primary" />
            <span class="text-sm">{{ selectedFile.name }}</span>
          </div>
          <button
            class="btn btn-ghost btn-sm"
            @click="selectedFile = null"
          >
            <XMarkIcon class="h-5 w-5" />
          </button>
        </div>

        <!-- Template Download -->
        <div class="text-center">
          <button
            class="btn btn-ghost btn-sm normal-case"
            @click="downloadTemplate"
          >
            <ArrowDownTrayIcon class="h-5 w-5 mr-2" />
            {{ $t('users.downloadTemplate') }}
          </button>
        </div>

        <!-- Actions -->
        <div class="modal-action">
          <button
            type="button"
            class="btn btn-ghost"
            @click="$emit('close')"
          >
            {{ $t('common.cancel') }}
          </button>
          <button
            type="button"
            class="btn btn-primary"
            :disabled="!selectedFile || isImporting"
            :class="{ 'loading': isImporting }"
            @click="handleImport"
          >
            {{ $t('users.startImport') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  CloudArrowUpIcon,
  DocumentIcon,
  XMarkIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'

const emit = defineEmits(['close', 'import'])

const isDragging = ref(false)
const selectedFile = ref(null)
const isImporting = ref(false)

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file && file.type === 'text/csv') {
    selectedFile.value = file
  }
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
  }
}

const downloadTemplate = () => {
  // Template CSV content
  const template = 'name,email,status,roles\nJohn Doe,john@example.com,active,"admin,user"\n'
  const blob = new Blob([template], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'users_template.csv')
  document.body.appendChild(link)
  link.click()
  link.remove()
}

const handleImport = async () => {
  if (!selectedFile.value) return

  isImporting.value = true
  try {
    await emit('import', selectedFile.value)
  } finally {
    isImporting.value = false
  }
}
</script>
