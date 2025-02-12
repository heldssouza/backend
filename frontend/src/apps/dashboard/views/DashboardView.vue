<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold">{{ $t('dashboard.title') }}</h1>
      <p class="text-gray-600">{{ $t('dashboard.description') }}</p>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Tenants -->
      <MetricCard
        :title="$t('dashboard.activeTenants')"
        :value="metricsStore.activeTenants"
        :change="tenantChange"
        icon="tenants"
        :loading="metricsStore.loading.tenants"
        :trend="tenantChange >= 0 ? 'positive' : 'negative'"
        :footer="$t('dashboard.totalTenants', { total: metricsStore.totalTenants })"
      />

      <!-- Users -->
      <MetricCard
        :title="$t('dashboard.activeUsers')"
        :value="metricsStore.activeUsers"
        :change="userChange"
        icon="users"
        :loading="metricsStore.loading.users"
        :trend="userChange >= 0 ? 'positive' : 'negative'"
        :footer="$t('dashboard.totalUsers', { total: metricsStore.totalUsers })"
      />

      <!-- Storage -->
      <MetricCard
        :title="$t('dashboard.storageUsed')"
        :value="metricsStore.storageUsed"
        type="bytes"
        icon="server"
        :loading="metricsStore.loading.storage"
        :trend="metricsStore.storagePercentage > 80 ? 'negative' : 'neutral'"
        :footer="$t('dashboard.storageTotal', {
          used: formatBytes(metricsStore.storageUsed),
          total: formatBytes(metricsStore.storageTotal)
        })"
      />

      <!-- Performance -->
      <MetricCard
        :title="$t('dashboard.systemHealth')"
        :value="metricsStore.apiSuccessRate"
        type="percentage"
        icon="chart"
        :loading="metricsStore.loading.api"
        :trend="metricsStore.apiSuccessRate >= 98 ? 'positive' : 'negative'"
        :footer="$t('dashboard.lastUpdated', {
          time: formatDate(metricsStore.lastUpdated)
        })"
      />
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- Activity Chart -->
      <ActivityChart
        :title="$t('dashboard.activity')"
        :loading="metricsStore.loading.activity"
        :error="metricsStore.error"
        :data="activityData"
        @period-change="handleActivityPeriodChange"
      />

      <!-- Resource Usage -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-4">{{ $t('dashboard.resourceUsage') }}</h3>
        
        <!-- CPU Usage -->
        <div class="mb-4">
          <div class="flex justify-between mb-1">
            <span class="text-sm font-medium">CPU</span>
            <span class="text-sm text-gray-600">{{ resourceMetrics.cpu }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="bg-primary rounded-full h-2"
              :style="{ width: `${resourceMetrics.cpu}%` }"
              :class="{
                'bg-success': resourceMetrics.cpu < 70,
                'bg-warning': resourceMetrics.cpu >= 70 && resourceMetrics.cpu < 90,
                'bg-error': resourceMetrics.cpu >= 90
              }"
            ></div>
          </div>
        </div>

        <!-- Memory Usage -->
        <div class="mb-4">
          <div class="flex justify-between mb-1">
            <span class="text-sm font-medium">{{ $t('dashboard.memory') }}</span>
            <span class="text-sm text-gray-600">{{ resourceMetrics.memory }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="bg-primary rounded-full h-2"
              :style="{ width: `${resourceMetrics.memory}%` }"
              :class="{
                'bg-success': resourceMetrics.memory < 70,
                'bg-warning': resourceMetrics.memory >= 70 && resourceMetrics.memory < 90,
                'bg-error': resourceMetrics.memory >= 90
              }"
            ></div>
          </div>
        </div>

        <!-- Database Connections -->
        <div class="mb-4">
          <div class="flex justify-between mb-1">
            <span class="text-sm font-medium">{{ $t('dashboard.dbConnections') }}</span>
            <span class="text-sm text-gray-600">{{ resourceMetrics.dbConnections }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="bg-primary rounded-full h-2"
              :style="{ width: `${resourceMetrics.dbConnections}%` }"
              :class="{
                'bg-success': resourceMetrics.dbConnections < 70,
                'bg-warning': resourceMetrics.dbConnections >= 70 && resourceMetrics.dbConnections < 90,
                'bg-error': resourceMetrics.dbConnections >= 90
              }"
            ></div>
          </div>
        </div>

        <!-- Cache Hit Rate -->
        <div>
          <div class="flex justify-between mb-1">
            <span class="text-sm font-medium">{{ $t('dashboard.cacheHitRate') }}</span>
            <span class="text-sm text-gray-600">{{ resourceMetrics.cacheHitRate }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="bg-primary rounded-full h-2"
              :style="{ width: `${resourceMetrics.cacheHitRate}%` }"
              :class="{
                'bg-error': resourceMetrics.cacheHitRate < 70,
                'bg-warning': resourceMetrics.cacheHitRate >= 70 && resourceMetrics.cacheHitRate < 90,
                'bg-success': resourceMetrics.cacheHitRate >= 90
              }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="p-6">
        <h3 class="text-lg font-medium mb-4">{{ $t('dashboard.recentActivity') }}</h3>
        
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr>
                <th>{{ $t('common.time') }}</th>
                <th>{{ $t('common.user') }}</th>
                <th>{{ $t('common.tenant') }}</th>
                <th>{{ $t('common.action') }}</th>
                <th>{{ $t('common.status') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="metricsStore.loading.activity">
                <td colspan="5" class="text-center py-4">
                  <div class="loading loading-spinner loading-lg"></div>
                </td>
              </tr>
              <tr
                v-else-if="recentActivity.length"
                v-for="activity in recentActivity"
                :key="activity.id"
                class="hover"
              >
                <td>{{ formatDate(activity.timestamp) }}</td>
                <td>{{ activity.user }}</td>
                <td>{{ activity.tenant }}</td>
                <td>{{ activity.action }}</td>
                <td>
                  <span
                    class="badge"
                    :class="{
                      'badge-success': activity.status === 'success',
                      'badge-error': activity.status === 'error',
                      'badge-warning': activity.status === 'warning'
                    }"
                  >
                    {{ activity.status }}
                  </span>
                </td>
              </tr>
              <tr v-else>
                <td colspan="5" class="text-center py-4">
                  {{ $t('dashboard.noActivity') }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useMetricsStore } from '../store/metricsStore'
import { useI18n } from 'vue-i18n'
import MetricCard from '../components/MetricCard.vue'
import ActivityChart from '../components/ActivityChart.vue'
import { formatDate } from '@/utils/dateUtils'
import { formatBytes } from '@/utils/formatUtils'

const { t } = useI18n()
const metricsStore = useMetricsStore()

// Refs
const refreshInterval = ref(null)
const activityPeriod = ref('7d')

// Computed
const tenantChange = computed(() => {
  if (!metricsStore.tenantMetrics?.previousActive) return 0
  const previous = metricsStore.tenantMetrics.previousActive
  const current = metricsStore.tenantMetrics.active
  return ((current - previous) / previous) * 100
})

const userChange = computed(() => {
  if (!metricsStore.userMetrics?.previousActive) return 0
  const previous = metricsStore.userMetrics.previousActive
  const current = metricsStore.userMetrics.active
  return ((current - previous) / previous) * 100
})

const activityData = computed(() => {
  if (!metricsStore.activityMetrics) return null
  return {
    labels: metricsStore.activityMetrics.labels,
    logins: metricsStore.activityMetrics.logins,
    actions: metricsStore.activityMetrics.actions,
    errors: metricsStore.activityMetrics.errors
  }
})

const resourceMetrics = computed(() => ({
  cpu: metricsStore.resourceMetrics?.cpu || 0,
  memory: metricsStore.resourceMetrics?.memory || 0,
  dbConnections: metricsStore.resourceMetrics?.dbConnections || 0,
  cacheHitRate: metricsStore.cacheMetrics?.hitRate || 0
}))

const recentActivity = computed(() => metricsStore.activityMetrics?.recent || [])

// Methods
const loadMetrics = async () => {
  try {
    await metricsStore.fetchAllMetrics()
  } catch (error) {
    console.error('Error loading metrics:', error)
  }
}

const handleActivityPeriodChange = async (period) => {
  activityPeriod.value = period
  try {
    await metricsStore.fetchActivityMetrics({ period })
  } catch (error) {
    console.error('Error loading activity metrics:', error)
  }
}

const startRefreshInterval = () => {
  refreshInterval.value = setInterval(loadMetrics, 60000) // Refresh every minute
}

// Lifecycle
onMounted(() => {
  loadMetrics()
  startRefreshInterval()
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>
