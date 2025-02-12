<template>
  <div class="space-y-6">
    <!-- Avatar -->
    <div class="flex items-start space-x-4">
      <div class="relative">
        <img
          v-if="settingsStore.hasAvatar"
          :src="settingsStore.profile.avatar"
          alt="Avatar"
          class="w-24 h-24 rounded-full object-cover"
        />
        <div
          v-else
          class="w-24 h-24 rounded-full bg-primary/10 flex items-center justify-center"
        >
          <UserCircleIcon class="w-16 h-16 text-primary" />
        </div>
        
        <div class="absolute -bottom-2 -right-2">
          <label
            class="btn btn-circle btn-sm btn-primary"
            :class="{ 'loading': uploading }"
          >
            <input
              type="file"
              class="hidden"
              accept="image/*"
              @change="handleAvatarChange"
            />
            <CameraIcon v-if="!uploading" class="w-4 h-4" />
          </label>
        </div>
      </div>

      <div class="flex-1">
        <h3 class="text-lg font-medium">{{ $t('settings.avatar') }}</h3>
        <p class="text-sm text-gray-500">
          {{ $t('settings.avatarHelp') }}
        </p>
        <div class="mt-2">
          <button
            v-if="settingsStore.hasAvatar"
            class="btn btn-ghost btn-sm text-error"
            @click="handleDeleteAvatar"
          >
            {{ $t('settings.removeAvatar') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Profile Form -->
    <Form
      @submit="handleProfileSubmit"
      :validation-schema="profileSchema"
      :initial-values="initialProfileValues"
      v-slot="{ errors, isSubmitting }"
    >
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Name -->
        <div>
          <label for="name" class="form-label">{{ $t('common.name') }}</label>
          <Field
            id="name"
            name="name"
            type="text"
            class="input input-bordered w-full"
            :class="{ 'input-error': errors.name }"
          />
          <ErrorMessage name="name" class="text-error text-sm mt-1" />
        </div>

        <!-- Email -->
        <div>
          <label for="email" class="form-label">{{ $t('common.email') }}</label>
          <Field
            id="email"
            name="email"
            type="email"
            class="input input-bordered w-full"
            :class="{ 'input-error': errors.email }"
          />
          <ErrorMessage name="email" class="text-error text-sm mt-1" />
        </div>

        <!-- Phone -->
        <div>
          <label for="phone" class="form-label">{{ $t('common.phone') }}</label>
          <Field
            id="phone"
            name="phone"
            type="tel"
            class="input input-bordered w-full"
            :class="{ 'input-error': errors.phone }"
          />
          <ErrorMessage name="phone" class="text-error text-sm mt-1" />
        </div>

        <!-- Language -->
        <div>
          <label for="language" class="form-label">{{ $t('common.language') }}</label>
          <Field
            id="language"
            name="language"
            as="select"
            class="select select-bordered w-full"
            :class="{ 'select-error': errors.language }"
          >
            <option value="pt-BR">Português (Brasil)</option>
            <option value="en">English</option>
            <option value="es">Español</option>
          </Field>
          <ErrorMessage name="language" class="text-error text-sm mt-1" />
        </div>

        <!-- Timezone -->
        <div>
          <label for="timezone" class="form-label">{{ $t('settings.timezone') }}</label>
          <Field
            id="timezone"
            name="timezone"
            as="select"
            class="select select-bordered w-full"
            :class="{ 'select-error': errors.timezone }"
          >
            <option value="America/Sao_Paulo">America/Sao_Paulo</option>
            <option value="UTC">UTC</option>
            <!-- Add more timezones as needed -->
          </Field>
          <ErrorMessage name="timezone" class="text-error text-sm mt-1" />
        </div>

        <!-- Bio -->
        <div class="md:col-span-2">
          <label for="bio" class="form-label">{{ $t('settings.bio') }}</label>
          <Field
            id="bio"
            name="bio"
            as="textarea"
            class="textarea textarea-bordered w-full h-24"
            :class="{ 'textarea-error': errors.bio }"
          />
          <ErrorMessage name="bio" class="text-error text-sm mt-1" />
        </div>
      </div>

      <div class="mt-6">
        <button
          type="submit"
          class="btn btn-primary"
          :class="{ 'loading': isSubmitting }"
          :disabled="isSubmitting"
        >
          {{ $t('common.save') }}
        </button>
      </div>
    </Form>

    <!-- Change Password -->
    <div class="pt-6 border-t">
      <h3 class="text-lg font-medium mb-4">{{ $t('settings.changePassword') }}</h3>
      
      <Form
        @submit="handlePasswordSubmit"
        :validation-schema="passwordSchema"
        v-slot="{ errors, isSubmitting }"
      >
        <div class="space-y-4">
          <!-- Current Password -->
          <div>
            <label for="currentPassword" class="form-label">
              {{ $t('settings.currentPassword') }}
            </label>
            <div class="relative">
              <Field
                id="currentPassword"
                name="currentPassword"
                :type="showCurrentPassword ? 'text' : 'password'"
                class="input input-bordered w-full pr-10"
                :class="{ 'input-error': errors.currentPassword }"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
                @click="showCurrentPassword = !showCurrentPassword"
              >
                <EyeIcon
                  v-if="!showCurrentPassword"
                  class="h-5 w-5 text-gray-400"
                />
                <EyeSlashIcon
                  v-else
                  class="h-5 w-5 text-gray-400"
                />
              </button>
            </div>
            <ErrorMessage name="currentPassword" class="text-error text-sm mt-1" />
          </div>

          <!-- New Password -->
          <div>
            <label for="newPassword" class="form-label">
              {{ $t('settings.newPassword') }}
            </label>
            <div class="relative">
              <Field
                id="newPassword"
                name="newPassword"
                :type="showNewPassword ? 'text' : 'password'"
                class="input input-bordered w-full pr-10"
                :class="{ 'input-error': errors.newPassword }"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
                @click="showNewPassword = !showNewPassword"
              >
                <EyeIcon
                  v-if="!showNewPassword"
                  class="h-5 w-5 text-gray-400"
                />
                <EyeSlashIcon
                  v-else
                  class="h-5 w-5 text-gray-400"
                />
              </button>
            </div>
            <ErrorMessage name="newPassword" class="text-error text-sm mt-1" />
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="form-label">
              {{ $t('settings.confirmPassword') }}
            </label>
            <div class="relative">
              <Field
                id="confirmPassword"
                name="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="input input-bordered w-full pr-10"
                :class="{ 'input-error': errors.confirmPassword }"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <EyeIcon
                  v-if="!showConfirmPassword"
                  class="h-5 w-5 text-gray-400"
                />
                <EyeSlashIcon
                  v-else
                  class="h-5 w-5 text-gray-400"
                />
              </button>
            </div>
            <ErrorMessage name="confirmPassword" class="text-error text-sm mt-1" />
          </div>

          <div>
            <button
              type="submit"
              class="btn btn-primary"
              :class="{ 'loading': isSubmitting }"
              :disabled="isSubmitting"
            >
              {{ $t('settings.updatePassword') }}
            </button>
          </div>
        </div>
      </Form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { object, string } from 'yup'
import { useI18n } from 'vue-i18n'
import { useSettingsStore } from '../store/settingsStore'
import { useNotification } from '@/shared/composables/useNotification'
import {
  UserCircleIcon,
  CameraIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/vue/24/outline'

const { t } = useI18n()
const settingsStore = useSettingsStore()
const notification = useNotification()

// Refs
const uploading = ref(false)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// Validation schemas
const profileSchema = object({
  name: string().required('settings.nameRequired'),
  email: string().required('settings.emailRequired').email('settings.emailInvalid'),
  phone: string(),
  language: string().required('settings.languageRequired'),
  timezone: string().required('settings.timezoneRequired'),
  bio: string().max(500, 'settings.bioMaxLength')
})

const passwordSchema = object({
  currentPassword: string().required('settings.currentPasswordRequired'),
  newPassword: string()
    .required('settings.newPasswordRequired')
    .min(8, 'settings.passwordMinLength')
    .matches(/[0-9]/, 'settings.passwordNumber')
    .matches(/[A-Z]/, 'settings.passwordUppercase')
    .matches(/[a-z]/, 'settings.passwordLowercase')
    .matches(/[^A-Za-z0-9]/, 'settings.passwordSpecial'),
  confirmPassword: string()
    .required('settings.confirmPasswordRequired')
    .oneOf([ref('newPassword')], 'settings.passwordMatch')
})

// Initial values
const initialProfileValues = computed(() => ({
  name: settingsStore.profile?.name || '',
  email: settingsStore.profile?.email || '',
  phone: settingsStore.profile?.phone || '',
  language: settingsStore.profile?.language || 'pt-BR',
  timezone: settingsStore.profile?.timezone || 'America/Sao_Paulo',
  bio: settingsStore.profile?.bio || ''
}))

// Methods
const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('avatar', file)
    await settingsStore.updateAvatar(formData)
    notification.showSuccess(t('settings.avatarUpdated'))
  } catch (error) {
    notification.showError(error.message)
  } finally {
    uploading.value = false
  }
}

const handleDeleteAvatar = async () => {
  try {
    await settingsStore.deleteAvatar()
    notification.showSuccess(t('settings.avatarRemoved'))
  } catch (error) {
    notification.showError(error.message)
  }
}

const handleProfileSubmit = async (values) => {
  try {
    await settingsStore.updateUserProfile(values)
    notification.showSuccess(t('settings.profileUpdated'))
  } catch (error) {
    notification.showError(error.message)
  }
}

const handlePasswordSubmit = async (values) => {
  try {
    await settingsStore.updatePassword({
      currentPassword: values.currentPassword,
      newPassword: values.newPassword
    })
    notification.showSuccess(t('settings.passwordUpdated'))
  } catch (error) {
    notification.showError(error.message)
  }
}
</script>
