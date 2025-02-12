<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="page-title">{{ $t('settings.profile') }}</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Informações Pessoais -->
      <div class="lg:col-span-2">
        <div class="card-container">
          <h2 class="section-title">{{ $t('users.personalInfo') }}</h2>
          
          <form @submit.prevent="updateProfile" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Nome -->
              <div>
                <label class="form-label" for="firstName">{{ $t('users.firstName') }}</label>
                <input
                  id="firstName"
                  v-model="profile.firstName"
                  type="text"
                  class="input-primary"
                  :placeholder="$t('users.firstName')"
                />
              </div>

              <!-- Sobrenome -->
              <div>
                <label class="form-label" for="lastName">{{ $t('users.lastName') }}</label>
                <input
                  id="lastName"
                  v-model="profile.lastName"
                  type="text"
                  class="input-primary"
                  :placeholder="$t('users.lastName')"
                />
              </div>
            </div>

            <!-- Email -->
            <div>
              <label class="form-label" for="email">{{ $t('auth.email') }}</label>
              <input
                id="email"
                v-model="profile.email"
                type="email"
                class="input-primary"
                :placeholder="$t('auth.email')"
                disabled
              />
              <p class="text-sm text-gray-500 mt-1">{{ $t('users.emailChangeNotice') }}</p>
            </div>

            <!-- Idioma -->
            <div>
              <label class="form-label" for="language">{{ $t('common.language') }}</label>
              <select
                id="language"
                v-model="profile.language"
                class="input-primary"
              >
                <option value="pt-BR">Português (Brasil)</option>
                <option value="en-US">English (US)</option>
              </select>
            </div>

            <!-- Botão Salvar -->
            <div class="flex justify-end">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="loading loading-spinner"></span>
                {{ $t('common.save') }}
              </button>
            </div>
          </form>
        </div>

        <!-- Alterar Senha -->
        <div class="card-container mt-6">
          <h2 class="section-title">{{ $t('settings.security') }}</h2>
          
          <form @submit.prevent="updatePassword" class="space-y-6">
            <!-- Senha Atual -->
            <div>
              <label class="form-label" for="currentPassword">{{ $t('auth.currentPassword') }}</label>
              <input
                id="currentPassword"
                v-model="passwordForm.currentPassword"
                type="password"
                class="input-primary"
                :placeholder="$t('auth.currentPassword')"
              />
            </div>

            <!-- Nova Senha -->
            <div>
              <label class="form-label" for="newPassword">{{ $t('auth.newPassword') }}</label>
              <input
                id="newPassword"
                v-model="passwordForm.newPassword"
                type="password"
                class="input-primary"
                :placeholder="$t('auth.newPassword')"
              />
            </div>

            <!-- Confirmar Nova Senha -->
            <div>
              <label class="form-label" for="confirmPassword">{{ $t('auth.confirmPassword') }}</label>
              <input
                id="confirmPassword"
                v-model="passwordForm.confirmPassword"
                type="password"
                class="input-primary"
                :placeholder="$t('auth.confirmPassword')"
              />
            </div>

            <!-- Botão Alterar Senha -->
            <div class="flex justify-end">
              <button type="submit" class="btn btn-primary" :disabled="passwordLoading">
                <span v-if="passwordLoading" class="loading loading-spinner"></span>
                {{ $t('auth.changePassword') }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Avatar e Informações Adicionais -->
      <div class="lg:col-span-1">
        <div class="card-container">
          <div class="flex flex-col items-center">
            <!-- Avatar -->
            <div class="w-32 h-32 rounded-full bg-gray-200 flex items-center justify-center mb-4">
              <svg v-if="!profile.avatar" xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <img
                v-else
                :src="profile.avatar"
                :alt="profile.firstName"
                class="w-full h-full object-cover rounded-full"
              />
            </div>

            <!-- Upload Avatar -->
            <button class="btn btn-outline btn-sm mb-4" @click="triggerFileInput">
              {{ $t('users.changeAvatar') }}
            </button>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleAvatarUpload"
            />

            <!-- Informações do Usuário -->
            <div class="w-full space-y-4 mt-4">
              <div>
                <label class="text-sm text-gray-500">{{ $t('users.role') }}</label>
                <p class="font-medium">{{ profile.role }}</p>
              </div>
              <div>
                <label class="text-sm text-gray-500">{{ $t('users.lastLogin') }}</label>
                <p class="font-medium">{{ formatDate(profile.lastLogin) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/core/store/auth'
import { format } from 'date-fns'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const authStore = useAuthStore()
const fileInput = ref(null)

const loading = ref(false)
const passwordLoading = ref(false)

const profile = ref({
  firstName: '',
  lastName: '',
  email: '',
  role: '',
  avatar: null,
  language: 'pt-BR',
  lastLogin: new Date()
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const formatDate = (date) => {
  return format(new Date(date), 'dd/MM/yyyy HH:mm')
}

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    // Aqui você pode implementar o upload do avatar
    console.log('Upload avatar:', file)
  } catch (error) {
    console.error('Erro ao fazer upload do avatar:', error)
  }
}

const updateProfile = async () => {
  loading.value = true
  try {
    // Aqui você pode implementar a atualização do perfil
    console.log('Update profile:', profile.value)
  } catch (error) {
    console.error('Erro ao atualizar perfil:', error)
  } finally {
    loading.value = false
  }
}

const updatePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    // Adicionar mensagem de erro
    return
  }

  passwordLoading.value = true
  try {
    // Aqui você pode implementar a alteração de senha
    console.log('Update password:', passwordForm.value)
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error) {
    console.error('Erro ao alterar senha:', error)
  } finally {
    passwordLoading.value = false
  }
}

onMounted(async () => {
  try {
    // Aqui você pode carregar os dados do perfil
    const user = authStore.user
    profile.value = {
      firstName: user?.firstName || '',
      lastName: user?.lastName || '',
      email: user?.email || '',
      role: user?.role || 'Usuário',
      avatar: user?.avatar,
      language: localStorage.getItem('language') || 'pt-BR',
      lastLogin: user?.lastLogin || new Date()
    }
  } catch (error) {
    console.error('Erro ao carregar perfil:', error)
  }
})
</script>
