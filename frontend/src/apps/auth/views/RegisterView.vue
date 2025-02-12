<template>
  <div class="min-h-screen bg-base-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-base-content">
          {{ $t('auth.register') }}
        </h2>
        <p class="mt-2 text-center text-sm text-base-content/60">
          {{ $t('auth.alreadyHaveAccount') }}
          <router-link :to="{ name: 'Login' }" class="font-medium text-primary hover:text-primary/80">
            {{ $t('auth.login') }}
          </router-link>
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="rounded-md shadow-sm space-y-4">
          <!-- Nome -->
          <div>
            <label for="firstName" class="form-label">{{ $t('users.firstName') }}</label>
            <input
              id="firstName"
              v-model="form.firstName"
              type="text"
              required
              class="input-primary"
              :placeholder="$t('users.firstName')"
            />
            <p v-if="errors.firstName" class="form-error">{{ errors.firstName }}</p>
          </div>

          <!-- Sobrenome -->
          <div>
            <label for="lastName" class="form-label">{{ $t('users.lastName') }}</label>
            <input
              id="lastName"
              v-model="form.lastName"
              type="text"
              required
              class="input-primary"
              :placeholder="$t('users.lastName')"
            />
            <p v-if="errors.lastName" class="form-error">{{ errors.lastName }}</p>
          </div>

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
            <p v-if="errors.email" class="form-error">{{ errors.email }}</p>
          </div>

          <!-- Senha -->
          <div>
            <label for="password" class="form-label">{{ $t('auth.password') }}</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="input-primary"
              :placeholder="$t('auth.password')"
            />
            <p v-if="errors.password" class="form-error">{{ errors.password }}</p>
          </div>

          <!-- Confirmar Senha -->
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

        <!-- Termos e Condições -->
        <div class="flex items-center">
          <input
            id="terms"
            v-model="form.acceptTerms"
            type="checkbox"
            required
            class="checkbox checkbox-primary"
          />
          <label for="terms" class="ml-2 block text-sm text-base-content/80">
            {{ $t('auth.agreeToTerms') }}
            <a href="#" class="text-primary hover:text-primary/80">{{ $t('auth.termsAndConditions') }}</a>
          </label>
        </div>

        <!-- Botão Registrar -->
        <div>
          <button
            type="submit"
            class="btn btn-primary w-full"
            :disabled="loading"
          >
            <span v-if="loading" class="loading loading-spinner"></span>
            {{ $t('auth.register') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/core/store/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false
})

const errors = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateForm = () => {
  let isValid = true
  errors.value = {
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: ''
  }

  if (!form.value.firstName) {
    errors.value.firstName = 'Nome é obrigatório'
    isValid = false
  }

  if (!form.value.lastName) {
    errors.value.lastName = 'Sobrenome é obrigatório'
    isValid = false
  }

  if (!form.value.email) {
    errors.value.email = 'Email é obrigatório'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    errors.value.email = 'Email inválido'
    isValid = false
  }

  if (!form.value.password) {
    errors.value.password = 'Senha é obrigatória'
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

const handleRegister = async () => {
  if (!validateForm()) return

  loading.value = true
  try {
    await authStore.register({
      firstName: form.value.firstName,
      lastName: form.value.lastName,
      email: form.value.email,
      password: form.value.password
    })
    router.push({ name: 'Login' })
  } catch (error) {
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else {
      console.error('Erro ao registrar:', error)
    }
  } finally {
    loading.value = false
  }
}
</script>
