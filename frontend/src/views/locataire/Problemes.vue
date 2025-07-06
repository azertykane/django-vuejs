<template>
  <div class="container py-4">
    <h2 class="mb-4">Signaler un problème</h2>

    <!-- ── Formulaire ─────────────────────────────────── -->
    <form @submit.prevent="signalerProbleme" class="mb-5">
      <!-- contrat -->
      <div class="mb-3">
        <label class="form-label">Contrat</label>
        <select v-model="form.contrat" class="form-select" required>
          <option value="" disabled>— Choisir —</option>
          <option v-for="c in contrats" :key="c.id" :value="c.id">
            Chambre : {{ c.chambre.titre }}
          </option>
        </select>
      </div>

      <!-- type -->
      <div class="mb-3">
        <label class="form-label">Type</label>
        <select v-model="form.type" class="form-select" required>
          <option value="plomberie">Plomberie</option>
          <option value="electricite">Électricité</option>
          <option value="autre">Autre</option>
        </select>
      </div>

      <!-- responsable -->
      <div class="mb-3">
        <label class="form-label">Responsable</label>
        <select v-model="form.responsable" class="form-select" required>
          <option value="locataire">Moi (Locataire)</option>
          <option value="proprietaire">Propriétaire</option>
        </select>
      </div>

      <!-- description -->
      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea
          v-model="form.description"
          class="form-control"
          rows="4"
          required
        ></textarea>
      </div>

      <!-- feedback -->
      <div
        v-if="msg.text"
        :class="['alert', msg.ok ? 'alert-success' : 'alert-danger']"
      >
        {{ msg.text }}
      </div>

      <button class="btn btn-primary" type="submit" :disabled="sending">
        <span v-if="sending" class="spinner-border spinner-border-sm me-1"></span>
        Envoyer
      </button>
    </form>

    <!-- ── Liste des problèmes ─────────────────────────── -->
    <h4 class="mb-3">Mes problèmes signalés</h4>
    <ul class="list-group">
      <li v-for="p in problemes" :key="p.id" class="list-group-item">
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

    <p v-if="!problemes.length" class="text-muted mt-3">
      Aucun problème signalé.
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

/* ─── état ─────────────────────────────────────────────── */
const contrats = ref([])
const problemes = ref([])

const form = ref({
  contrat: '',
  type: 'plomberie',
  responsable: 'locataire',
  description: ''
})

const sending = ref(false)
const msg = ref({ ok: true, text: '' })

/* ─── chargement initial ───────────────────────────────── */
onMounted(loadData)

async function loadData () {
  const { data: c } = await api.get('/api/contrats/')
  const { data: p } = await api.get('/api/problemes/')
  contrats.value = c
  problemes.value = p
}

/* ─── envoi du formulaire ──────────────────────────────── */
async function signalerProbleme () {
  sending.value = true
  msg.value = { ok: true, text: '' }

  try {
    await api.post('/api/problemes/', form.value)

    msg.value = { ok: true, text: 'Problème signalé avec succès.' }

    // refresh list
    const { data } = await api.get('/api/problemes/')
    problemes.value = data

    // reset
    form.value = {
      contrat: '',
      type: 'plomberie',
      responsable: 'locataire',
      description: ''
    }
  } catch (err) {
    msg.value = {
      ok: false,
      text: err.response?.data?.detail || 'Erreur lors de l’envoi.'
    }
  } finally {
    sending.value = false
  }
}
</script>
