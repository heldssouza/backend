<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-medium">{{ title }}</h3>
      
      <!-- Period selector -->
      <div class="flex items-center space-x-2">
        <button
          v-for="period in periods"
          :key="period.value"
          class="btn btn-sm"
          :class="selectedPeriod === period.value ? 'btn-primary' : 'btn-ghost'"
          @click="handlePeriodChange(period.value)"
        >
          {{ period.label }}
        </button>
      </div>
    </div>

    <div
      class="h-[300px]"
      :class="{ 'animate-pulse': loading }"
    >
      <Bar
        v-if="!loading && chartData"
        :data="chartData"
        :options="chartOptions"
      />
      <div
        v-else-if="error"
        class="flex items-center justify-center h-full"
      >
        <p class="text-error">{{ error }}</p>
      </div>
      <div
        v-else-if="loading"
        class="flex items-center justify-center h-full"
      >
        <div class="loading loading-spinner loading-lg"></div>
      </div>
    </div>

    <!-- Legend -->
    <div class="mt-4 flex items-center justify-center space-x-6">
      <div
        v-for="dataset in chartData?.datasets"
        :key="dataset.label"
        class="flex items-center space-x-2"
      >
        <span
          class="inline-block w-3 h-3 rounded-full"
          :style="{ backgroundColor: dataset.backgroundColor }"
        ></span>
        <span class="text-sm text-gray-600">{{ dataset.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar } from 'vue-chartjs'

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  data: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['period-change'])

// State
const selectedPeriod = ref('7d')

// Constants
const periods = [
  { label: '7D', value: '7d' },
  { label: '30D', value: '30d' },
  { label: '90D', value: '90d' }
]

// Chart options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || ''
          if (label) {
            label += ': '
          }
          label += new Intl.NumberFormat('pt-BR').format(context.parsed.y)
          return label
        }
      }
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.1)'
      },
      ticks: {
        callback: function(value) {
          return new Intl.NumberFormat('pt-BR').format(value)
        }
      }
    }
  },
  interaction: {
    intersect: false,
    mode: 'index'
  }
}

// Computed
const chartData = computed(() => {
  if (!props.data) return null

  return {
    labels: props.data.labels,
    datasets: [
      {
        label: 'Logins',
        data: props.data.logins,
        backgroundColor: 'rgba(59, 130, 246, 0.5)', // blue-500
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 1
      },
      {
        label: 'Ações',
        data: props.data.actions,
        backgroundColor: 'rgba(16, 185, 129, 0.5)', // green-500
        borderColor: 'rgb(16, 185, 129)',
        borderWidth: 1
      },
      {
        label: 'Erros',
        data: props.data.errors,
        backgroundColor: 'rgba(239, 68, 68, 0.5)', // red-500
        borderColor: 'rgb(239, 68, 68)',
        borderWidth: 1
      }
    ]
  }
})

// Methods
const handlePeriodChange = (period) => {
  selectedPeriod.value = period
  emit('period-change', period)
}

// Watch for data changes
watch(() => props.data, () => {
  if (props.data) {
    // You could add animations or transitions here
  }
})

// Initialize
onMounted(() => {
  emit('period-change', selectedPeriod.value)
})
</script>
