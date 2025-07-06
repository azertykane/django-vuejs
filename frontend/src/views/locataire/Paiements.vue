<template>
  <div class="container py-4">
    <h2 class="mb-4">Mes paiements</h2>

    <ul class="list-group">
      <li
        v-for="p in paiements"
        :key="p.id"
        class="list-group-item d-flex justify-content-between align-items-start flex-wrap"
      >
        <div>
          <strong>Montant :</strong> {{ formatMoney(p.montant) }}<br />
          <strong>Échéance :</strong> {{ formatDate(p.date_echeance) }}<br />
          <strong>Statut :</strong>
          <span :class="badgeClass(p.statut)">
            {{ p.statut.toUpperCase() }}
          </span>
        </div>
        <div>
          <strong>Payé le :</strong>
          {{ p.date_paiement ? formatDate(p.date_paiement) : 'Non payé' }}
        </div>
      </li>
    </ul>

    <p v-if="!paiements.length" class="text-muted mt-3">Aucun paiement enregistré.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const paiements = ref([])

onMounted(async () => {
  const { data } = await api.get('/api/paiements/')
  paiements.value = data
})

function formatDate(date) {
  return new Date(date).toLocaleDateString('fr-FR', {
    weekday: 'short', year: 'numeric', month: 'long', day: 'numeric'
  })
}

function formatMoney(n) {
  return parseFloat(n).toLocaleString('fr-FR', {
    style: 'currency',
    currency: 'XOF'
  })
}

function badgeClass(statut) {
  return statut === 'paye' ? 'badge bg-success' : 'badge bg-danger'
}
</script>
