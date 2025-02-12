<template>
  <div class="min-h-screen bg-base-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-base-content">
          {{ $t('auth.resetPassword') }}
        </h2>
        <p class="mt-2 text-center text-sm text-base-content/60">
          {{ $t('auth.resetPasswordDescription') }}
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleResetPassword">
        <div class="rounded-md shadow-sm space-y-4">
          <!-- Nova Senha -->
          <div>
            <label for="password" class="form-label">{{ $t('auth.newPassword') }}</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="input-primary"
              :placeholder="$t('auth.newPassword')"
            />
            <p v-if="errors.password" class="form-error">{{ errors.password }}</p>
          </div>

          <!-- Confirmar Nova Senha -->
          <div>
            <label for="confirmPassword" class="form-label">{{ $t('auth.confirmPassword') }}</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              required
              class="input-primary"
              :placeholder="$t('auth.confirmPassword')"
            />
            <p v-if="errors.confirmPassword" class="form-error">{{ errors.confirmPassword }}</p>
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
            {{ $t('auth.resetPassword') }}
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
          <span>{{ $t('auth.passwordResetSuccess') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/core/store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const success = ref(false)
const token = ref('')

const form = ref({
  password: '',
  confirmPassword: ''
})

const errors = ref({
  password: '',
  confirmPassword: ''
})

const validateForm = () => {
  let isValid = true
  errors.value = {
    password: '',
    confirmPassword: ''
  }

  if (!form.value.password) {
    errors.value.password = 'Nova senha é obrigatória'
    isValid = false
  } else if (form.value.password.length < 8) {
    errors.value.password = 'A senha deve ter pelo menos 8 caracteres'
    isValid = false
  }

  if (!form.value.confirmPassword) {
    errors.value.confirmPassword = 'Confirmação de senha é obrigatória'
    isValid = false
  } else if (form.value.password !== form.value.confirmPassword) {
    errors.value.confirmPassword = 'As senhas não coincidem'
    isValid = false
  }

  return isValid
}

const handleResetPassword = async () => {
  if (!validateForm()) return

  loading.value = true
  try {
    await authStore.resetPassword({
      token: token.value,
      password: form.value.password
    })
    success.value = true
    setTimeout(() => {
      router.push({ name: 'Login' })
    }, 2000)
  } catch (error) {
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else {
      console.error('Erro ao redefinir senha:', error)
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  token.value = route.query.token
  if (!token.value) {
    router.push({ name: 'Login' })
  }
})
</script>
