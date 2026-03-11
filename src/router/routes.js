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
    path: '/continue',
    component: () => import('layouts/MainLayout.vue'), 
    children: [
      { path: '', component: () => import('pages/UserPage.vue') }
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
    path: '/charities',
    component: () => import('layouts/MainLayout.vue'), 
    children: [
      { path: '', component: () => import('pages/ProjectPage.vue') }
    ],
  },


  
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
