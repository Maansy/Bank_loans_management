<template>
  <v-app>
    <v-main>
      <Navbar /> 
      <router-view></router-view> <!-- Place where your routed components will be rendered -->
    </v-main>
  </v-app>
</template>

<script>
import Navbar from '@/components/layout/Navbar.vue'
import axios from 'axios';
export default {
  name: 'App',
  components: {
    Navbar
  },
  created() {
  this.$store.dispatch('initializeAuthentication');
}
}
</script>


<style lang="scss">
@import '../node_modules/bulma';
</style>
