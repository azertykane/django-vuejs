import { createApp } from 'vue'
import App            from './App.vue'
import router         from './router'
import store          from './store'

/* Axios ---------------------------------------------------- */
import axios from 'axios'
axios.defaults.baseURL = 'http://127.0.0.1:8000/'
axios.interceptors.request.use(cfg => {
  const t = localStorage.getItem('access_token')
  if (t) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})

/* Styles --------------------------------------------------- */
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import '@fortawesome/fontawesome-free/css/all.min.css'

/* Bootstrap-Vue 3 plugin ---------------------------------- */
import BootstrapVue3 from 'bootstrap-vue-3'

const app = createApp(App)

app.use(BootstrapVue3)      // 🟢 OBLIGATOIRE pour <b-*> et useToast()
app.use(router)
app.use(store)

app.mount('#app')
