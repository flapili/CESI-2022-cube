
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/users', component: () => import('pages/Users.vue') },
    ]
  },

  { path: '/error', component: () => import('pages/Error/ErrorWithMessage.vue') },
  { path: '/welcome', component: () => import('pages/Welcome.vue') },
  { path: '/reset_password', component: () => import('pages/ResetPassword.vue') },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error/Error404.vue')
  }
]

export default routes
