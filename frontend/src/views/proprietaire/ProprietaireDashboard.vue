<template>
  <div class="dashboard">
    <aside class="sidebar bg-primary text-white p-4">
  <h4 class="mb-4 text-center">🏠 Propriétaire</h4>
  <ul class="nav flex-column gap-2">
    <li class="nav-item">
      <router-link to="/proprietaire/dashboard" class="nav-link text-white">
        <i class="fas fa-home me-2"></i> Tableau de bord
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/proprietaire/biens" class="nav-link text-white">
        <i class="fas fa-building me-2"></i> Mes Biens
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/proprietaire/chambres" class="nav-link text-white">
        <i class="fas fa-bed me-2"></i> Mes Chambres
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/proprietaire/locataires" class="nav-link text-white">
        <i class="fas fa-users me-2"></i> Mes Locataires
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/proprietaire/contrats" class="nav-link text-white">
        <i class="fas fa-file-contract me-2"></i> Contrats
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/proprietaire/paiements" class="nav-link text-white">
        <i class="fas fa-credit-card me-2"></i> Paiements
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/proprietaire/reglages-paiement" class="nav-link text-white">
        <i class="fas fa-cogs me-2"></i> Réglages de paiement
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/proprietaire/notifications" class="nav-link text-white">
        <i class="fas fa-bell me-2"></i> Notifications
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/proprietaire/problemes" class="nav-link text-white">
        <i class="fas fa-tools me-2"></i> Problèmes signalés
      </router-link>
    </li>

    <li class="nav-item mt-4">
      <button @click="logout" class="btn btn-outline-light w-100">
        <i class="fas fa-sign-out-alt me-2"></i> Déconnexion
      </button>
    </li>
  </ul>
</aside>


    <main class="content">
      <h1>Bienvenue, {{ displayName }}</h1>
      <p>Voici un aperçu de votre activité récente.</p>

      <section class="cards">
        <div class="card">
          <i class="fas fa-home fa-2x text-primary mb-2"></i>
          <h3>3 Biens Loués</h3>
        </div>
        <div class="card">
          <i class="fas fa-users fa-2x text-success mb-2"></i>
          <h3>5 Locataires</h3>
        </div>
        <div class="card">
          <i class="fas fa-euro-sign fa-2x text-warning mb-2"></i>
          <h3>200 000 FCFA / mois</h3>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { useStore, mapState } from 'vuex'

export default {
  name: 'ProprietaireDashboard',
  computed: {
    ...mapState(['user']),
    displayName () {
      return this.user?.nom || this.user?.email || 'Utilisateur'
    }
  },
  setup () {
    const router = useRouter()
    const store = useStore()

    const logout = async () => {
      await store.dispatch('logout')
      router.push('/')
    }

    return { logout }
  }
}
</script>


<style scoped>
.dashboard {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 350px;
  background-color: #343a40;
  color: white;
  padding: 20px;
}
.sidebar h2 {
  font-size: 20px;
  margin-bottom: 20px;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  margin-bottom: 10px;
}
.sidebar a,
.sidebar button {
  color: white;
  text-decoration: none;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}
.content {
  flex: 1;
  padding: 40px;
}
.cards {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}
.card {
  flex: 1;
  background: #f8f9fa;
  border-radius: 10px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}
</style>
