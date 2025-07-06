<template>
  <div class="container py-4">
    <h2 class="mb-3">{{ isEdit ? 'Modifier la Chambre' : 'Ajouter une Chambre' }}</h2>

    <b-form @submit.prevent="save" enctype="multipart/form-data">
      <b-form-group label="Maison">
        <b-form-select
          v-model="form.maison_id"
          :options="maisonOpts"
          required
        />
      </b-form-group>

      <b-form-group label="Titre">
        <b-form-input v-model="form.titre" required />
      </b-form-group>

      <b-row>
        <b-col md="4">
          <b-form-group label="Type">
            <b-form-select
              v-model="form.type"
              :options="['simple', 'appartement', 'maison']"
            />
          </b-form-group>
        </b-col>

        <b-col md="4">
          <b-form-group label="Taille (m²)">
            <b-form-input v-model="form.taille" />
          </b-form-group>
        </b-col>

        <b-col md="4">
          <b-form-group label="Prix">
            <b-form-input type="number" v-model="form.prix" />
          </b-form-group>
        </b-col>
      </b-row>

      <b-row>
        <b-col md="4">
          <b-form-checkbox v-model="form.meublee">Meublée</b-form-checkbox>
        </b-col>
        <b-col md="4">
          <b-form-checkbox v-model="form.salle_de_bain">Salle de bain privative</b-form-checkbox>
        </b-col>
        <b-col md="4">
          <b-form-checkbox v-model="form.disponible">Disponible</b-form-checkbox>
        </b-col>
      </b-row>

      <b-form-group label="Description">
        <b-form-textarea v-model="form.description" rows="3" />
      </b-form-group>

      <!-- Images (3 max) -->
      <b-form-group label="Images (3 max)">
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          multiple
          :disabled="files.length >= 3"
          class="form-control"
          @change="onFileChange"
        />
        <div class="d-flex gap-2 mt-3 flex-wrap">
          <div
            v-for="(url, i) in previews"
            :key="i"
            class="preview-box"
          >
            <img :src="url" alt="pré‑image" />
          </div>
        </div>
      </b-form-group>

      <b-button variant="primary" type="submit">
        {{ isEdit ? 'Enregistrer' : 'Ajouter' }}
      </b-button>
      <router-link class="btn btn-link" to="/proprietaire/chambres">Retour</router-link>
    </b-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

/* -------- états -------- */
const route      = useRoute()
const router     = useRouter()
const isEdit     = ref(false)

const files      = ref([])
const previews   = ref([])
const maisonOpts = ref([])

const form = ref({
  maison_id: '',
  titre: '',
  description: '',
  taille: '',
  type: 'simple',
  meublee: false,
  salle_de_bain: false,
  prix: '',
  disponible: true
})

/* -------- charger maisons du propriétaire -------- */
async function fetchMaisons () {
  const { data } = await api.get('/api/maisons/')
  maisonOpts.value = data.map(m => ({ value: m.id, text: m.adresse }))
}

/* -------- charger chambre si édition -------- */
onMounted(async () => {
  await fetchMaisons()
  const id = route.query.id
  if (!id) return
  isEdit.value = true
  try {
    const { data } = await api.get(`/api/chambres/${id}/`)
    Object.assign(form.value, data)
    previews.value = data.medias.map(m => m.fichier)
  } catch {
    alert('Impossible de charger la chambre.')
  }
})

/* -------- fichiers -------- */
function onFileChange (e) {
  files.value   = Array.from(e.target.files).slice(0, 3)
  previews.value = files.value.map(f => URL.createObjectURL(f))
}

/* -------- save -------- */
async function save () {
  const fd = new FormData()
  Object.entries(form.value).forEach(([k, v]) => fd.append(k, v))
  files.value.forEach(f => fd.append('images', f))

  try {
    if (isEdit.value) {
      await api.put(`/api/chambres/${route.query.id}/`, fd)
    } else {
      await api.post('/api/chambres/', fd)
    }
    alert('Sauvegarde réussie.')
    router.push('/proprietaire/chambres')
  } catch {
    alert('Erreur lors de la sauvegarde.')
  }
}
</script>

<style scoped>
.container { max-width: 700px; }
.preview-box {
  width: 100px;
  height: 100px;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 0 6px rgba(0,0,0,.15);
}
.preview-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
