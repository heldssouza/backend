<template>
  <div class="modal modal-open">
    <div class="modal-box">
      <button
        class="btn btn-sm btn-circle absolute right-2 top-2"
        @click="$emit('cancel')"
      >
        ✕
      </button>
      
      <h3 class="text-lg font-bold mb-4">
        {{ title }}
      </h3>

      <p class="text-gray-600">
        {{ message }}
      </p>

      <div class="modal-action">
        <button
          type="button"
          class="btn btn-ghost"
          @click="$emit('cancel')"
        >
          {{ $t('common.cancel') }}
        </button>
        <button
          type="button"
          class="btn btn-error"
          :class="{ 'loading': loading }"
          :disabled="loading"
          @click="handleConfirm"
        >
          {{ confirmText || $t('common.confirm') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['confirm', 'cancel'])

const loading = ref(false)

const handleConfirm = async () => {
  loading.value = true
  try {
    await emit('confirm')
  } finally {
    loading.value = false
  }
}
</script>
