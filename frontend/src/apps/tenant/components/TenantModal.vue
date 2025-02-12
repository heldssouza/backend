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
        {{ isEdit ? $t('tenants.editTenant') : $t('tenants.createTenant') }}
      </h3>

      <Form @submit="handleSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }">
        <div class="space-y-4">
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
              />
              <ErrorMessage name="name" class="text-error text-sm mt-1" />
            </div>

            <!-- Domain -->
            <div>
              <label for="domain" class="form-label">{{ $t('tenants.domain') }}</label>
              <Field
                id="domain"
                name="domain"
                type="text"
                class="input input-bordered w-full"
                :class="{ 'input-error': errors.domain }"
              />
              <ErrorMessage name="domain" class="text-error text-sm mt-1" />
            </div>
          </div>

          <!-- Description -->
          <div>
            <label for="description" class="form-label">{{ $t('common.description') }}</label>
            <Field
              id="description"
              name="description"
              as="textarea"
              class="textarea textarea-bordered w-full h-24"
              :class="{ 'textarea-error': errors.description }"
            />
            <ErrorMessage name="description" class="text-error text-sm mt-1" />
          </div>

          <!-- Database Configuration -->
          <div class="space-y-4">
            <h4 class="font-medium">{{ $t('tenants.databaseConfig') }}</h4>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Database Name -->
              <div>
                <label for="dbName" class="form-label">{{ $t('tenants.dbName') }}</label>
                <Field
                  id="dbName"
                  name="database.name"
                  type="text"
                  class="input input-bordered w-full"
                  :class="{ 'input-error': errors['database.name'] }"
                />
                <ErrorMessage name="database.name" class="text-error text-sm mt-1" />
              </div>

              <!-- Database Type -->
              <div>
                <label for="dbType" class="form-label">{{ $t('tenants.dbType') }}</label>
                <Field
                  id="dbType"
                  name="database.type"
                  as="select"
                  class="select select-bordered w-full"
                  :class="{ 'select-error': errors['database.type'] }"
                >
                  <option value="postgresql">PostgreSQL</option>
                  <option value="mysql">MySQL</option>
                  <option value="mongodb">MongoDB</option>
                </Field>
                <ErrorMessage name="database.type" class="text-error text-sm mt-1" />
              </div>
            </div>
          </div>

          <!-- Settings -->
          <div class="space-y-4">
            <h4 class="font-medium">{{ $t('tenants.settings') }}</h4>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Language -->
              <div>
                <label for="language" class="form-label">{{ $t('common.language') }}</label>
                <Field
                  id="language"
                  name="settings.language"
                  as="select"
                  class="select select-bordered w-full"
                  :class="{ 'select-error': errors['settings.language'] }"
                >
                  <option value="pt-BR">Português (Brasil)</option>
                  <option value="en">English</option>
                  <option value="es">Español</option>
                </Field>
                <ErrorMessage name="settings.language" class="text-error text-sm mt-1" />
              </div>

              <!-- Timezone -->
              <div>
                <label for="timezone" class="form-label">{{ $t('tenants.timezone') }}</label>
                <Field
                  id="timezone"
                  name="settings.timezone"
                  as="select"
                  class="select select-bordered w-full"
                  :class="{ 'select-error': errors['settings.timezone'] }"
                >
                  <option value="America/Sao_Paulo">America/Sao_Paulo</option>
                  <option value="UTC">UTC</option>
                  <!-- Add more timezones as needed -->
                </Field>
                <ErrorMessage name="settings.timezone" class="text-error text-sm mt-1" />
              </div>
            </div>

            <!-- Features -->
            <div class="space-y-2">
              <label class="form-label">{{ $t('tenants.features') }}</label>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <label class="flex items-center space-x-2">
                  <Field
                    type="checkbox"
                    name="settings.features"
                    value="2fa"
                    class="checkbox checkbox-primary"
                  />
                  <span>{{ $t('tenants.2fa') }}</span>
                </label>
                <label class="flex items-center space-x-2">
                  <Field
                    type="checkbox"
                    name="settings.features"
                    value="audit"
                    class="checkbox checkbox-primary"
                  />
                  <span>{{ $t('tenants.audit') }}</span>
                </label>
                <label class="flex items-center space-x-2">
                  <Field
                    type="checkbox"
                    name="settings.features"
                    value="api"
                    class="checkbox checkbox-primary"
                  />
                  <span>{{ $t('tenants.api') }}</span>
                </label>
                <label class="flex items-center space-x-2">
                  <Field
                    type="checkbox"
                    name="settings.features"
                    value="backup"
                    class="checkbox checkbox-primary"
                  />
                  <span>{{ $t('tenants.backup') }}</span>
                </label>
              </div>
              <ErrorMessage name="settings.features" class="text-error text-sm mt-1" />
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
import { object, string, array } from 'yup'

const props = defineProps({
  tenant: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])

const isEdit = computed(() => !!props.tenant)

// Validation schema
const schema = object({
  name: string().required('tenants.nameRequired'),
  domain: string()
    .required('tenants.domainRequired')
    .matches(/^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/, 'tenants.domainInvalid'),
  description: string(),
  database: object({
    name: string().required('tenants.dbNameRequired'),
    type: string().required('tenants.dbTypeRequired')
  }),
  settings: object({
    language: string().required('tenants.languageRequired'),
    timezone: string().required('tenants.timezoneRequired'),
    features: array().of(string())
  })
})

// Initial values
const initialValues = computed(() => {
  if (props.tenant) {
    return {
      name: props.tenant.name,
      domain: props.tenant.domain,
      description: props.tenant.description,
      database: props.tenant.database,
      settings: props.tenant.settings
    }
  }
  return {
    name: '',
    domain: '',
    description: '',
    database: {
      name: '',
      type: 'postgresql'
    },
    settings: {
      language: 'pt-BR',
      timezone: 'America/Sao_Paulo',
      features: []
    }
  }
})

const handleSubmit = (values) => {
  emit('save', values)
}
</script>
