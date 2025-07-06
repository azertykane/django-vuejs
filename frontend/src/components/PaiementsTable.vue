<template>
  <div>
    <b-table
      :items="data"
      :fields="fields"
      :busy="!loaded"
      striped
      hover
      bordered
      responsive
    >
      <template #cell(statut)="d">
        <span :class="['badge', d.value === 'payé' ? 'bg-success' : 'bg-danger']">
          {{ d.value }}
        </span>
      </template>
    </b-table>

    <div v-if="loaded && !data.length" class="text-center text-muted py-4">
      Aucun paiement trouvé.
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaiementsTable',
  props: {
    data:   { type: Array,   required: true },
    loaded: { type: Boolean, required: true },
  },
  data() {
    return {
      fields: [
        { key: 'id',        label: '#' },
        { key: 'locataire', label: 'Locataire' },
        { key: 'mois',      label: 'Période' },
        { key: 'montant',   label: 'Montant (FCFA)' },
        { key: 'statut',    label: 'Statut' },
      ],
    }
  },
}
</script>

