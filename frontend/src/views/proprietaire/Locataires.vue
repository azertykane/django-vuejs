<template>
  <div>
    <h3 class="mb-4">Mes Locataires</h3>
    <b-table
      v-if="loaded"
      :items="locataires"
      :fields="fields"
      striped hover small
    />
    <div v-else class="text-center py-5"><b-spinner /></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const locataires = ref([])
const loaded     = ref(false)
const fields     = [
  { key: 'id', label: '#' },
  { key: 'nom', label: 'Nom' },
  { key: 'email', label: 'Email' },
  { key: 'telephone', label: 'Téléphone' },
  { key: 'cni', label: 'CNI' },
]

async function fetchLocataires () {
  loaded.value = false
  try {
    const { data } = await api.get('/api/locataires/?mes=true')
    locataires.value = data
  } finally { loaded.value = true }
}

onMounted(fetchLocataires)
</script>
