<template>
  <Form @submit="handleLogin" :validation-schema="schema" v-slot="{ errors, isSubmitting }">
    <!-- Tenant Selection for Master Users -->
    <div v-if="isMasterUser" class="space-y-6">
      <div>
        <label for="tenant" class="form-label">{{ $t('auth.selectTenant') }}</label>
        <Field
          name="tenant"
          as="select"
          class="input-primary"
          :class="{ 'input-error': errors.tenant }"
        >
          <option value="">{{ $t('auth.selectTenant') }}</option>
          <option v-for="tenant in tenants" :key="tenant.id" :value="tenant.id">
            {{ tenant.name }}
          </option>
        </Field>
        <ErrorMessage name="tenant" class="form-error" />
      </div>
    </div>

    <!-- Login Form -->
    <div class="space-y-6">
      <div>
        <label for="email" class="form-label">{{ $t('auth.email') }}</label>
        <Field
          id="email"
          name="email"
          type="email"
          autocomplete="email"
          required
          class="input-primary"
          :class="{ 'input-error': errors.email }"
        />
        <ErrorMessage name="email" class="form-error" />
      </div>

      <div>
        <label for="password" class="form-label">
          {{ $t('auth.password') }}
        </label>
        <div class="relative">
          <Field
            id="password"
            :type="showPassword ? 'text' : 'password'"
            name="password"
            autocomplete="current-password"
            required
            class="input-primary pr-10"
            :class="{ 'input-error': errors.password }"
          />
          <button
            type="button"
            class="absolute inset-y-0 right-0 pr-3 flex items-center"
            @click="showPassword = !showPassword"
          >
            <EyeIcon v-if="!showPassword" class="h-5 w-5 text-gray-400" />
            <EyeSlashIcon v-else class="h-5 w-5 text-gray-400" />
          </button>
        </div>
        <ErrorMessage name="password" class="form-error" />
      </div>

      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <Field
            id="remember"
            name="remember"
            type="checkbox"
            class="checkbox checkbox-primary"
          />
          <label for="remember" class="ml-2 block text-sm text-gray-900">
            {{ $t('auth.rememberMe') }}
          </label>
        </div>

        <div class="text-sm">
          <router-link
            to="/auth/forgot-password"
            class="font-medium text-primary hover:text-primary-focus"
          >
            {{ $t('auth.forgotPassword') }}
          </router-link>
        </div>
      </div>

      <div>
        <button
          type="submit"
          class="btn-primary w-full"
          :class="{ 'loading': isSubmitting }"
          :disabled="isSubmitting"
        >
          {{ $t('auth.signIn') }}
        </button>
      </div>

      <!-- 2FA Modal -->
      <TwoFactorModal
        v-if="show2FADialog"
        :email="form.email"
        @verify="handleVerify2FA"
        @close="show2FADialog = false"
      />
    </div>
  </Form>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/core/store/auth'
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline'
import { authApi } from '@/core/api/auth'
import { useNotification } from '@/shared/composables/useNotification'
import TwoFactorModal from '../components/TwoFactorModal.vue'

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()
const notification = useNotification()

const showPassword = ref(false)
const show2FADialog = ref(false)
const form = ref({
  email: '',
  password: '',
  tenant: ''
})
const tenants = ref([])

// Form validation schema
const schema = yup.object().shape({
  email: yup.string().required(t('validation.required')).email(t('validation.email')),
  password: yup.string().required(t('validation.required')),
  tenant: yup.string().when('isMasterUser', {
    is: true,
    then: () => yup.string().required(t('validation.required')),
    otherwise: () => yup.string()
  })
})

const isMasterUser = computed(() => {
  return authStore.hasRole('master_user')
})

// Fetch tenants if master user
const fetchTenants = async () => {
  if (isMasterUser.value) {
    try {
      const response = await authApi.getTenants()
      tenants.value = response.data
    } catch (error) {
      notification.showError(error.message)
    }
  }
}

// Handle login
const handleLogin = async (values) => {
  try {
    const response = await authApi.login(values)
    if (response.requires2FA) {
      show2FADialog.value = true
    } else {
      await authStore.setUser(response.user)
      await authStore.setToken(response.token)
      notification.showSuccess(t('auth.loginSuccess'))
      router.push({ name: 'dashboard' })
    }
  } catch (error) {
    notification.showError(error.message)
  }
}

// Handle 2FA verification
const handleVerify2FA = async (code) => {
  try {
    const response = await authApi.verify2FA(code)
    await authStore.setUser(response.user)
    await authStore.setToken(response.token)
    notification.showSuccess(t('auth.loginSuccess'))
    router.push({ name: 'dashboard' })
  } catch (error) {
    notification.showError(error.message)
  }
}
</script>
