<template>
  <div class="modal modal-open">
    <div class="modal-box max-w-4xl">
      <button
        class="btn btn-sm btn-circle absolute right-2 top-2"
        @click="$emit('close')"
      >
        ✕
      </button>
      
      <h3 class="text-lg font-bold mb-4">
        {{ isEdit ? $t('roles.editRole') : $t('roles.createRole') }}
      </h3>

      <Form @submit="handleSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }">
        <div class="space-y-6">
          <!-- Basic Information -->
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
                :placeholder="$t('roles.namePlaceholder')"
              />
              <ErrorMessage name="name" class="text-error text-sm mt-1" />
            </div>

            <!-- Description -->
            <div>
              <label for="description" class="form-label">{{ $t('common.description') }}</label>
              <Field
                id="description"
                name="description"
                type="text"
                class="input input-bordered w-full"
                :class="{ 'input-error': errors.description }"
                :placeholder="$t('roles.descriptionPlaceholder')"
              />
              <ErrorMessage name="description" class="text-error text-sm mt-1" />
            </div>
          </div>

          <!-- Permissions -->
          <div>
            <h4 class="font-medium mb-4">{{ $t('roles.permissions') }}</h4>

            <div class="space-y-4">
              <div
                v-for="(permissions, category) in permissionsByCategory"
                :key="category"
                class="bg-base-100 p-4 rounded-lg border"
              >
                <div class="flex items-center justify-between mb-2">
                  <h5 class="font-medium">{{ category }}</h5>
                  <label class="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      class="checkbox checkbox-sm"
                      :checked="isAllCategorySelected(permissions)"
                      @change="toggleCategory(permissions)"
                    />
                    <span class="text-sm">{{ $t('common.selectAll') }}</span>
                  </label>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                  <label
                    v-for="permission in permissions"
                    :key="permission.id"
                    class="flex items-center space-x-2 p-2 rounded hover:bg-base-200"
                  >
                    <Field
                      type="checkbox"
                      name="permissions"
                      :value="permission.id"
                      class="checkbox checkbox-primary checkbox-sm"
                    />
                    <div>
                      <span class="text-sm">{{ permission.name }}</span>
                      <p class="text-xs text-gray-500">{{ permission.description }}</p>
                    </div>
                  </label>
                </div>
              </div>
            </div>
            <ErrorMessage name="permissions" class="text-error text-sm mt-1" />
          </div>

          <!-- Advanced Settings -->
          <div class="space-y-4">
            <h4 class="font-medium">{{ $t('roles.advancedSettings') }}</h4>

            <!-- Priority -->
            <div>
              <label for="priority" class="form-label">{{ $t('roles.priority') }}</label>
              <Field
                id="priority"
                name="priority"
                type="number"
                class="input input-bordered w-full"
                :class="{ 'input-error': errors.priority }"
              />
              <p class="text-sm text-gray-500 mt-1">
                {{ $t('roles.priorityHelp') }}
              </p>
              <ErrorMessage name="priority" class="text-error text-sm mt-1" />
            </div>

            <!-- Scope -->
            <div>
              <label for="scope" class="form-label">{{ $t('roles.scope') }}</label>
              <Field
                id="scope"
                name="scope"
                as="select"
                class="select select-bordered w-full"
                :class="{ 'select-error': errors.scope }"
              >
                <option value="global">{{ $t('roles.scopeGlobal') }}</option>
                <option value="tenant">{{ $t('roles.scopeTenant') }}</option>
              </Field>
              <p class="text-sm text-gray-500 mt-1">
                {{ $t('roles.scopeHelp') }}
              </p>
              <ErrorMessage name="scope" class="text-error text-sm mt-1" />
            </div>

            <!-- Options -->
            <div class="space-y-2">
              <label class="flex items-center space-x-2">
                <Field
                  type="checkbox"
                  name="isDefault"
                  class="checkbox checkbox-primary"
                />
                <span>{{ $t('roles.isDefault') }}</span>
              </label>
              <p class="text-sm text-gray-500 ml-6">
                {{ $t('roles.isDefaultHelp') }}
              </p>

              <label class="flex items-center space-x-2">
                <Field
                  type="checkbox"
                  name="isSystem"
                  class="checkbox checkbox-primary"
                  :disabled="true"
                />
                <span>{{ $t('roles.isSystem') }}</span>
              </label>
              <p class="text-sm text-gray-500 ml-6">
                {{ $t('roles.isSystemHelp') }}
              </p>
            </div>
          </div>
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
import { computed } from 'vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { object, string, array, number, boolean } from 'yup'
import { storeToRefs } from 'pinia'
import { useRoleStore } from '../store/roleStore'

const props = defineProps({
  role: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])

const roleStore = useRoleStore()
const { availablePermissions } = storeToRefs(roleStore)

const isEdit = computed(() => !!props.role)

// Computed
const permissionsByCategory = computed(() => {
  return roleStore.getPermissionsByCategory
})

// Validation schema
const schema = object({
  name: string()
    .required('roles.nameRequired')
    .min(3, 'roles.nameMinLength')
    .matches(/^[a-zA-Z0-9_-]+$/, 'roles.nameFormat'),
  description: string().required('roles.descriptionRequired'),
  permissions: array().min(1, 'roles.permissionsRequired'),
  priority: number()
    .required('roles.priorityRequired')
    .min(0, 'roles.priorityMin')
    .max(100, 'roles.priorityMax'),
  scope: string().required('roles.scopeRequired'),
  isDefault: boolean(),
  isSystem: boolean()
})

// Initial values
const initialValues = computed(() => {
  if (props.role) {
    return {
      name: props.role.name,
      description: props.role.description,
      permissions: props.role.permissions.map(p => p.id),
      priority: props.role.priority,
      scope: props.role.scope,
      isDefault: props.role.isDefault,
      isSystem: props.role.isSystem
    }
  }
  return {
    name: '',
    description: '',
    permissions: [],
    priority: 0,
    scope: 'tenant',
    isDefault: false,
    isSystem: false
  }
})

// Methods
const isAllCategorySelected = (permissions) => {
  return permissions.every(permission =>
    initialValues.value.permissions.includes(permission.id)
  )
}

const toggleCategory = (permissions) => {
  const allSelected = isAllCategorySelected(permissions)
  const permissionIds = permissions.map(p => p.id)
  
  if (allSelected) {
    // Remove all permissions from this category
    initialValues.value.permissions = initialValues.value.permissions.filter(
      id => !permissionIds.includes(id)
    )
  } else {
    // Add all permissions from this category
    initialValues.value.permissions = [
      ...new Set([...initialValues.value.permissions, ...permissionIds])
    ]
  }
}

const handleSubmit = (values) => {
  emit('save', values)
}
</script>
