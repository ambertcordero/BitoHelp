const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ],
  },
  {
    path: '/donate',
    component: () => import('layouts/MainLayout.vue'), 
    children: [
      { path: '', component: () => import('pages/DonatePage.vue') }
    ],
  },
  {
    path: '/donor',
    component: () => import('layouts/MainLayout.vue'), 
    children: [
      { path: '', component: () => import('pages/DonorPage.vue') }
    ],
  },
  {
    path: '/charity',
    component: () => import('layouts/MainLayout.vue'), 
    children: [
      { path: '', component: () => import('pages/CharityPage.vue') }
    ],
  },
  {
    path: '/dashboard',
    component: () => import('layouts/MainLayout.vue'), 
    children: [
      { path: '', component: () => import('pages/DashboardPage.vue') }
    ],
  },
  {
    path: '/charities',
    component: () => import('layouts/MainLayout.vue'), 
    children: [
      { path: '', component: () => import('pages/ProjectPage.vue') }
    ],
  },
  {
    path: '/donor',
    component: () => import('layouts/MainLayout.vue'), 
    children: [
      { path: '', component: () => import('pages/DonorPage.vue') }
    ],
  },


  
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
