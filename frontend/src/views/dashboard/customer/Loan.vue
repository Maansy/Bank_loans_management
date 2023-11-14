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
                <v-row> 
                    <v-col cols="12" sm="4"> 
                        <v-text-field label="Enter Your amount $" v-model="this.amount" required></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="4"> 
                        <v-text-field label="Monthly amount $" v-model="this.monthly_amount" required
                            disabled></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="4"> 
                        <v-text-field label="Interest $" v-model="this.interest" required disabled></v-text-field>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <v-alert type="error" v-if="calc_errors.length" v-for="calc_error in calc_errors"
                            :key="calc_error">{{ calc_errors
                            }}</v-alert>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <v-btn color="success" type="Calculate the Monthly amount" @click="calculateMonthlyAmount(amount)"
                            block>Calculate Monthly Amount</v-btn>
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
                                <strong>Interest type:</strong> {{ this.interest_type }}
                            </v-col>
                            <v-col cols="12" sm="6">
                                <strong>Type:</strong> {{ this.loan_type }}
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <strong>Description:</strong> {{ this.description }}
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-alert type="error" v-if="errors.length" v-for="error in errors" :key="error">{{ error
                                }}</v-alert>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-btn color="success" type="submit" @click="subcribeLoan(amount)" block>Submit</v-btn>
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
            name: '',
            duration: 0,
            description: '',
            interest_rate: 0.0,
            interest: 0.0,
            monthly_amount: 0.0,
            min_loan_amount: 0.0,
            max_loan_amount: 0.0,
            amount: 0.0,
            loan_type: '',
            interest_type: '',
            errors: [], 
            calc_errors: [],
        };
    },
    mounted() {
        this.fetchLoanDetails();
    },
    methods: {
        async fetchLoanDetails() {
            try {
                const loanId = this.$route.params.loanId;
                const response = await axios.get(`/get-loan/${loanId}`);
                this.name = response.data.name;
                this.duration = response.data.duration;
                this.description = response.data.description;
                this.interest_rate = response.data.interest_rate;
                this.min_loan_amount = response.data.min_loan_amount;
                this.max_loan_amount = response.data.max_loan_amount;
                this.loan_type = response.data.loan_type;
                this.interest_type = response.data.interest_type;

            } catch (error) {
                console.error('Error fetching loan details:', error);
                this.errors.push('Failed to fetch loan details');
            }
        },
        subcribeLoan(amount) {
            if (amount < this.min_loan_amount || amount > this.max_loan_amount || isNaN(amount) || amount < 0) {
                this.errors.push('Amount should be between min and max amount');
                return;
            }
            const loanId = this.$route.params.loanId;
            axios.post(`/request-loan/${loanId}/`, { payed_amount: amount })
                .then((response) => {
                    this.$router.push('customer-dashboard/');
                })
                .catch((error) => {
                    console.log(error);
                    this.errors.push('Failed to subcribe loan');
                });
        },
        async calculateMonthlyAmount(amount) {
            if (amount < this.min_loan_amount || amount > this.max_loan_amount || isNaN(amount) || amount < 0) {
                this.calc_errors.push('Amount should be between min and max amount');
                return;
            }
            const loanId = this.$route.params.loanId;
            const response = await axios.get(`/calc-interest/${loanId}/${amount}/`);
            this.interest = response.data.interest;
            this.monthly_amount = response.data.monthly_payment;
        }
    },
};
</script>