<template>
  <div class="relative">
    <button
      type="button"
      class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      @click="toggleDropdown"
    >
      <span class="sr-only">{{ $t('common.changeLanguage') }}</span>
      <span class="text-sm font-medium">{{ currentLanguage.toUpperCase() }}</span>
    </button>

    <!-- Dropdown menu -->
    <div
      v-if="isOpen"
      class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="language-menu-button"
      tabindex="-1"
    >
      <a
        v-for="lang in availableLanguages"
        :key="lang.code"
        href="#"
        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
        :class="{ 'bg-gray-100': currentLanguage === lang.code }"
        @click.prevent="changeLanguage(lang.code)"
        role="menuitem"
        tabindex="-1"
      >
        {{ lang.name }}
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import eventBus, { EventTypes } from '@/infrastructure/events/eventBus'

const { locale } = useI18n()
const isOpen = ref(false)

const availableLanguages = [
  { code: 'pt-BR', name: 'Português' },
  { code: 'en-US', name: 'English' },
  { code: 'es-ES', name: 'Español' }
]

const currentLanguage = computed(() => locale.value)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const changeLanguage = (lang) => {
  locale.value = lang
  localStorage.setItem('language', lang)
  isOpen.value = false
  eventBus.emit(EventTypes.LANGUAGE_CHANGED, lang)
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (isOpen.value && !event.target.closest('.relative')) {
    isOpen.value = false
  }
}

// Add/remove event listener
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
