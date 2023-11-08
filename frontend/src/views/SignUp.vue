<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card>
            <v-card-title class="headline">Sign Up</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="submitForm">
                <v-text-field label="Email" v-model="username" />
                <v-text-field type="password" label="Password" v-model="password1" />
                <v-text-field type="password" label="Repeat Password" v-model="password2" />
  
                <v-alert type="error" v-if="errors.length" >
                  <ul>
                    <li v-for="error in errors" :key="error">{{ error }}</li>
                  </ul>
                </v-alert>

                <v-btn color="success" type="submit">Submit</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  


<script>
import axios from 'axios';
import { toast } from 'bulma-toast';
export default {
    name: 'SignUp',
    data() {
        return {
            username: '',
            password1: '',
            password2: '',
            errors: []
        }
    },
    methods: {
        async submitForm() {
            
            this.errors = [];
            if (this.username === '') {
                this.errors.push('Username required.');
            }
            if (this.password1 === '') {
                this.errors.push('Password required.');
            }
            if (this.password1 !== this.password2) {
                this.errors.push('Passwords do not match.');
            }
            if (!this.errors.length) {
                this.$store.commit('setIsLoading', true)

                const formData = {
                    username: this.username,
                    password: this.password1
                }
                console.log(formData)
                await axios
                    .post('/api/v1/users/', formData)
                    .then(response => {
                        toast({
                            message: 'User created successfully',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'bottom-right',
                        });
                        this.$router.push('/login');
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
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
        }
    }
}

</script>