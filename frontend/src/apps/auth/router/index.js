export default [
  {
    path: '/auth',
    component: () => import('../layout/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('../views/LoginView.vue'),
        meta: {
          title: 'auth.login',
          requiresAuth: false
        }
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('../views/RegisterView.vue'),
        meta: {
          title: 'auth.register',
          requiresAuth: false
        }
      },
      {
        path: 'forgot-password',
        name: 'ForgotPassword',
        component: () => import('../views/ForgotPasswordView.vue'),
        meta: {
          title: 'auth.forgotPassword',
          requiresAuth: false
        }
      },
      {
        path: 'reset-password',
        name: 'ResetPassword',
        component: () => import('../views/ResetPasswordView.vue'),
        meta: {
          title: 'auth.resetPassword',
          requiresAuth: false
        }
      },
      {
        path: 'verify-email',
        name: 'VerifyEmail',
        component: () => import('../views/VerifyEmailView.vue'),
        meta: {
          title: 'auth.verifyEmail',
          requiresAuth: false
        }
      }
    ]
  }
]
