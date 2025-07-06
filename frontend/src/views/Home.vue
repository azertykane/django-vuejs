<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-overlay"></div>
      <div class="hero-content text-center text-white">
        <h1 class="display-4 fw-bold mb-4">Trouvez Votre Logement Idéal</h1>
        <p class="lead mb-5">Découvrez des centaines de chambres et appartements à louer dans toute la ville</p>
        <div class="d-grid gap-3 d-sm-flex justify-content-sm-center">
          <router-link
            to="/login"
            class="btn btn-primary btn-lg px-4 gap-3"
          >
            Se Connecter
          </router-link>
          <router-link
            to="/register"
            class="btn btn-outline-light btn-lg px-4"
          >
            Créer un Compte
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="container py-5">
      <h2 class="text-center mb-5">Pourquoi choisir Location Sociale ?</h2>
      <div class="row g-4">
        <div class="col-md-4">
          <div class="feature-card p-4 text-center">
            <div class="feature-icon mb-3">
              <i class="fas fa-home fa-3x text-primary"></i>
            </div>
            <h3>Large Choix</h3>
            <p>Des centaines de propriétés disponibles dans toute la ville</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="feature-card p-4 text-center">
            <div class="feature-icon mb-3">
              <i class="fas fa-euro-sign fa-3x text-primary"></i>
            </div>
            <h3>Prix Justes</h3>
            <p>Des loyers adaptés à tous les budgets</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="feature-card p-4 text-center">
            <div class="feature-icon mb-3">
              <i class="fas fa-shield-alt fa-3x text-primary"></i>
            </div>
            <h3>Sécurité</h3>
            <p>Transactions sécurisées et contrats vérifiés</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Property Showcase -->
    <section class="bg-light py-5">
      <div class="container">
        <h2 class="text-center mb-5">Nos Dernières Offres</h2>
        <div class="row g-4">
          <div 
            class="col-md-4" 
            v-for="(property, index) in featuredProperties" 
            :key="index"
          >
            <div class="property-card card h-100">
              <img 
                :src="property.image" 
                class="card-img-top property-image" 
                alt="Property image"
              >
              <div class="card-body">
                <h5 class="card-title">{{ property.title }}</h5>
                <p class="card-text">{{ property.description }}</p>
                <div class="d-flex justify-content-between align-items-center">
                  <span class="badge bg-primary">{{ property.price }}€/mois</span>
                  <button 
                    class="btn btn-sm btn-outline-primary"
                    @click="viewProperty(property.id)"
                  >
                    Voir plus
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="cta-section py-5 text-center text-white">
      <div class="container">
        <h2 class="mb-4">Prêt à trouver votre nouveau logement ?</h2>
        <router-link
          to="/register"
          class="btn btn-light btn-lg px-5"
        >
          Commencez Maintenant
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      featuredProperties: [
        {
          id: 1,
          title: 'Studio Moderne',
          description: 'Studio meublé de 25m² proche du centre-ville',
          price: 450,
          image: 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        },
        {
          id: 2,
          title: 'Appartement Lumineux',
          description: '2 pièces de 45m² avec balcon',
          price: 650,
          image: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        },
        {
          id: 3,
          title: 'Chambre Étudiante',
          description: 'Chambre dans colocation proche université',
          price: 350,
          image: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        }
      ]
    }
  },
  methods: {
    viewProperty(id) {
      this.$router.push(`/property/${id}`)
    }
  }
}
</script>

<style scoped>
.home-page {
  overflow-x: hidden;
}

.hero-section {
  position: relative;
  height: 80vh;
  background: url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80') no-repeat center center;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  padding: 0 20px;
}

.property-card {
  transition: transform 0.3s ease;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.property-card:hover {
  transform: translateY(-5px);
}

.property-image {
  height: 200px;
  object-fit: cover;
}

.feature-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 80px 0;
}

.btn-primary {
  background-color: #667eea;
  border-color: #667eea;
}

.btn-primary:hover {
  background-color: #5a6fd1;
  border-color: #5a6fd1;
}

.btn-outline-light:hover {
  color: #667eea;
}
</style>
