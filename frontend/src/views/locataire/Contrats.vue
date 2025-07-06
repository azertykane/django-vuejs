<template>
  <div class="p-4">
    <h2 class="mb-4">Mes contrats de location</h2>

    <div
      v-for="contrat in contrats"
      :key="contrat.id"
      class="card mb-4 shadow-sm">
      <div class="card-body">
        <h5 class="card-title">{{ contrat.chambre.titre }}</h5>
        <p>
          <strong>Période :</strong>
          du {{ formatDate(contrat.date_debut) }} au {{ formatDate(contrat.date_fin) }}
        </p>
        <p><strong>Montant caution :</strong> {{ formatMoney(contrat.montant_caution) }}</p>
        <p><strong>Statut :</strong> {{ contrat.statut }}</p>
        <hr />
        <h6>Paiements</h6>
        <ul class="list-group">
          <li
            v-for="p in contrat.paiements"
            :key="p.id"
            class="list-group-item d-flex justify-content-between align-items-center">
            Échéance : {{ formatDate(p.date_echeance) }}
            <span :class="['badge', p.statut === 'payé' ? 'bg-success' : 'bg-warning']">
              {{ p.statut }}
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const contrats = ref([])

onMounted(fetchContrats)

async function fetchContrats() {
  const { data } = await api.get('/api/contrats/')
  for (const c of data) {
    const { data: paiements } = await api.get(`/api/paiements/?contrat=${c.id}`)
    c.paiements = paiements
  }
  contrats.value = data
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('fr-FR')
}

function formatMoney(n) {
  return parseInt(n, 10).toLocaleString('fr-FR', {
    style: 'currency',
    currency: 'XOF'
  })
}
</script>
