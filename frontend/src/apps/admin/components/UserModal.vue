<template>
  <div class="modal modal-open">
    <div class="modal-box max-w-2xl">
      <button
        class="btn btn-sm btn-circle absolute right-2 top-2"
        @click="$emit('close')"
      >
        ✕
      </button>
      
      <h3 class="text-lg font-bold mb-4">
        {{ isEdit ? $t('users.editUser') : $t('users.createUser') }}
      </h3>

      <Form @submit="handleSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Name -->
          <div>
            <label for="name" class="form-label">{{ $t('users.name') }}</label>
            <Field
              id="name"
              name="name"
              type="text"
              class="input-primary"
              :class="{ 'input-error': errors.name }"
              :placeholder="$t('users.namePlaceholder')"
            />
            <ErrorMessage name="name" class="form-error" />
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="form-label">{{ $t('users.email') }}</label>
            <Field
              id="email"
              name="email"
              type="email"
              class="input-primary"
              :class="{ 'input-error': errors.email }"
              :placeholder="$t('users.emailPlaceholder')"
            />
            <ErrorMessage name="email" class="form-error" />
          </div>

          <!-- Password (only for new users) -->
          <div v-if="!isEdit">
            <label for="password" class="form-label">{{ $t('users.password') }}</label>
            <div class="relative">
              <Field
                id="password"
                :type="showPassword ? 'text' : 'password'"
                name="password"
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

          <!-- Status -->
          <div>
            <label for="status" class="form-label">{{ $t('users.status') }}</label>
            <Field
              id="status"
              name="status"
              as="select"
              class="input-primary"
              :class="{ 'input-error': errors.status }"
            >
              <option value="active">{{ $t('users.active') }}</option>
              <option value="inactive">{{ $t('users.inactive') }}</option>
            </Field>
            <ErrorMessage name="status" class="form-error" />
          </div>
        </div>

        <!-- Roles -->
        <div class="mt-4">
          <label class="form-label">{{ $t('users.roles') }}</label>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
            <label
              v-for="role in roles"
              :key="role.id"
              class="flex items-center space-x-2 p-2 rounded border hover:bg-gray-50"
            >
              <Field
                type="checkbox"
                name="roles"
                :value="role.id"
                class="checkbox checkbox-primary"
              />
              <span class="text-sm">{{ role.name }}</span>
            </label>
          </div>
          <ErrorMessage name="roles" class="form-error" />
        </div>

        <!-- Force 2FA -->
        <div class="mt-4">
          <label class="flex items-center space-x-2">
            <Field
              type="checkbox"
              name="force2fa"
              class="checkbox checkbox-primary"
            />
            <span>{{ $t('users.force2fa') }}</span>
          </label>
          <p class="text-sm text-gray-500 mt-1">
            {{ $t('users.force2faHelp') }}
          </p>
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
            type="submit"
            class="btn btn-primary"
            :class="{ 'loading': isSubmitting }"
            :disabled="isSubmitting"
          >
            {{ $t('common.save') }}
          </button>
        </div>
      </Form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { object, string, array } from 'yup'
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  user: {
    type: Object,
    default: null
  },
  roles: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['close', 'save'])

const showPassword = ref(false)

const isEdit = computed(() => !!props.user)

// Validation schema
const schema = object({
  name: string().required('users.nameRequired'),
  email: string().required('users.emailRequired').email('users.emailInvalid'),
  password: string().when('isEdit', {
    is: false,
    then: () => string().required('users.passwordRequired')
      .min(8, 'users.passwordMinLength')
      .matches(/[0-9]/, 'users.passwordNumber')
      .matches(/[A-Z]/, 'users.passwordUppercase')
      .matches(/[a-z]/, 'users.passwordLowercase')
      .matches(/[^A-Za-z0-9]/, 'users.passwordSpecial'),
    otherwise: () => string()
  }),
  status: string().required('users.statusRequired'),
  roles: array().min(1, 'users.rolesRequired'),
  force2fa: string()
})

// Initial form values
const initialValues = computed(() => {
  if (props.user) {
    return {
      name: props.user.name,
      email: props.user.email,
      status: props.user.status,
      roles: props.user.roles.map(role => role.id),
      force2fa: props.user.force2fa
    }
  }
  return {
    name: '',
    email: '',
    password: '',
    status: 'active',
    roles: [],
    force2fa: false
  }
})

const handleSubmit = (values) => {
  emit('save', values)
}
</script>
