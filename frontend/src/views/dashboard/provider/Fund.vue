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
                <v-row> 
                    <v-col cols="12" sm="6"> 
                        <v-text-field label="Enter Your amount" v-model="this.amount" required></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6"> 
                        <v-text-field label="Amount after fund period" v-model="this.after_period" :disabled="true"
                            required></v-text-field>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <v-btn color="success" type="Submit" @click="calc_amount(amount)" block >Calculate your money after period</v-btn>
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
                            <v-col >
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
            name: '',
            duration: '',
            description: '',
            interest_rate: '',
            min_fund_amount: '',
            max_fund_amount: '',
            amount: '',
            after_period: '',
            errors: [],
        };
    },
    mounted() {
        this.fetchfundDetails();
    },
    methods: {
        async fetchfundDetails() {
            try {
                const fundId = this.$route.params.fundId;
                const response = await axios.get(`/get-fund/${fundId}`);
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
        async subcribeFund(amount) {
            if (amount < this.min_fund_amount || amount > this.max_fund_amount || isNaN(amount) || amount < 0) {
                this.errors.push('Amount should be between min and max amount');
                return;
            }
            const fundId = this.$route.params.fundId;
            const payed_amount = amount
            await axios.post(`/request-fund/${fundId}/`, { payed_amount })
                .then((response) => {
                    this.$router.push('/provider-dashboard');
                })
                .catch((error) => {
                    console.error('Error subscribing fund:', error);
                    this.errors.push('Failed to subscribe fund');
                });
        },
        async calc_amount(amount){
            if (amount < this.min_fund_amount || amount > this.max_fund_amount || isNaN(amount) || amount < 0) {
                this.errors.push('Amount should be between min and max amount');
                return;
            }
            const fundId = this.$route.params.fundId;
            const response = await axios.get(`/calc-fund-interest/${fundId}/${amount}/`);
            this.after_period = response.data;
        }
    },
};
</script>