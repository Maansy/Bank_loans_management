<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card>
          <v-card-title class="headline">Log in</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="submitForm">
              <v-text-field label="Username" v-model="username" required></v-text-field>
              <v-text-field label="Password" type="password" v-model="password" required></v-text-field>
              <v-alert type="error" v-if="errors.length" v-for="error in errors" :key="error">{{ error }}</v-alert>
              <v-btn color="success" type="submit" block>Submit</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { toast } from 'bulma-toast'
import axios from 'axios';


export default {
  name: 'LogIn',
  data() {
    return {
      username: '',
      password: '',
      errors: [],
    };
  },
  methods: {
    async submitForm() {

      this.errors = [];
      try {
        const response = await axios.post('/login/', {
          username: this.username,
          password: this.password
        })

        this.$store.commit('setToken', response.data.token);
        this.$store.commit('setRole', response.data.role);
        this.$store.commit('setUser', response.data.user);
        this.$store.commit('setIsVerified', response.data.is_verified);
        
        axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`;
        toast({
            message: 'Logged in successfully',
            type: 'is-success',
            position: 'bottom-right',
            dismissible: true,
            pauseOnHover: true,
            duration: 3000,
          })

        this.$router.push({ name: 'MyAccount' });
      } catch (error) {
        if (error.response && error.response.data) {
          // Handle errors from the server
          for (const key in error.response.data) {
            this.errors.push(`${key}: ${error.response.data[key]}`);
          }
        } else {
          // Handle other errors
          this.errors.push('An error occurred. Please try again later.');
        }
      }
    }
  },
};
</script>
