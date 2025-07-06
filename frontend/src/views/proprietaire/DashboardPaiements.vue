<template>
  <div>
    <h3 class="mb-4">Statistiques Paiements</h3>
    <canvas ref="chartEl"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Chart } from 'chart.js/auto'
import api from '@/services/api'

const chartEl = ref(null)

onMounted(async () => {
  const { data } = await api.get('/api/paiements/mes/')
  const payes   = data.filter(p => p.statut === 'payé').length
  const impayes = data.filter(p => p.statut === 'impayé').length

  new Chart(chartEl.value, {
    type: 'doughnut',
    data: {
      labels: ['Payés', 'Impayés'],
      datasets: [{
        data: [payes, impayes],
      }],
    },
  })
})
</script>
