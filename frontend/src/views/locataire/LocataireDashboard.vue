<template>
  <div class="dashboard">
    <!-- —————————————————— Barre latérale —————————————————— -->
    <aside class="sidebar bg-primary text-white p-4">
  <h4 class="mb-4 text-center">👤 Locataire</h4>
  <ul class="nav flex-column gap-2">
    <li class="nav-item">
      <router-link to="/locataire/dashboard" class="nav-link text-white">
        <i class="fas fa-home me-2"></i> Tableau de bord
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/locataire/locations" class="nav-link text-white">
        <i class="fas fa-door-open me-2"></i> Mes Locations
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/locataire/paiements" class="nav-link text-white">
        <i class="fas fa-wallet me-2"></i> Payer mon Loyer
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/locataire/notifications" class="nav-link text-white">
        <i class="fas fa-bell me-2"></i> Notifications
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/locataire/contrats" class="nav-link text-white">
        <i class="fas fa-file-signature me-2"></i> Contrats
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/locataire/problemes" class="nav-link text-white">
        <i class="fas fa-history me-2"></i> Problemes
      </router-link>
    </li>

    <li class="nav-item mt-4">
      <button @click="logout" class="btn btn-outline-light w-100">
        <i class="fas fa-sign-out-alt me-2"></i> Déconnexion
      </button>
    </li>
  </ul>
</aside>


    <!-- —————————————————— Contenu principal —————————————————— -->
    <main class="content">
      <h1 class="mb-3">Bienvenue, {{ displayName }}</h1>

      <!-- Recherche -->
      <div class="input-group mb-4">
        <span class="input-group-text"><i class="fas fa-search" /></span>
        <input
          v-model="search"
          class="form-control"
          placeholder="Rechercher (titre, type, adresse)..." />
      </div>

      <!-- Liste des chambres -->
      <div v-if="loaded" class="row g-4">
        <div
          v-for="c in filteredChambres"
          :key="c.id"
          class="col-md-4">
          <div class="card h-100 shadow-sm">
            <img
              :src="c.medias[0]?.fichier || placeholder"
              class="card-img-top img-cover"
              alt="photo" />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ c.titre }}</h5>
              <p class="card-text small flex-grow-1">
                {{ c.description.slice(0, 80) }}…
              </p>
              <p class="mb-2">
                <i class="fas fa-map-marker-alt" />
                {{ c.maison?.adresse || 'Adresse non disponible' }}
              </p>
              <div class="d-flex justify-content-between align-items-center">
                <span class="badge bg-primary">
                  {{ formatMoney(c.prix) }} / {{ c.periodicite }}
                </span>
                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="openModal(c)">
                  Voir&nbsp;+
                </button>
              </div>
            </div>
          </div>
        </div>
        <p v-if="!filteredChambres.length" class="text-muted">
          Aucune chambre ne correspond à la recherche.
        </p>
      </div>

      <div v-else class="text-center py-5">
        <div class="spinner-border text-primary" />
      </div>
    </main>

    <!-- ———————————— Modal détail / RDV ———————————— -->
    <b-modal
      id="modal-detail"
      v-model="showModal"
      :title="selected?.titre"
      hide-footer
      size="lg">
      <template #default>
        <div v-if="selected">
          <!-- Carousel -->
          <b-carousel
            v-if="selected.medias.length"
            controls
            indicators
            background="#000"
            class="mb-3">
            <b-carousel-slide
              v-for="m in selected.medias"
              :key="m.id"
              :img-src="m.fichier" />
          </b-carousel>
          <img
            v-else
            :src="placeholder"
            alt="placeholder"
            class="w-100 mb-3 rounded" />

          <p><strong>Adresse :</strong> {{ selected.maison?.adresse || 'Adresse non disponible' }}</p>
          <p><strong>Description :</strong> {{ selected.description }}</p>
          <p>
            <strong>Prix :</strong>
            {{ formatMoney(selected.prix) }} — <em>{{ selected.periodicite }}</em>
          </p>

          <!-- RDV -->
          <hr />
          <h5>Demande de visite</h5>
          <div class="row g-2 align-items-end">
            <div class="col-md-8">
              <label class="form-label small">Date &amp; heure</label>
              <input
                v-model="rdvDate"
                type="datetime-local"
                class="form-control" />
            </div>
            <div class="col-md-4 d-grid">
              <button
                class="btn btn-success"
                :disabled="!rdvDate || loadingRdv"
                @click="sendRdv">
                <span
                  v-if="loadingRdv"
                  class="spinner-border spinner-border-sm me-1" />
                Envoyer
              </button>
            </div>
          </div>
          <div v-if="rdvMsg" class="alert alert-info mt-3">{{ rdvMsg }}</div>
        </div>
      </template>
    </b-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import api from '@/services/api'

const router = useRouter()
const store = useStore()

/* ——— Etat ——— */
const search = ref('')
const chambres = ref([])
const loaded = ref(false)

const selected = ref(null)
const rdvDate = ref('')
const loadingRdv = ref(false)
const rdvMsg = ref('')
const showModal = ref(false)

/* placeholder générique */
const placeholder =
  'https://via.placeholder.com/600x400?text=Pas+de+photo'

/* ——— Computed ——— */
const displayName = computed(() =>
  store.state.user?.nom || store.state.user?.email || 'Utilisateur'
)

const filteredChambres = computed(() => {
  if (!search.value.trim()) return chambres.value
  const q = search.value.toLowerCase()
  return chambres.value.filter(c =>
    c.titre.toLowerCase().includes(q) ||
    c.type.toLowerCase().includes(q) ||
    (c.maison?.adresse && c.maison.adresse.toLowerCase().includes(q))
  )
})

/* ——— Lifecycle ——— */
onMounted(fetchChambres)

async function fetchChambres() {
  loaded.value = false
  try {
    const { data } = await api.get('/api/chambres/')
    chambres.value = data
  } finally {
    loaded.value = true
  }
}

/* ——— Actions ——— */
function openModal(c) {
  selected.value = c
  rdvDate.value = ''
  rdvMsg.value = ''
  loadingRdv.value = false
  showModal.value = true
}

async function sendRdv() {
  loadingRdv.value = true
  rdvMsg.value = ''
  try {
    await api.post('/api/rendezvous/', {
      chambre: selected.value.id,
      date_heure: rdvDate.value
    })
    rdvMsg.value = 'Votre demande a bien été envoyée.'
    setTimeout(() => {
      showModal.value = false
    }, 1500) // Fermer après 1.5s
  } catch {
    rdvMsg.value = 'Erreur lors de l’envoi de la demande.'
  } finally {
    loadingRdv.value = false
  }
}

async function logout() {
  await store.dispatch('logout')
  router.push('/')
}

/* ——— Helper ——— */
function formatMoney(n) {
  return parseInt(n, 10).toLocaleString('fr-FR', {
    style: 'currency',
    currency: 'XOF'
  })
}
</script>

<style scoped>
.dashboard { display: flex; min-height: 100vh; }
.sidebar   { width: 300px; background: #007bff; color: #fff; padding: 20px;  }
.sidebar h2 { font-size: 30px; margin-bottom: 20px; }
.sidebar ul { list-style: none; padding: 0; }
.sidebar li { margin-bottom: 10px; }
.sidebar a, .sidebar button {
  color: #fff;
  background: none;
  border: none;
  font-size: 25px;
  cursor: pointer;
}
.sidebar a:hover,
.sidebar button:hover {
  text-decoration: underline;
}
.content    { flex: 1; padding: 40px; }
.img-cover  { height: 180px; object-fit: cover; }

@media (max-width: 767px) {
  .sidebar { display: none; }
}
</style>
