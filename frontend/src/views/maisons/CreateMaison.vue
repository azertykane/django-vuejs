<template>
  <div class="container py-4">
    <h2 class="mb-3">{{ isEdit ? 'Modifier la Maison' : 'Ajouter une Maison' }}</h2>

    <b-form @submit.prevent="save" enctype="multipart/form-data">
      <!-- Adresse, latitude, longitude -->
      <b-row>
        <b-col md="6">
          <b-form-group label="Adresse">
            <b-form-input v-model="form.adresse" required />
          </b-form-group>
        </b-col>

        <b-col md="3">
          <b-form-group label="Latitude">
            <b-form-input type="number" v-model="form.latitude" step="0.000001" />
          </b-form-group>
        </b-col>

        <b-col md="3">
          <b-form-group label="Longitude">
            <b-form-input type="number" v-model="form.longitude" step="0.000001" />
          </b-form-group>
        </b-col>
      </b-row>

      <b-form-group label="Description">
        <b-form-textarea v-model="form.description" rows="3" />
      </b-form-group>

      <!-- Images -->
      <b-form-group label="Images (3 max)">
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          multiple
          class="form-control"
          :disabled="files.length >= 3"
          @change="onFileChange"
        />
        <div class="d-flex gap-2 mt-3 flex-wrap">
          <div
            v-for="(url, i) in previews"
            :key="i"
            class="preview-box"
          >
            <img :src="url" alt="preview" />
          </div>
        </div>
      </b-form-group>

      <b-button variant="primary" type="submit">
        {{ isEdit ? 'Enregistrer' : 'Ajouter' }}
      </b-button>
      <router-link class="btn btn-link" to="/proprietaire/biens">Retour</router-link>
    </b-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const store = useStore()

const isEdit = ref(false)
const files = ref([])
const previews = ref([])

const form = ref({
  adresse: '',
  latitude: '',
  longitude: '',
  description: ''
})

onMounted(async () => {
  const id = route.query.id
  if (!id) return
  isEdit.value = true
  try {
    const { data } = await api.get(`/api/maisons/${id}/`)
    Object.assign(form.value, data)
    previews.value = data.medias.map(m => m.fichier)
  } catch {
    alert('Impossible de charger la maison.')
  }
})

function onFileChange (e) {
  files.value = Array.from(e.target.files).slice(0, 3)
  previews.value = files.value.map(f => URL.createObjectURL(f))
}

async function save () {
  const fd = new FormData()
  Object.entries(form.value).forEach(([k, v]) => fd.append(k, v))
  fd.append('proprietaire', store.state.user.id)

  files.value.forEach(f => fd.append('images', f))

  try {
    if (isEdit.value) {
      await api.put(`/api/maisons/${route.query.id}/`, fd)
    } else {
      await api.post('/api/maisons/', fd)
    }
    alert('Sauvegarde réussie.')
    router.push('/proprietaire/biens')
  } catch {
    alert('Erreur lors de la sauvegarde.')
  }
}
</script>

<style scoped>
.container {
  max-width: 700px;
}

.preview-box {
  width: 100px;
  height: 100px;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.15);
}

.preview-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
