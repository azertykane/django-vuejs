<template>
  <div class="container py-4">
    <h2 class="mb-4">Réglages Paiement</h2>

    <b-form @submit.prevent="save">
      <b-row class="mb-3">
        <b-col md="6">
          <b-form-group label="Périodicité par défaut">
            <b-form-select v-model="periodicite" :options="periodicites" />
          </b-form-group>
        </b-col>

        <b-col md="6">
          <b-form-group label="Mode de paiement par défaut">
            <b-form-select v-model="mode" :options="modes" />
          </b-form-group>
        </b-col>
      </b-row>

      <b-button type="submit" variant="primary">Enregistrer</b-button>
    </b-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const periodicite  = ref('mensuel')
const mode         = ref('mobile money')

const periodicites = [
  { value: 'journalier',   text: 'Journalier' },
  { value: 'hebdomadaire', text: 'Hebdomadaire' },
  { value: 'mensuel',      text: 'Mensuel' },
]
const modes = ['virement', 'cash', 'mobile money']

onMounted(async () => {
  try {
    const { data } = await api.get('/api/reglages-paiement/')
    periodicite.value = data.periodicite
    mode.value        = data.mode
  } catch (e) {
    alert('Erreur lors du chargement des réglages.')
  }
})

async function save () {
  try {
    await api.put('/api/reglages-paiement/', {
      periodicite: periodicite.value,
      mode:        mode.value,
    })
    alert('Réglages enregistrés !')
  } catch (e) {
    alert('Erreur lors de l’enregistrement.')
  }
}
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: auto;
}
</style>
