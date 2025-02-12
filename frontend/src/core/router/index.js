import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/core/store/auth'

const routes = [
  {
    path: '/',
    component: () => import('@/shared/components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/apps/admin/views/DashboardView.vue'),
        meta: { permission: 'view_dashboard' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/apps/user/views/ProfileView.vue')
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/apps/admin/views/UsersView.vue'),
        meta: { permission: 'manage_users' }
      },
      {
        path: 'tenants',
        name: 'Tenants',
        component: () => import('@/apps/tenant/views/TenantsView.vue'),
        meta: { permission: 'manage_tenants' }
      },
      {
        path: 'roles',
        name: 'Roles',
        component: () => import('@/apps/admin/views/RolesView.vue'),
        meta: { permission: 'manage_roles' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/apps/settings/views/SettingsView.vue'),
        children: [
          {
            path: '',
            redirect: '/settings/profile'
          },
          {
            path: 'profile',
            name: 'SettingsProfile',
            component: () => import('@/apps/settings/components/ProfileSettings.vue')
          },
          {
            path: 'preferences',
            name: 'SettingsPreferences',
            component: () => import('@/apps/settings/components/PreferencesSettings.vue')
          }
        ]
      }
    ]
  },
  {
    path: '/auth',
    component: () => import('@/apps/auth/layout/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/apps/auth/views/LoginView.vue')
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('@/apps/auth/views/RegisterView.vue')
      },
      {
        path: 'forgot-password',
        name: 'ForgotPassword',
        component: () => import('@/apps/auth/views/ForgotPasswordView.vue')
      },
      {
        path: 'reset-password',
        name: 'ResetPassword',
        component: () => import('@/apps/auth/views/ResetPasswordView.vue')
      }
    ]
  },
  {
    path: '/forbidden',
    name: 'Forbidden',
    component: () => import('@/shared/components/error/ForbiddenView.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/shared/components/error/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiredPermission = to.meta.permission

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (requiredPermission && !authStore.hasPermission(requiredPermission)) {
    next({ name: 'Forbidden' })
  } else {
    next()
  }
})

export default router
