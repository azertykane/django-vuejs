<template>
  <div class="container py-4">
    <h2 class="mb-4">Mes notifications</h2>

    <!-- ===== Demandes de visite ===== -->
    <section class="mb-5">
      <h4 class="mb-3">Mes demandes de visite</h4>
      <ul class="list-group">
        <li
          v-for="rdv in rendezvous"
          :key="rdv.id"
          class="list-group-item d-flex justify-content-between align-items-start flex-wrap"
        >
          <div>
            <strong>Chambre :</strong> {{ rdv.chambre.titre }}<br />
            <strong>Date :</strong> {{ formatDate(rdv.date_heure) }}<br />
            <span :class="badgeClass(rdv.statut)">
              {{ rdv.statut.toUpperCase() }}
            </span>
          </div>
        </li>
      </ul>
      <p v-if="!rendezvous.length" class="text-muted mt-3">
        Aucune demande de visite.
      </p>
    </section>

    <!-- ===== Contrats ===== -->
    <section>
      <h4 class="mb-3">Mes contrats</h4>
      <ul class="list-group">
        <li
          v-for="c in contrats"
          :key="c.id"
          class="list-group-item d-flex justify-content-between align-items-start flex-wrap"
        >
          <div>
            <strong>Chambre :</strong> {{ c.chambre.titre }}<br />
            <strong>Loyer :</strong> {{ formatMoney(c.chambre.prix) }} / {{ c.periodicite }}<br />
            <span :class="badgeClassContrat(c.statut)">
              {{ c.statut.toUpperCase() }}
            </span>
          </div>

          <!-- Boutons d'action -->
          <div v-if="c.statut === 'propose'" class="btn-group mt-2">
            <button class="btn btn-sm btn-success" @click="accepterContrat(c.id)">
              Accepter
            </button>
            <button class="btn btn-sm btn-outline-danger" @click="refuserContrat(c.id)">
              Refuser
            </button>
          </div>
        </li>
      </ul>
      <p v-if="!contrats.length" class="text-muted mt-3">
        Aucun contrat pour le moment.
      </p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const rendezvous = ref([])
const contrats   = ref([])

onMounted(() => {
  fetchRendezvous()
  fetchContrats()
})

async function fetchRendezvous() {
  const { data } = await api.get('/api/rendezvous/')
  rendezvous.value = data
}

async function fetchContrats() {
  const { data } = await api.get('/api/contrats/')
  contrats.value = data
}

async function accepterContrat(id) {
  try {
    await api.post(`/api/contrats/${id}/accepter/`)
    alert("Contrat accepté. Le propriétaire sera notifié.")
    fetchContrats()
  } catch (err) {
    alert("Erreur lors de l'acceptation du contrat")
  }
}

async function refuserContrat(id) {
  try {
    await api.post(`/api/contrats/${id}/refuser/`)
    alert("Contrat refusé.")
    fetchContrats()
  } catch (err) {
    alert("Erreur lors du refus du contrat")
  }
}

function formatDate(str) {
  return new Date(str).toLocaleString('fr-FR')
}

function formatMoney(n) {
  return parseInt(n, 10).toLocaleString('fr-FR', {
    style: 'currency',
    currency: 'XOF'
  })
}

function badgeClass(statut) {
  if (statut === 'en_attente') return 'badge bg-warning'
  if (statut === 'confirme')   return 'badge bg-success'
  if (statut === 'refuse')     return 'badge bg-danger'
  return 'badge bg-secondary'
}

function badgeClassContrat(statut) {
  if (statut === 'propose')  return 'badge bg-info'
  if (statut === 'accepte')  return 'badge bg-success'
  if (statut === 'refuse')   return 'badge bg-danger'
  return 'badge bg-secondary'
}
</script>
