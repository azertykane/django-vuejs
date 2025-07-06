<template>
  <div class="container py-4">
    <!-- En‑tête -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Mes Maisons</h2>

      <div>
        <router-link
          class="btn btn-success me-2"
          :to="{ name: 'CreateMaison' }"
        >
          <i class="fas fa-plus" /> Ajouter
        </router-link>

        <b-button variant="outline-primary" @click="getMaisons">
          <i class="fas fa-sync-alt" />
        </b-button>
      </div>
    </div>

    <!-- Tableau -->
    <b-table
      v-if="loaded"
      :items="maisons"
      :fields="fields"
      striped hover bordered responsive
    >
      <!-- Photo -->
      <template #cell(photo)="d">
        <img
          v-if="d.value"
          :src="d.value"
          class="thumb"
          alt="thumb"
        />
        <small v-else class="text-muted">—</small>
      </template>

      <!-- Description courte -->
      <template #cell(description)="d">
        {{ d.value?.slice(0, 60) }}…
      </template>

      <!-- Actions -->
      <template #cell(actions)="row">
        <b-button
          size="sm" variant="outline-secondary" class="me-1"
          @click="editMaison(row.item)"
        >
          <i class="fas fa-pen" />
        </b-button>

        <b-button
          size="sm" variant="outline-danger"
          @click="deleteMaison(row.item.id)"
        >
          <i class="fas fa-trash" />
        </b-button>
      </template>
    </b-table>

    <!-- Spinner -->
    <div v-else class="text-center py-5">
      <b-spinner variant="primary" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const maisons = ref([])
const loaded  = ref(false)
const router  = useRouter()

const fields = [
  { key: 'photo', label: '', thStyle: { width: '80px' } },
  { key: 'adresse', label: 'Adresse' },
  { key: 'description', label: 'Description' },
  { key: 'cree_le', label: 'Créé le' },
  { key: 'actions', label: 'Actions', thStyle: { width: '110px' } },
]

async function getMaisons () {
  loaded.value = false
  try {
    const { data } = await api.get('/api/maisons/?mes=true')
    // pour chaque maison on prend la première photo (facultatif)
    maisons.value = data.map(m => ({
      ...m,
      photo: m.medias?.[0]?.fichier || null,
    }))
  } catch {
    alert('Erreur lors du chargement des maisons.')
  } finally { loaded.value = true }
}

function editMaison (m) {
  router.push({ name: 'CreateMaison', query: { id: m.id } })
}

async function deleteMaison (id) {
  if (!confirm('Supprimer cette maison ?')) return
  try {
    await api.delete(`/api/maisons/${id}/`)
    await getMaisons()
  } catch {
    alert('Suppression impossible.')
  }
}

onMounted(getMaisons)
</script>

<style scoped>
.container { max-width: 1000px; }
.thumb {
  width: 60px; height: 60px; object-fit: cover;
  border-radius: 6px; box-shadow: 0 0 4px rgba(0,0,0,.2);
}
</style>
