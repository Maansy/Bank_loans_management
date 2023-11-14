<template>
  <v-row>
    <v-col cols="12" sm="4" v-for="loan in loans" :key="loan.id">
      <v-card>
        <v-card-title>{{ loan.name }}</v-card-title>
        <v-card-subtitle>{{ loan.min_loan_amount }} - {{ loan.max_loan_amount }}</v-card-subtitle>
        <v-card-text>
          <p>Interest Rate: {{ loan.interest_rate }}%</p>
          <p>Duration: {{ loan.duration }} years</p>
          <p>Interest Type: {{ loan.interest_type }}</p>
          <p>Loan Type: {{ loan.loan_type }}</p>
          <template v-if="$store.state.role === 'bank'">
            <p>Fund: {{ loan.fund.name }}</p>
          </template>
        </v-card-text>
        <template v-if="$store.state.role === 'customer'">
          <v-card-actions>
            <v-btn color="primary" @click="subscribeToLoan(loan.id)">Subscribe</v-btn>
          </v-card-actions>
        </template>
      </v-card>
    </v-col>
  </v-row>
</template>
  
<script>
import axios from 'axios';

export default {
  name: 'Loans',
  data() {
    return {
      loans: [],
    };
  },
  mounted() {
    this.fetchLoans();
  },
  methods: {
    async fetchLoans() {
      try {
        const response = await axios.get('/get-loans/');
        this.loans = response.data;
      } catch (error) {
        console.error('Error fetching loans:', error);
      }
    },
    async subscribeToLoan(loanId) {
      try {
        this.$router.push({ name: 'Loan', params: { loanId } });
      } catch (error) {
        console.error('Error subscribing to loan:', error);
      }
    },
  },
};
</script>
  