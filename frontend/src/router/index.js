import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Layouts
import DefaultLayout from '@/layouts/DefaultLayout.vue'

// Views
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import UsersView from '@/views/UsersView.vue'
import CompaniesView from '@/views/CompaniesView.vue'
import ContasView from '@/views/ContasView.vue'
import RazaoView from '@/views/RazaoView.vue'
import SaldosView from '@/views/SaldosView.vue'
import GrupoContasView from '@/views/GrupoContasView.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { 
      requiresAuth: false,
      title: 'Login'
    }
  },
  {
    path: '/',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: DashboardView,
        meta: {
          title: 'Dashboard',
          description: 'Dashboard principal'
        }
      },
      {
        path: 'users',
        name: 'users',
        component: UsersView,
        meta: {
          title: 'Usuários',
          description: 'Gerenciamento de usuários'
        }
      },
      {
        path: 'companies',
        name: 'companies',
        component: CompaniesView,
        meta: {
          title: 'Empresas',
          description: 'Gerenciamento de empresas'
        }
      },
      {
        path: 'contas',
        name: 'contas',
        component: ContasView,
        meta: {
          title: 'Contas',
          description: 'Gerenciamento de contas'
        }
      },
      {
        path: 'razao',
        name: 'razao',
        component: RazaoView,
        meta: {
          title: 'Razão',
          description: 'Lançamentos contábeis'
        }
      },
      {
        path: 'saldos',
        name: 'saldos',
        component: SaldosView,
        meta: {
          title: 'Saldos',
          description: 'Saldos das contas'
        }
      },
      {
        path: 'grupocontas',
        name: 'grupocontas',
        component: GrupoContasView,
        meta: {
          title: 'Grupos de Contas',
          description: 'Gerenciamento de grupos de contas'
        }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  document.title = `${to.meta.title || 'Dashboard'} - Vue App`

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
