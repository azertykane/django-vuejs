<template>
  <b-container class="mt-5">
    <b-row class="justify-content-md-center">
      <b-col cols="12" md="6">
        <b-card header="Connexion">
          <b-form @submit.prevent="login">
            <b-form-group label="Nom d'utilisateur">
              <b-form-input v-model="credentials.username" required></b-form-input>
            </b-form-group>

            <b-form-group label="Mot de passe">
              <b-form-input v-model="credentials.password" type="password" required></b-form-input>
            </b-form-group>

            <b-button type="submit" variant="primary" block>Se connecter</b-button>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'LoginView',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    ...mapActions(['login']),
    async login() {
      const success = await this.$store.dispatch('login', this.credentials)
      if (success) {
        this.$router.push(this.$route.query.redirect || '/dashboard')
      }
    }
  }
}
</script>