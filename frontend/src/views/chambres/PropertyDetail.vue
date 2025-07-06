<template>
  <div v-if="chambre">
    <h1 class="mb-4">{{ chambre.titre }}</h1>
    <img
      v-if="chambre.medias.length"
      :src="chambre.medias[0].fichier"
      class="img-fluid mb-3"
    />
    <p>{{ chambre.description }}</p>
    <ul class="list-group mb-3">
      <li class="list-group-item">Prix : {{ chambre.prix }} € / {{ chambre.periodicite }}</li>
      <li class="list-group-item">Taille : {{ chambre.taille }}</li>
      <li class="list-group-item">Type : {{ chambre.type }}</li>
      <li class="list-group-item" :class="{'text-success': chambre.disponible, 'text-danger': !chambre.disponible}">
        {{ chambre.disponible ? 'Disponible' : 'Indisponible' }}
      </li>
    </ul>
    <button class="btn btn-primary" @click="prendreRDV" :disabled="!chambre.disponible">
      Prendre rendez-vous
    </button>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const chambre = ref(null)

onMounted(async () => {
  const { data } = await api.get(`/api/chambres/${route.params.id}/`)
  chambre.value = data
})

function prendreRDV() {
  // redirection ou modal …
}
</script>
