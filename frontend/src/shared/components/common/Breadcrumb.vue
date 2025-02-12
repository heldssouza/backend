<template>
  <nav class="flex" aria-label="Breadcrumb">
    <ol class="flex items-center space-x-4">
      <li>
        <div>
          <router-link
            :to="{ name: 'Dashboard' }"
            class="text-gray-400 hover:text-gray-500"
          >
            <svg
              class="flex-shrink-0 h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"
              />
            </svg>
            <span class="sr-only">{{ $t('common.home') }}</span>
          </router-link>
        </div>
      </li>

      <li v-for="(crumb, index) in breadcrumbs" :key="index">
        <div class="flex items-center">
          <!-- Separator -->
          <svg
            class="flex-shrink-0 h-5 w-5 text-gray-300"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
          </svg>

          <!-- Link or Text -->
          <router-link
            v-if="crumb.to"
            :to="crumb.to"
            class="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700"
          >
            {{ $t(crumb.text) }}
          </router-link>
          <span
            v-else
            class="ml-4 text-sm font-medium text-gray-500"
          >
            {{ $t(crumb.text) }}
          </span>
        </div>
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const breadcrumbs = computed(() => {
  const crumbs = []
  const pathSegments = route.path.split('/').filter(Boolean)

  let currentPath = ''
  pathSegments.forEach((segment, index) => {
    currentPath += `/${segment}`
    
    // Verifica se é a última parte do caminho
    const isLast = index === pathSegments.length - 1

    // Adiciona o breadcrumb
    crumbs.push({
      text: `navigation.${segment}`,
      to: isLast ? null : currentPath
    })
  })

  return crumbs
})
</script>
