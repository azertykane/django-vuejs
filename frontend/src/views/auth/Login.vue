<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card shadow p-4">
        <h2 class="text-center mb-4">Connexion</h2>
        <form @submit.prevent="login">
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-control" id="email" required>
          </div>
          <div class="mb-4">
            <label for="password" class="form-label">Mot de passe</label>
            <input v-model="form.password" type="password" class="form-control" id="password" required>
          </div>
          <button :disabled="loading" type="submit" class="btn btn-primary w-100">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Connexion…' : 'Se connecter' }}
          </button>
        </form>
        <div class="mt-3 text-center">
          <router-link to="/register">Pas encore de compte ? S'inscrire</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const store = useStore()
    return { router, store }
  },
  data() {
    return {
      loading: false,
      form: { email: '', password: '' }
    }
  },
  methods: {
    async login() {
      this.loading = true
      try {
        const { data } = await api.post('/auth/login/', this.form)
        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        this.store.commit('setToken', data.access)
        await this.store.dispatch('fetchUser')
        const route = data.role === 'proprietaire'
          ? '/proprietaire/dashboard'
          : '/locataire/dashboard'
        this.router.push(route)
      } catch {
        alert('Échec de la connexion — vérifiez vos identifiants')
      } finally {
        this.loading = false
      }
    }
  }
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
