<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card>
            <v-card-title class="headline">Log in</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="submitForm">
                <v-text-field
                  label="Email"
                  type="email"
                  v-model="username"
                  required
                ></v-text-field>
  
                <v-text-field
                  label="Password"
                  type="password"
                  v-model="password"
                  required
                ></v-text-field>
  
                <v-alert
                  type="error"
                  v-if="errors.length"
                  v-for="error in errors"
                  :key="error"
                >
                  {{ error }}
                </v-alert>
  
                <v-btn color="success" type="submit" block>Submit</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
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
        async submitForm(){
            // this.$store.commit('setIsLoading', true)

            axios.defaults.headers.common['Authorization'] = ''
            localStorage.removeItem('token')
            const formData = {
                username: this.username,
                password: this.password
            }

            await axios
                .post('/api/v1/token/login/',formData)
                .then(response => {
                    // const token = response.data.auth_token
                    // this.$store.commit('setToken', token)
                    // axios.defaults.headers.common['Authorization'] = 'Token ' + token
                    // localStorage.setItem('token', token)
                    this.$router.push('/')
                })
                .catch(error => {
                        if (error.response) {
                            for(const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`);
                            }
                        } else if (error.request) {
                            this.errors.push(error.request);
                        } else {
                            this.errors.push(error.message);
                        }

                    });
            this.$store.commit('setIsLoading', false)
        }
    },
  };
  </script>
  