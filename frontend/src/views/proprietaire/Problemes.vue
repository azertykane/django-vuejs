<template>
  <div class="container py-4">
    <h2 class="mb-4">Problèmes signalés par les locataires</h2>

    <ul class="list-group">
      <li
        v-for="p in problemes"
        :key="p.id"
        class="list-group-item"
      >
        <strong>Locataire :</strong> {{ p.signale_par.nom || p.signale_par.email }}<br />
        <strong>Chambre :</strong> {{ p.contrat.chambre.titre }}<br />
        <strong>Type :</strong> {{ p.type }} |
        <strong>Responsable :</strong> {{ p.responsable }} |
        <strong>Résolu :</strong>
        <span :class="p.resolu ? 'text-success' : 'text-danger'">
          {{ p.resolu ? 'Oui' : 'Non' }}
        </span>
        <br />
        <em>{{ p.description }}</em>
      </li>
    </ul>

    <p v-if="!problemes.length" class="text-muted mt-3">Aucun problème signalé.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const problemes = ref([])

onMounted(async () => {
  const { data } = await api.get('/api/problemes/')
  problemes.value = data
})
</script>
