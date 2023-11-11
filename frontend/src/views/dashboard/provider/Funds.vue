<template>
    <v-row>
      <v-col cols="12" sm="4" v-for="fund in funds" :key="fund.id">
        <v-card>
          <v-card-title>{{ fund.name }}</v-card-title>
          <v-card-subtitle>{{ fund.min_fund_amount }} - {{ fund.max_fund_amount }}</v-card-subtitle>        
          <v-card-text>
            <p>Interest Rate: {{ fund.interest_rate }}%</p>
            <p>Duration: {{ fund.duration }} years</p>
          </v-card-text>
          <template v-if="$store.state.role === 'provider'">
            <v-card-actions>
                <v-btn color="primary">Subscribe</v-btn>
            </v-card-actions>
        </template>
        </v-card>
      </v-col>
    </v-row>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Funds',
    data() {
      return {
        funds: [],
      };
    },
    mounted() {
      this.fetchfunds();
    },
    methods: {
      async fetchfunds() {
        try {
          const response = await axios.get('/get-funds/');
          this.funds = response.data;
        } catch (error) {
          console.error('Error fetching loans:', error);
        }
      },
    },
  };
  </script>
  