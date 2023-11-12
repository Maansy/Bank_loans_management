<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <h1 class="text-h5 py-4">Fund Details</h1>
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
                                <strong>Min amount:</strong> ${{ this.min_fund_amount }}
                            </v-col>

                            <v-col cols="12" sm="6">
                                <strong>Max amount:</strong> ${{ this.max_fund_amount }}
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
                                <v-btn color="success" type="submit" @click="subcribeFund(amount)" block>Submit</v-btn>
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
    name: 'Fund',
    data() {
        return {
            name: '', // Assuming these are the details you want to fetch
            duration: '',
            description: '',
            interest_rate: '',
            min_fund_amount: '',
            max_fund_amount: '',
            errors: [], // For error handling
        };
    },
    mounted() {
        this.fetchfundDetails();
    },
    methods: {
        async submitForm() {
            // Your existing form submission logic
        },
        async fetchfundDetails() {
            try {
                const fundId = this.$route.params.fundId; // If using Vue Router and the loan ID is a route parameter
                console.log(fundId);
                const response = await axios.get(`/get-fund/${fundId}`); // Adjust the URL as per your API requirements
                // Assuming the API returns an object with amount and duration fields
                console.log(response.data);
                this.name = response.data.name;
                this.duration = response.data.duration;
                this.description = response.data.description;
                this.interest_rate = response.data.interest_rate;
                this.min_fund_amount = response.data.min_fund_amount;
                this.max_fund_amount = response.data.max_fund_amount;

            } catch (error) {
                console.error('Error fetching fund details:', error);
                this.errors.push('Failed to fetch fund details');
            }
        },
        subcribeFund(amount) {
            if (amount < this.min_fund_amount || amount > this.max_fund_amount) {
                this.errors.push('Amount should be between min and max amount');
                return;
            }
            console.log(amount);
        },
    },
};
</script>