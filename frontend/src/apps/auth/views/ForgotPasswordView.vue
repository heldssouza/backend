<template>
  <div class="min-h-screen bg-base-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-base-content">
          {{ $t('auth.forgotPassword') }}
        </h2>
        <p class="mt-2 text-center text-sm text-base-content/60">
          {{ $t('auth.forgotPasswordDescription') }}
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleForgotPassword">
        <div class="rounded-md shadow-sm space-y-4">
          <!-- Email -->
          <div>
            <label for="email" class="form-label">{{ $t('auth.email') }}</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="input-primary"
              :placeholder="$t('auth.email')"
            />
            <p v-if="error" class="form-error">{{ error }}</p>
          </div>
        </div>

        <!-- Botões -->
        <div class="flex flex-col space-y-4">
          <button
            type="submit"
            class="btn btn-primary w-full"
            :disabled="loading"
          >
            <span v-if="loading" class="loading loading-spinner"></span>
            {{ $t('auth.sendResetLink') }}
          </button>

          <div class="text-center">
            <router-link
              :to="{ name: 'Login' }"
              class="font-medium text-primary hover:text-primary/80"
            >
              {{ $t('auth.backToLogin') }}
            </router-link>
          </div>
        </div>
      </form>

      <!-- Mensagem de Sucesso -->
      <div v-if="success" class="alert alert-success shadow-lg">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ $t('auth.resetLinkSent') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/core/store/auth'

const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')
const success = ref(false)
const form = ref({
  email: ''
})

const handleForgotPassword = async () => {
  loading.value = true
  error.value = ''
  success.value = false

  try {
    await authStore.forgotPassword(form.value.email)
    success.value = true
    form.value.email = ''
  } catch (err) {
    error.value = err.response?.data?.message || 'Erro ao enviar o link de redefinição'
  } finally {
    loading.value = false
  }
}
</script>
