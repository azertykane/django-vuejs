import { createStore } from 'vuex'
import api from '@/services/api'

export default createStore({
  state: () => ({
    token: localStorage.getItem('access_token'),
    user:  JSON.parse(localStorage.getItem('user') || 'null'),
  }),
  getters: {
    isAuthenticated: s => !!s.token,
    userRole:        s => s.user?.role,
    currentUser:     s => s.user,
  },
  mutations: {
    setToken(s, t) { s.token = t },
    setUser(s, u)  { s.user  = u },
  },
  actions: {
    async fetchUser({ commit }) {
      const { data } = await api.get('/auth/me/')
      localStorage.setItem('user', JSON.stringify(data))
      commit('setUser', data)
    },
    logout({ commit }) {
      localStorage.clear()
      commit('setToken', null)
      commit('setUser', null)
    },
  },
})
