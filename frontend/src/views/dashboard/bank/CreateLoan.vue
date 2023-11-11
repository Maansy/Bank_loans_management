<template>
    <v-container>
        <v-row>
            <v-col cols="12" sm="8" md="4">
                <v-btn color="primary" to="/loans">All Loans</v-btn>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12" sm="8" md="4">
                <v-card>
                    <v-card-title class="headline">Add a loan</v-card-title>
                    <v-card-text>
                        <v-form @submit.prevent="submitForm">
                            <v-text-field label="Name" v-model="name" />
                            <v-text-field label="Description" v-model="description" />
                            <v-text-field label="Interest rate" v-model="interest_rate" />
                            <v-text-field label="Min loan amount" v-model="min_loan_amount" />
                            <v-text-field label="Max loan amount" v-model="max_loan_amount" />
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
import { toast } from 'bulma-toast'
export default {
    name: 'CreateLoan',
    data() {
        return {
            name: '',
            description: '',
            interest_rate: '',
            max_loan_amount: '',
            min_loan_amount: '',
            duration: '',
            errors: [],
        }
    },
    methods: {
        async submitForm() {
            try {
                if (this.max_loan_amount <= this.min_loan_amount) {
                    this.errors.push("Max loan amount must be greater than min loan amount")
                    return
                }
                else if (this.max_loan_amount < 0 || this.min_loan_amount < 0) {
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
                    const response = await axios.post('/create-loan/', {
                        name: this.name,
                        description: this.description,
                        interest_rate: this.interest_rate,
                        max_loan_amount: this.max_loan_amount,
                        min_loan_amount: this.min_loan_amount,
                        duration: this.duration,
                    })
                    .then(
                        toast({
                            message: 'Loan created successfully',
                            type: 'is-success',
                            position: 'bottom-right',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                        })
                    )
                    this.$router.push({ name: 'Loans' });
                    
                }

            } catch (error) {
                console.log(error);
            }
        },
    }

}
</script>