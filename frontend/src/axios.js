import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000
})

instance.interceptors.request.use(config => {
  const token = localStorage.getItem('vuex') 
    ? JSON.parse(localStorage.getItem('vuex')).token 
    : null
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

export default instance