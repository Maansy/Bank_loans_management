import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import vuetify from './plugins/vuetify'
import Cookies from 'js-cookie';

axios.defaults.baseURL='http://localhost:8000'
// After creating the store

axios.interceptors.request.use(function (config) {
  const token = Cookies.get('token');
  config.headers.Authorization =  token ? `Token ${token}` : '';
  return config;
});


store.commit('initializeStore');

createApp(App)
  .use(store)
  .use(router)
  .use(vuetify)
  .mount('#app')
