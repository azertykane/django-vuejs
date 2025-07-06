<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" variant="primary">
      <b-container>
        <b-navbar-brand to="/">Location Sociale</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item to="/dashboard" v-if="isAuthenticated">
              <font-awesome-icon icon="home" class="mr-1" /> Tableau de bord
            </b-nav-item>
          </b-navbar-nav>

          <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown right v-if="isAuthenticated">
              <template #button-content>
                <font-awesome-icon icon="user" class="mr-1" />
                {{ currentUser?.nom || currentUser?.email || 'Profil' }}
              </template>
              <b-dropdown-item @click="logout">Déconnexion</b-dropdown-item>
            </b-nav-item-dropdown>

            <template v-else>
              <b-nav-item to="/login">
                <font-awesome-icon icon="sign-in-alt" class="mr-1" /> Connexion
              </b-nav-item>
              <b-nav-item to="/register">
                <font-awesome-icon icon="user-plus" class="mr-1" /> Inscription
              </b-nav-item>
            </template>
          </b-navbar-nav>
        </b-collapse>
      </b-container>
    </b-navbar>

    <b-container class="mt-4">
      <router-view v-if="$route.matched.length"></router-view>
      <div v-else class="text-center py-5">
        <b-spinner variant="primary"></b-spinner>
        <p>Chargement...</p>
      </div>
    </b-container>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'App',
  computed: {
    ...mapGetters(['isAuthenticated', 'currentUser'])
  },
  methods: {
    ...mapActions(['logout'])
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  background-color: #f8faf8;
}
</style>
