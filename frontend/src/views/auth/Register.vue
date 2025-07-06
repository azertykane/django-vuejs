<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card shadow p-4">
        <h2 class="text-center mb-4">Inscription</h2>

        <form @submit.prevent="register">
          <!-- Email -->
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input
              v-model="form.email"
              type="email"
              class="form-control"
              id="email"
              required
            />
          </div>

          <!-- Mot de passe -->
          <div class="mb-3">
            <label for="password" class="form-label">Mot de passe</label>
            <input
              v-model="form.password"
              type="password"
              class="form-control"
              id="password"
              required
              minlength="8"
            />
          </div>

          <!-- Confirmation -->
          <div class="mb-3">
            <label for="password2" class="form-label">Confirmer le mot de passe</label>
            <input
              v-model="form.password2"
              type="password"
              class="form-control"
              id="password2"
              required
            />
          </div>

          <!-- Téléphone -->
          <div class="mb-3">
            <label for="telephone" class="form-label">Téléphone</label>
            <input
              v-model="form.telephone"
              type="text"
              class="form-control"
              id="telephone"
            />
          </div>

          <!-- CNI -->
          <div class="mb-3">
            <label for="cni" class="form-label">CNI</label>
            <input
              v-model="form.cni"
              type="text"
              class="form-control"
              id="cni"
            />
          </div>

          <!-- Rôle -->
          <div class="mb-4">
            <label for="role" class="form-label">Rôle</label>
            <select v-model="form.role" id="role" class="form-select" required>
              <option value="locataire">Locataire</option>
              <option value="proprietaire">Propriétaire</option>
            </select>
          </div>

          <!-- Bouton -->
          <button :disabled="loading" type="submit" class="btn btn-primary w-100">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Inscription…' : "S'inscrire" }}
          </button>
        </form>

        <div class="mt-3 text-center">
          <router-link to="/login">Déjà un compte ? Se connecter</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api        from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      loading: false,
      form: {
        email: '',
        password: '',
        password2: '',
        telephone: '',
        cni: '',
        role: 'locataire',
      },
    }
  },
  methods: {
    async register() {
      /* validation simple */
      if (this.form.password !== this.form.password2) {
        alert('Les mots de passe ne correspondent pas')
        return
      }
      if (this.form.password.length < 8) {
        alert('Mot de passe trop court (≥ 8 caractères)')
        return
      }

      this.loading = true
      try {
        await api.post('/auth/register/', { ...this.form })
        alert('Inscription réussie ! Vous pouvez vous connecter.')
        this.router.push('/login')
      } catch (e) {
        const msg = e.response?.data
          ? Object.values(e.response.data).join(' ')
          : "Erreur lors de l'inscription"
        alert(msg)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2f5;
  padding: 20px;
}

.auth-container {
  max-width: 400px;
  width: 100%;
}

.auth-card {
  background: #fff;
  border-radius: 8px;
}
</style>
