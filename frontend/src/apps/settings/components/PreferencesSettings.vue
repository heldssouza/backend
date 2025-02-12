<template>
  <div class="space-y-6">
    <!-- Theme Settings -->
    <div>
      <h3 class="text-lg font-medium mb-4">{{ $t('settings.appearance') }}</h3>
      
      <div class="space-y-4">
        <!-- Theme Mode -->
        <div>
          <label class="form-label">{{ $t('settings.themeMode') }}</label>
          <div class="grid grid-cols-3 gap-4">
            <label
              v-for="mode in themeModes"
              :key="mode.value"
              class="relative"
            >
              <input
                type="radio"
                name="themeMode"
                :value="mode.value"
                :checked="preferences.themeMode === mode.value"
                @change="updatePreference('themeMode', mode.value)"
                class="peer sr-only"
              />
              <div class="p-4 rounded-lg border cursor-pointer hover:bg-base-200 peer-checked:border-primary peer-checked:bg-primary/10">
                <component
                  :is="mode.icon"
                  class="w-6 h-6 mx-auto mb-2"
                />
                <div class="text-center text-sm">{{ mode.label }}</div>
              </div>
            </label>
          </div>
        </div>

        <!-- Color Scheme -->
        <div>
          <label class="form-label">{{ $t('settings.colorScheme') }}</label>
          <div class="grid grid-cols-4 gap-4">
            <label
              v-for="color in colorSchemes"
              :key="color.value"
              class="relative"
            >
              <input
                type="radio"
                name="colorScheme"
                :value="color.value"
                :checked="preferences.colorScheme === color.value"
                @change="updatePreference('colorScheme', color.value)"
                class="peer sr-only"
              />
              <div
                class="p-4 rounded-lg border cursor-pointer hover:bg-base-200 peer-checked:border-primary peer-checked:bg-primary/10"
                :style="{ backgroundColor: color.preview }"
              >
                <div class="text-center text-sm">{{ color.label }}</div>
              </div>
            </label>
          </div>
        </div>

        <!-- Font Size -->
        <div>
          <label class="form-label">{{ $t('settings.fontSize') }}</label>
          <div class="flex items-center space-x-4">
            <button
              class="btn btn-circle btn-sm"
              @click="decreaseFontSize"
              :disabled="preferences.fontSize <= 12"
            >
              <MinusIcon class="w-4 h-4" />
            </button>
            <span class="text-lg font-medium">{{ preferences.fontSize }}px</span>
            <button
              class="btn btn-circle btn-sm"
              @click="increaseFontSize"
              :disabled="preferences.fontSize >= 20"
            >
              <PlusIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Layout Settings -->
    <div class="pt-6 border-t">
      <h3 class="text-lg font-medium mb-4">{{ $t('settings.layout') }}</h3>
      
      <div class="space-y-4">
        <!-- Sidebar Position -->
        <div>
          <label class="form-label">{{ $t('settings.sidebarPosition') }}</label>
          <div class="grid grid-cols-2 gap-4">
            <label
              v-for="position in sidebarPositions"
              :key="position.value"
              class="relative"
            >
              <input
                type="radio"
                name="sidebarPosition"
                :value="position.value"
                :checked="preferences.sidebarPosition === position.value"
                @change="updatePreference('sidebarPosition', position.value)"
                class="peer sr-only"
              />
              <div class="p-4 rounded-lg border cursor-pointer hover:bg-base-200 peer-checked:border-primary peer-checked:bg-primary/10">
                <component
                  :is="position.icon"
                  class="w-6 h-6 mx-auto mb-2"
                />
                <div class="text-center text-sm">{{ position.label }}</div>
              </div>
            </label>
          </div>
        </div>

        <!-- Content Width -->
        <div>
          <label class="form-label">{{ $t('settings.contentWidth') }}</label>
          <div class="grid grid-cols-2 gap-4">
            <label
              v-for="width in contentWidths"
              :key="width.value"
              class="relative"
            >
              <input
                type="radio"
                name="contentWidth"
                :value="width.value"
                :checked="preferences.contentWidth === width.value"
                @change="updatePreference('contentWidth', width.value)"
                class="peer sr-only"
              />
              <div class="p-4 rounded-lg border cursor-pointer hover:bg-base-200 peer-checked:border-primary peer-checked:bg-primary/10">
                <component
                  :is="width.icon"
                  class="w-6 h-6 mx-auto mb-2"
                />
                <div class="text-center text-sm">{{ width.label }}</div>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Behavior Settings -->
    <div class="pt-6 border-t">
      <h3 class="text-lg font-medium mb-4">{{ $t('settings.behavior') }}</h3>
      
      <div class="space-y-4">
        <!-- Animations -->
        <label class="flex items-center justify-between">
          <div>
            <span class="font-medium">{{ $t('settings.animations') }}</span>
            <p class="text-sm text-gray-500">
              {{ $t('settings.animationsHelp') }}
            </p>
          </div>
          <input
            type="checkbox"
            :checked="preferences.animations"
            @change="updatePreference('animations', $event.target.checked)"
            class="toggle toggle-primary"
          />
        </label>

        <!-- Sound Effects -->
        <label class="flex items-center justify-between">
          <div>
            <span class="font-medium">{{ $t('settings.soundEffects') }}</span>
            <p class="text-sm text-gray-500">
              {{ $t('settings.soundEffectsHelp') }}
            </p>
          </div>
          <input
            type="checkbox"
            :checked="preferences.soundEffects"
            @change="updatePreference('soundEffects', $event.target.checked)"
            class="toggle toggle-primary"
          />
        </label>

        <!-- Auto Save -->
        <label class="flex items-center justify-between">
          <div>
            <span class="font-medium">{{ $t('settings.autoSave') }}</span>
            <p class="text-sm text-gray-500">
              {{ $t('settings.autoSaveHelp') }}
            </p>
          </div>
          <input
            type="checkbox"
            :checked="preferences.autoSave"
            @change="updatePreference('autoSave', $event.target.checked)"
            class="toggle toggle-primary"
          />
        </label>
      </div>
    </div>

    <!-- Reset Button -->
    <div class="pt-6 border-t">
      <button
        class="btn btn-outline btn-error"
        @click="resetPreferences"
      >
        {{ $t('settings.resetPreferences') }}
      </button>
      <p class="text-sm text-gray-500 mt-2">
        {{ $t('settings.resetPreferencesHelp') }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSettingsStore } from '../store/settingsStore'
import { useNotification } from '@/shared/composables/useNotification'
import {
  SunIcon,
  MoonIcon,
  ComputerDesktopIcon,
  MinusIcon,
  PlusIcon,
  ArrowsPointingInIcon,
  ArrowsPointingOutIcon,
  Bars3Icon,
  Bars3BottomLeftIcon
} from '@heroicons/vue/24/outline'

const { t } = useI18n()
const settingsStore = useSettingsStore()
const notification = useNotification()

// Constants
const themeModes = [
  { value: 'light', label: t('settings.light'), icon: SunIcon },
  { value: 'dark', label: t('settings.dark'), icon: MoonIcon },
  { value: 'system', label: t('settings.system'), icon: ComputerDesktopIcon }
]

const colorSchemes = [
  { value: 'blue', label: t('settings.blue'), preview: '#3B82F6' },
  { value: 'green', label: t('settings.green'), preview: '#10B981' },
  { value: 'purple', label: t('settings.purple'), preview: '#8B5CF6' },
  { value: 'red', label: t('settings.red'), preview: '#EF4444' }
]

const sidebarPositions = [
  { value: 'left', label: t('settings.left'), icon: Bars3BottomLeftIcon },
  { value: 'right', label: t('settings.right'), icon: Bars3Icon }
]

const contentWidths = [
  { value: 'full', label: t('settings.full'), icon: ArrowsPointingOutIcon },
  { value: 'contained', label: t('settings.contained'), icon: ArrowsPointingInIcon }
]

// Default preferences
const defaultPreferences = {
  themeMode: 'system',
  colorScheme: 'blue',
  fontSize: 16,
  sidebarPosition: 'left',
  contentWidth: 'contained',
  animations: true,
  soundEffects: true,
  autoSave: true
}

// Computed
const preferences = computed(() => ({
  ...defaultPreferences,
  ...settingsStore.preferences
}))

// Methods
const updatePreference = async (key, value) => {
  try {
    await settingsStore.updatePreferences({
      ...preferences.value,
      [key]: value
    })
    notification.showSuccess(t('settings.preferencesUpdated'))
  } catch (error) {
    notification.showError(error.message)
  }
}

const increaseFontSize = () => {
  if (preferences.value.fontSize < 20) {
    updatePreference('fontSize', preferences.value.fontSize + 1)
  }
}

const decreaseFontSize = () => {
  if (preferences.value.fontSize > 12) {
    updatePreference('fontSize', preferences.value.fontSize - 1)
  }
}

const resetPreferences = async () => {
  try {
    await settingsStore.updatePreferences(defaultPreferences)
    notification.showSuccess(t('settings.preferencesReset'))
  } catch (error) {
    notification.showError(error.message)
  }
}
</script>
