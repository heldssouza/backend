<template>
  <div
    class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow duration-200"
    :class="{ 'animate-pulse': loading }"
  >
    <div class="flex items-start justify-between">
      <div>
        <p class="text-sm font-medium text-gray-600">
          {{ title }}
        </p>
        <div class="mt-2 flex items-baseline">
          <p
            class="text-2xl font-semibold"
            :class="valueColor"
          >
            {{ formattedValue }}
          </p>
          <p
            v-if="change !== undefined"
            class="ml-2 flex items-baseline text-sm font-semibold"
            :class="changeColor"
          >
            <component
              :is="changeIcon"
              class="h-4 w-4 flex-shrink-0 self-center"
              aria-hidden="true"
            />
            <span class="sr-only">
              {{ change >= 0 ? 'Increased' : 'Decreased' }} by
            </span>
            {{ Math.abs(change) }}%
          </p>
        </div>
      </div>
      <div
        class="rounded-lg p-3"
        :class="iconBackgroundColor"
      >
        <component
          :is="icon"
          class="h-6 w-6"
          :class="iconColor"
          aria-hidden="true"
        />
      </div>
    </div>

    <div v-if="showChart && chartData" class="mt-4">
      <div class="h-16">
        <Line
          :data="chartData"
          :options="chartOptions"
        />
      </div>
    </div>

    <div v-if="footer" class="mt-4 text-sm text-gray-600">
      {{ footer }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  ArrowUpIcon,
  ArrowDownIcon,
  UsersIcon,
  BuildingOfficeIcon,
  ServerIcon,
  ChartBarIcon,
  ClockIcon,
  CpuChipIcon,
  DatabaseIcon,
  CloudIcon
} from '@heroicons/vue/24/outline'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend
} from 'chart.js'

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend
)

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  type: {
    type: String,
    default: 'number',
    validator: (value) => ['number', 'percentage', 'currency', 'bytes'].includes(value)
  },
  change: {
    type: Number,
    default: undefined
  },
  trend: {
    type: String,
    default: 'neutral',
    validator: (value) => ['positive', 'negative', 'neutral'].includes(value)
  },
  icon: {
    type: String,
    default: 'ChartBarIcon'
  },
  loading: {
    type: Boolean,
    default: false
  },
  showChart: {
    type: Boolean,
    default: false
  },
  chartData: {
    type: Object,
    default: null
  },
  footer: {
    type: String,
    default: ''
  }
})

// Icon mapping
const iconMap = {
  users: UsersIcon,
  tenants: BuildingOfficeIcon,
  server: ServerIcon,
  chart: ChartBarIcon,
  time: ClockIcon,
  cpu: CpuChipIcon,
  database: DatabaseIcon,
  cloud: CloudIcon
}

// Computed properties
const formattedValue = computed(() => {
  if (props.loading) return '-'
  
  switch (props.type) {
    case 'percentage':
      return `${props.value}%`
    case 'currency':
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(props.value)
    case 'bytes':
      return formatBytes(props.value)
    default:
      return new Intl.NumberFormat('pt-BR').format(props.value)
  }
})

const iconComponent = computed(() => iconMap[props.icon] || ChartBarIcon)

const changeIcon = computed(() => props.change >= 0 ? ArrowUpIcon : ArrowDownIcon)

const valueColor = computed(() => {
  if (props.trend === 'positive') return 'text-success'
  if (props.trend === 'negative') return 'text-error'
  return 'text-primary'
})

const changeColor = computed(() => {
  if (props.change >= 0) return 'text-success'
  return 'text-error'
})

const iconBackgroundColor = computed(() => {
  if (props.trend === 'positive') return 'bg-success/10'
  if (props.trend === 'negative') return 'bg-error/10'
  return 'bg-primary/10'
})

const iconColor = computed(() => {
  if (props.trend === 'positive') return 'text-success'
  if (props.trend === 'negative') return 'text-error'
  return 'text-primary'
})

// Chart options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      enabled: true
    }
  },
  scales: {
    x: {
      display: false
    },
    y: {
      display: false
    }
  },
  elements: {
    line: {
      tension: 0.4
    },
    point: {
      radius: 0
    }
  }
}

// Helper functions
const formatBytes = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}
</script>
