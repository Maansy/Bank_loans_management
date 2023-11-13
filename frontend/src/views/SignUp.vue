<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12" sm="8" md="4">
                <v-card>
                    <v-card-title class="headline">Sign Up</v-card-title>
                    <v-card-text>
                        <v-form>
                            <v-text-field label="username" v-model="username" />
                            <v-text-field type="password" label="Password" v-model="password1" />
                            <v-text-field type="password" label="Repeat Password" v-model="password2" />
                            <v-text-field type="email" label="Email" v-model="email" />
                            <v-text-field label="First Name" v-model="first_name" />
                            <v-text-field label="Last Name" v-model="last_name" />
                            <v-text-field label="Phone" v-model="contact_number" />
                            <v-text-field label="City" v-model="city" />
                            <v-text-field label="State" v-model="state" />
                            <v-text-field label="Address" v-model="address" />


                            <!-- Role Selection Dropdown -->
                            <v-select label="Select" v-model="selectedRole" :items=roles variant="underlined"
                                @update:modelValue="toggleSecondForm"></v-select>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12" sm="8" md="4" v-if="showBankForm">
                <v-card>
                    <v-card-title class="headline">Bank Personal</v-card-title>
                    <v-card-text>
                        <v-form @submit.prevent="submitFormBankPersonal">
                            <v-text-field label="Bank Name" v-model="bank_name" />
                            <v-text-field label="Bank Branch" v-model="bank_branch" />

                            <!-- Role Selection Dropdown -->
                            <v-alert type="error" v-if="errors.length">
                                <ul>
                                    <li v-for="error in errors" :key="error">{{ error }}</li>
                                </ul>
                            </v-alert>

                            <v-btn color="success" type="submit">Submit</v-btn>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>

            <v-col cols="12" sm="8" md="4" v-if="showCustomerForm">
                <v-card>
                    <v-card-title class="headline">Customer</v-card-title>
                    <v-card-text>
                        <v-form @submit.prevent="submitFormCustomer">
                            <v-text-field label="Max Income" v-model="max_income" />

                            <v-alert type="error" v-if="errors.length">
                                <ul>
                                    <li v-for="error in errors" :key="error">{{ error }}</li>
                                </ul>
                            </v-alert>

                            <v-btn color="success" type="submit">Submit</v-btn>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>

            <v-col cols="12" sm="8" md="4" v-if="showLoanProviderForm">
                <v-card>
                    <v-card-title class="headline">Provider</v-card-title>
                    <v-card-text>
                        <v-form @submit.prevent="submitFormLoanProvider">
                            <v-text-field label="Max Amount" v-model="max_amount" />

                            <!-- Role Selection Dropdown -->
                            <v-alert type="error" v-if="errors.length">
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
import { toast } from 'bulma-toast'
export default {
    data: () => ({
        username: '',
        password1: '',
        address: '',
        password2: '',
        first_name: '',
        last_name: '',
        email: '',
        contact_number: '',
        city: '',
        state: '',
        errors: [],
        bank_name: '',
        bank_branch: '',
        max_income: '',
        max_amount: '',
        selectedRole: null,
        showBankForm: false,
        showCustomerForm: false,
        showLoanProviderForm: false,
        roles: ['Bank Personal', 'Customer', 'Loan Provider'],
    }),
    mounted() {
    },
    methods: {
        async submitFormLoanProvider() {
            const provider_data = {
                user: {
                    username: this.username,
                    password: this.password1,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    email: this.email,
                },
                address: this.address,
                contact_number: this.contact_number,
                city: this.city,
                state: this.state,
                max_amount: this.max_amount,
            }

            const apiEndpoint = 'loan-provider/';

            await axios
                .post(apiEndpoint, provider_data)
                .then(response => {
                    toast({
                        message: 'Sign up successfully',
                        type: 'is-success',
                        position: 'bottom-right',
                        duration: 3000,
                    })
                    this.$router.push('/login')

                })
                .catch(error => {
                    console.log(error);
                    this.errors = []; // Reset errors array to avoid duplicates.
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
        },
        async submitFormCustomer() {
            const customer_data = {
                user: {
                    username: this.username,
                    password: this.password1,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    email: this.email,
                },
                address: this.address,
                contact_number: this.contact_number,
                city: this.city,
                state: this.state,
                max_income: this.max_income,
            }

            const apiEndpoint = 'loan-customer/';

            await axios
                .post(apiEndpoint, customer_data)
                .then(response => {
                    toast({
                        message: 'Sign up successfully',
                        type: 'is-success',
                        position: 'bottom-right',
                        duration: 3000,
                    })
                    this.$router.push('/login')
                })
                .catch(error => {
                    console.log(error);
                    this.errors = []; // Reset errors array to avoid duplicates.
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
        },
        async submitFormBankPersonal() {
            const bank_personal_data = {
                user: {
                    username: this.username,
                    password: this.password1,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    email: this.email,
                },
                address: this.address,
                contact_number: this.contact_number,
                city: this.city,
                state: this.state,
                bank_name: this.bank_name,
                bank_branch: this.bank_branch,
            }

            const apiEndpoint = 'bank-personnel/';

            await axios
                .post(apiEndpoint, bank_personal_data)
                .then(response => {
                    toast({
                        message: 'Sign up successfully',
                        type: 'is-success',
                        position: 'bottom-right',
                        duration: 3000,
                    })
                    this.$router.push('/login')
                })
                .catch(error => {
                    console.log(error);
                    this.errors = []; // Reset errors array to avoid duplicates.
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
        },
        toggleSecondForm(value) {
            this.showBankForm = false;
            this.showCustomerForm = false;
            this.showLoanProviderForm = false;
            // Display the correct form based on the selected role
            switch (this.selectedRole) {
                case 'Bank Personal':
                    this.showBankForm = true;
                    break;
                case 'Customer':
                    this.showCustomerForm = true;
                    break;
                case 'Loan Provider':
                    this.showLoanProviderForm = true;
                    break;
            }
        },
    }
};
</script>
  