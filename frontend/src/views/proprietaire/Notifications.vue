<template>
  <div class="container py-4">
    <h2 class="mb-4">Notifications propriétaire</h2>

    <!-- ===== Demandes de visite reçues ===== -->
    <section class="mb-5">
      <h4 class="mb-3">Demandes de visite reçues</h4>
      <ul class="list-group">
        <li
          v-for="rdv in rendezvous"
          :key="rdv.id"
          class="list-group-item d-flex justify-content-between align-items-start flex-wrap"
        >
          <div>
            <strong>Locataire :</strong>
            {{ rdv.locataire.nom || rdv.locataire.email }}<br />
            <strong>Chambre :</strong> {{ rdv.chambre.titre }}<br />
            <strong>Date :</strong> {{ formatDate(rdv.date_heure) }}<br />
            <span :class="badgeClass(rdv.statut)">{{ rdv.statut.toUpperCase() }}</span>
          </div>

          <div class="d-flex gap-2 flex-wrap">
            <button
              v-if="rdv.statut === 'en_attente'"
              class="btn btn-sm btn-outline-success"
              @click="confirmerRdv(rdv.id)"
            >
              Confirmer
            </button>

            <button
              v-if="rdv.statut === 'confirme' && !rdv.contratEnvoye"
              class="btn btn-sm btn-primary"
              @click="openContratForm(rdv)"
            >
              Envoyer un contrat
            </button>

            <span v-if="rdv.contratEnvoye" class="badge bg-info align-self-center">
              Contrat envoyé
            </span>
          </div>
        </li>
      </ul>
      <p v-if="!rendezvous.length" class="text-muted mt-3">Aucune demande de visite.</p>
    </section>

    <!-- ===== Contrats envoyés ===== -->
    <section>
      <h4 class="mb-3">Contrats envoyés</h4>
      <ul class="list-group">
        <li
          v-for="c in contrats"
          :key="c.id"
          class="list-group-item d-flex justify-content-between align-items-start flex-wrap"
        >
          <div>
            <strong>Locataire :</strong> {{ c.locataire.nom || c.locataire.email }}<br />
            <strong>Chambre :</strong> {{ c.chambre.titre }}<br />
            <strong>Loyer :</strong> {{ formatMoney(c.chambre.prix) }} / {{ c.periodicite }}<br />
            <span :class="badgeClassContrat(c.statut)">{{ c.statut.toUpperCase() }}</span>
          </div>
        </li>
      </ul>
      <p v-if="!contrats.length" class="text-muted mt-3">Aucun contrat envoyé.</p>
    </section>

    <!-- ===== MODAL Contrat ===== -->
    <div class="modal fade" id="contratModal" tabindex="-1">
      <div class="modal-dialog">
        <form class="modal-content" @submit.prevent="submitContrat">
          <div class="modal-header">
            <h5 class="modal-title">Créer un contrat</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" />
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label>Date de début</label>
              <input type="date" class="form-control" v-model="form.date_debut" required />
            </div>
            <div class="mb-2">
              <label>Date de fin</label>
              <input type="date" class="form-control" v-model="form.date_fin" />
            </div>
            <div class="mb-2">
              <label>Mois de caution</label>
              <input type="number" class="form-control" v-model.number="form.mois_caution" min="1" required />
            </div>
            <div class="mb-2">
              <label>Montant caution</label>
              <input type="number" class="form-control" v-model.number="form.montant_caution" required />
            </div>
            <div class="mb-2">
              <label>Mode de paiement</label>
              <select class="form-select" v-model="form.mode_paiement" required>
                <option value="mobile_money">Mobile Money</option>
                <option value="virement">Virement</option>
                <option value="cash">Cash</option>
              </select>
            </div>
            <div class="mb-2">
              <label>Periodicité</label>
              <select class="form-select" v-model="form.periodicite">
                <option value="journalier">Journalier</option>
                <option value="hebdomadaire">Hebdomadaire</option>
                <option value="mensuel">Mensuel</option>
              </select>
            </div>
            <div class="mb-2">
              <label>Description</label>
              <textarea class="form-control" rows="3" v-model="form.description" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="submit" class="btn btn-primary">Envoyer</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "@/services/api"
import { Modal } from "bootstrap"

const rendezvous = ref([])
const contrats = ref([])
const form = ref({
  date_debut: "",
  date_fin: "",
  mois_caution: 1,
  montant_caution: 0,
  mode_paiement: "mobile_money",
  periodicite: "mensuel",
  description: ""
})
const currentRdv = ref(null)
let modalInstance = null

onMounted(() => {
  fetchRendezvous()
  fetchContrats()
  modalInstance = new Modal(document.getElementById("contratModal"))
})

async function fetchRendezvous() {
  const { data } = await api.get("/api/rendezvous/")
  rendezvous.value = data
  markContratEnvoye()
}

async function fetchContrats() {
  const { data } = await api.get("/api/contrats/")
  contrats.value = data
  markContratEnvoye()
}

function markContratEnvoye() {
  rendezvous.value.forEach(rdv => {
    rdv.contratEnvoye = contrats.value.some(
      c => c.chambre.id === rdv.chambre.id && c.locataire.id === rdv.locataire.id
    )
  })
}

async function confirmerRdv(id) {
  await api.post(`/api/rendezvous/${id}/confirmer/`)
  await fetchRendezvous()
}

function openContratForm(rdv) {
  currentRdv.value = rdv
  form.value.montant_caution = rdv.chambre.prix * form.value.mois_caution
  modalInstance.show()
}

async function submitContrat() {
  try {
    await api.post(`/api/rendezvous/${currentRdv.value.id}/envoyer_contrat/`, form.value)
    modalInstance.hide()
    await fetchRendezvous()
    await fetchContrats()
    alert("Contrat envoyé avec succès.")
  } catch (err) {
    alert(err.response?.data?.detail || "Erreur lors de l'envoi du contrat")
  }
}

function formatDate(str) {
  return new Date(str).toLocaleString("fr-FR")
}

function formatMoney(n) {
  return parseInt(n, 10).toLocaleString("fr-FR", {
    style: "currency",
    currency: "XOF",
  })
}

function badgeClass(statut) {
  if (statut === "en_attente") return "badge bg-warning"
  if (statut === "confirme") return "badge bg-success"
  if (statut === "refuse") return "badge bg-danger"
  return "badge bg-secondary"
}

function badgeClassContrat(statut) {
  if (statut === "propose") return "badge bg-info"
  if (statut === "accepte") return "badge bg-success"
  if (statut === "refuse") return "badge bg-danger"
  return "badge bg-secondary"
}
</script>
