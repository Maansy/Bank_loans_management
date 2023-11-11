import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import vuetify from './plugins/vuetify'

axios.defaults.baseURL='http://localhost:8000'
// After creating the store

store.commit('initializeStore');

createApp(App)
  .use(store)
  .use(router)
  .use(vuetify)
  .mount('#app')
