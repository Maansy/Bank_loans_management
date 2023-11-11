<template>
    <v-container>
        <v-row>
            <v-col cols="12" sm="8" md="4">
                <v-btn color="primary" to="/funds">All Funds</v-btn>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12" sm="8" md="4">
                <v-card>
                    <v-card-title class="headline">Add a fund</v-card-title>
                    <v-card-text>
                        <v-form @submit.prevent="submitForm">
                            <v-text-field label="Name" v-model="name" />
                            <v-text-field label="Description" v-model="description" />
                            <v-text-field label="Interest rate" v-model="interest_rate" />
                            <v-text-field label="Min fund amount" v-model="min_fund_amount" />
                            <v-text-field label="Max fund amount" v-model="max_fund_amount" />
                            <v-text-field label="Duration" v-model="duration" />
                            <v-alert type="error" v-if="errors.length" v-for="error in errors" :key="error">{{ error
                            }}</v-alert>
                            <v-btn color="primary" type="submit">Submit</v-btn>
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
    name: 'CreateFund',
    data() {
        return {
            name: '',
            description: '',
            interest_rate: '',
            max_fund_amount: '',
            min_fund_amount: '',
            duration: '',
            errors: [],
        }
    },
    methods: {
        async submitForm() {
            try {
                if (this.max_fund_amount <= this.min_fund_amount) {
                    this.errors.push("Max loan amount must be greater than min loan amount")
                    return
                }
                else if (this.max_fund_amount < 0 || this.min_fund_amount < 0) {
                    this.errors.push("Loan amount must be greater than 0")
                    return
                }
                else if (this.duration < 0) {
                    this.errors.push("Duration must be greater than 0")
                    return
                }
                else if (this.interest_rate < 0) {
                    this.errors.push("Interest rate must be greater than 0")
                    return
                }
                else {
                    const response = await axios.post('/create-fund/', {
                        name: this.name,
                        description: this.description,
                        interest_rate: this.interest_rate,
                        max_fund_amount: this.max_fund_amount,
                        min_fund_amount: this.min_fund_amount,
                        duration: this.duration,
                    })
                    
                    this.$router.push({ name: 'Funds' });
                }

            } catch (error) {
                console.log(error);
            }
        },
    }

}
</script>