<template>
  <div class="modal modal-open">
    <div class="modal-box relative">
      <button
        class="btn btn-sm btn-circle absolute right-2 top-2"
        @click="$emit('close')"
      >
        ✕
      </button>
      
      <h3 class="text-lg font-bold mb-4">
        {{ $t('auth.2faVerification') }}
      </h3>

      <Form @submit="handleSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }">
        <div class="space-y-4">
          <p class="text-sm text-gray-600">
            {{ $t('auth.2faInstructions') }}
          </p>

          <div>
            <label for="code" class="form-label">{{ $t('auth.2faCode') }}</label>
            <Field
              id="code"
              name="code"
              type="text"
              required
              class="input-primary"
              :class="{ 'input-error': errors.code }"
              maxlength="6"
              autocomplete="one-time-code"
              v-model="code"
            />
            <ErrorMessage name="code" class="form-error" />
          </div>

          <div class="mt-6">
            <button
              type="submit"
              class="btn-primary w-full"
              :class="{ 'loading': isSubmitting }"
              :disabled="isSubmitting"
            >
              {{ $t('auth.verify') }}
            </button>
          </div>
        </div>
      </Form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { object, string } from 'yup'

const props = defineProps({
  email: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['verify', 'close'])

const code = ref('')

const schema = object({
  code: string()
    .required('auth.2faCodeRequired')
    .matches(/^[0-9]{6}$/, 'auth.2faCodeInvalid')
})

const handleSubmit = async (values) => {
  emit('verify', values.code)
}
</script>
