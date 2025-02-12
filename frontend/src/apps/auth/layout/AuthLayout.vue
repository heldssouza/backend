<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <img class="mx-auto h-12 w-auto" src="@/assets/logo.svg" alt="Logo" />
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        {{ $route.meta.title ? $t($route.meta.title) : $t('auth.welcome') }}
      </h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <router-view></router-view>
      </div>

      <!-- Language Selector -->
      <div class="mt-6 text-center">
        <LanguageSelector />
      </div>
    </div>
  </div>
</template>

<script setup>
import LanguageSelector from '@/shared/components/common/LanguageSelector.vue'
</script>
