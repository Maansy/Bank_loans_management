<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <h1 class="text-h5 py-4">Loan Details</h1>
            </v-col>

            <v-col class="text-h6 py-3">
                <strong>{{ this.name }}</strong>
            </v-col>

            <v-col cols="12">
                <v-row> <!-- Centering the column -->
                    <v-col cols="12" sm="6"> <!-- Adjust the size of the column -->
                        <v-text-field label="Enter Your amount" v-model="amount" required></v-text-field>
                    </v-col>
                </v-row>
                <v-card>
                    <v-card-text>
                        <v-row>
                            <v-col cols="12" sm="6">
                                <strong>Min amount:</strong> ${{ this.min_loan_amount }}
                            </v-col>

                            <v-col cols="12" sm="6">
                                <strong>Max amount:</strong> ${{ this.max_loan_amount }}
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12" sm="6">
                                <strong>Duration:</strong> {{ this.duration }} years
                            </v-col>
                            <v-col cols="12" sm="6">
                                <strong>Interest Rate:</strong> {{ this.interest_rate }}%
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12" sm="6">
                                <strong>Description:</strong> {{ this.description }}
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12" sm="6">
                                <v-alert type="error" v-if="errors.length" v-for="error in errors" :key="error">{{ error
                                }}</v-alert>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12" sm="6">
                                <v-btn color="success" type="submit" @click="subcribeLoan(amount)" block>Submit</v-btn>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Loan',
    data() {
        return {
            name: '', // Assuming these are the details you want to fetch
            duration: '',
            description: '',
            interest_rate: '',
            min_loan_amount: '',
            max_loan_amount: '',
            errors: [], // For error handling
        };
    },
    mounted() {
        this.fetchLoanDetails();
    },
    methods: {
        async submitForm() {
            // Your existing form submission logic
        },
        async fetchLoanDetails() {
            try {
                const loanId = this.$route.params.loanId; // If using Vue Router and the loan ID is a route parameter
                console.log(loanId);
                const response = await axios.get(`/get-loan/${loanId}`); // Adjust the URL as per your API requirements
                // Assuming the API returns an object with amount and duration fields
                console.log(response.data);
                this.name = response.data.name;
                this.duration = response.data.duration;
                this.description = response.data.description;
                this.interest_rate = response.data.interest_rate;
                this.min_loan_amount = response.data.min_loan_amount;
                this.max_loan_amount = response.data.max_loan_amount;

            } catch (error) {
                console.error('Error fetching loan details:', error);
                this.errors.push('Failed to fetch loan details');
            }
        },
        subcribeLoan(amount) {
            if (amount < this.min_loan_amount || amount > this.max_loan_amount) {
                this.errors.push('Amount should be between min and max amount');
                return;
            }

        },
    },
};
</script>