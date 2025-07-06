// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

/* ───────────── 1. Routes ───────────── */
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/locataire/dashboard',
    name: 'LocataireDashboard',
    component: () => import('@/views/locataire/LocataireDashboard.vue'),
    meta: { requiresAuth: true, role: 'locataire' },
  },
                     /*---------proprio---------------- */
  {
    path: '/proprietaire/dashboard',
    name: 'ProprietaireDashboard',
    component: () => import('@/views/proprietaire/ProprietaireDashboard.vue'),
    meta: { requiresAuth: true, role: 'proprietaire' },
  },
  {
  path: '/proprietaire/biens',
  name: 'ProprietaireBiens',
  component: () => import('@/views/proprietaire/Biens.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' },
},
{
  path: '/proprietaire/chambres',
  name: 'ProprietaireChambres',
  component: () => import('@/views/proprietaire/Chambres.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' },
},
{
  path: '/proprietaire/locataires',
  name: 'ProprietaireLocataires',
  component: () => import('@/views/proprietaire/Locataires.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' },
},
{
  path: '/proprietaire/paiements',
  name: 'ProprietairePaiements',
  component: () => import('@/views/proprietaire/Paiements.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' },
},
{
  path: '/proprietaire/dashboard-paiements',
  name: 'ProprietaireDashPaiements',
  component: () => import('@/views/proprietaire/DashboardPaiements.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' },
},
{
  path: '/proprietaire/reglages-paiement',
  name: 'ProprietaireReglages',
  component: () => import('@/views/proprietaire/ReglagesPaiement.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' },
},
{
  path: '/proprietaire/maisons/ajouter',
  name: 'CreateMaison',
  component: () => import('@/views/maisons/CreateMaison.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' },
},
{
  path: '/proprietaire/chambres/ajouter',
  name: 'CreateChambre',
  component: () => import('@/views/chambres/CreateChambre.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' },
},
/*------------------------------------------------------------------*/
{
  path: '/locataire/notifications',
  name: 'LocataireNotifications',
  component: () => import('@/views/locataire/Notifications.vue'),
  meta: { requiresAuth: true, role: 'locataire' },
},
{
  path: '/proprietaire/notifications',
  name: 'ProprietaireNotifications',
  component: () => import('@/views/proprietaire/Notifications.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' },
}, 
/*---------------contrats--------------- */
{
  path: '/locataire/contrats',
  name: 'LocataireContrats',
  component: () => import('@/views/locataire/Contrats.vue'),
  meta: { requiresAuth: true, role: 'locataire' }
},
{
  path: '/proprietaire/contrats',
  name: 'ProprietaireContrats',
  component: () => import('@/views/proprietaire/Contrats.vue'),
  meta: { requiresAuth: true, role: 'proprietaire' }
},
{
  path: "/locataire/paiements",
  name: "LocatairePaiements",
  component: () => import("@/views/locataire/Paiements.vue"),
},
{
  path: "/locataire/problemes",
  name: "LocataireProblemes",
  component: () => import("@/views/locataire/Problemes.vue"),
},
{
  path: "/proprietaire/paiements",
  name: "ProprietairePaiements",
  component: () => import("@/views/proprietaire/Paiements.vue"),
},
{
  path: "/proprietaire/problemes",
  name: "ProprietaireProblemes",
  component: () => import("@/views/proprietaire/Problemes.vue"),
},
{
    path: '/property/:id',
    name: 'PropertyDetail',
    component: () => import('@/views/chambres/PropertyDetail.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

/* ───────────── 2. Création du router ───────────── */
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL || '/'),
  routes,
  scrollBehavior(to, _from, saved) {
    return saved || { top: 0 }
  },
})

/* ───────────── 3. Navigation-guard global ───────────── */
router.beforeEach(async (to, _from, next) => {
  const isAuth  = store.getters.isAuthenticated           // token présent ?
  const user    = store.state.user                        // profil déjà chargé
  const userRole = store.getters.userRole                 // 'locataire' / 'proprietaire'

  /* — Charger le profil s’il manque mais qu’on possède un token — */
  if (isAuth && !user) {
    try { await store.dispatch('fetchUser') } catch { await store.dispatch('logout') }
  }

  /* — Routes protégées : exige la connexion — */
  if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
    return next({ path: '/login', query: { redirect: to.fullPath } })
  }

  /* — Empêcher un utilisateur connecté d’aller sur login/register — */
  if (to.meta.guestOnly && store.getters.isAuthenticated) {
    return next(
      userRole === 'proprietaire'
        ? '/proprietaire/dashboard'
        : '/locataire/dashboard'
    )
  }

  /* — Vérification du rôle pour les dashboards — */
  if (to.meta.role && userRole && userRole !== to.meta.role) {
    return next(
      userRole === 'proprietaire'
        ? '/proprietaire/dashboard'
        : '/locataire/dashboard'
    )
  }

  next()
})

export default router
