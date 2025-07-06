<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3 class="mb-0">Mes Chambres</h3>
      <div>
        <b-button size="sm" variant="outline-primary" @click="fetchChambres">
          <i class="fas fa-sync-alt" /> Rafraîchir
        </b-button>
        <router-link
          class="btn btn-sm btn-success ms-2"
          to="/proprietaire/chambres/ajouter"
        >
          <i class="fas fa-plus" /> Ajouter une chambre
        </router-link>
      </div>
    </div>

    <b-table
      v-if="loaded"
      :items="chambres"
      :fields="fields"
      hover
      striped
      small
      class="shadow-sm"
    >
      <template #cell(type)="d">
        {{ d.value.charAt(0).toUpperCase() + d.value.slice(1) }}
      </template>

      <template #cell(actions)="row">
        <router-link
          :to="{
            path: '/proprietaire/chambres/ajouter',
            query: { id: row.item.id }
          }"
          class="btn btn-sm btn-outline-secondary me-1"
        >
          <i class="fas fa-edit" />
        </router-link>
        <button
          class="btn btn-sm btn-outline-danger"
          @click="supprimer(row.item.id)"
        >
          <i class="fas fa-trash" />
        </button>
      </template>
    </b-table>

    <div v-else class="text-center py-5">
      <b-spinner />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const chambres = ref([])
const loaded   = ref(false)

const fields = [
  { key: 'id',      label: '#' },
  { key: 'titre',   label: 'Titre' },
  { key: 'type',    label: 'Type' },
  { key: 'prix',    label: 'Prix' },
  { key: 'disponible', label: 'Dispo' },
  { key: 'actions', label: '', thStyle: { width: '90px' } }
]

async function fetchChambres () {
  loaded.value = false
  try {
    const { data } = await api.get('/api/chambres/')
    chambres.value = data
  } finally {
    loaded.value = true
  }
}

async function supprimer (id) {
  if (!confirm('Supprimer cette chambre ?')) return
  try {
    await api.delete(`/api/chambres/${id}/`)
    chambres.value = chambres.value.filter(c => c.id !== id)
  } catch {
    alert('Erreur suppression.')
  }
}

onMounted(fetchChambres)
</script>
