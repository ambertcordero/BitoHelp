const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'donate', component: () => import('pages/DonatePage.vue') },
      { path: 'donor', component: () => import('pages/DonorPage.vue') },
      { path: 'charity', component: () => import('pages/CharityPage.vue') },
      { path: 'dashboard', component: () => import('pages/DashboardPage.vue') },
      { path: 'charities', component: () => import('pages/ProjectPage.vue') },
      { path: 'user', component: () => import('pages/UserPage.vue') },
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
