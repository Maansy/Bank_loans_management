<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <h1 class="text-h5 py-4">My Account</h1>
            </v-col>

            <v-col cols="12">

                <h1 class="text-h6 py-4">Account Information</h1>
                <v-card>
                    <v-card-text>
                        <v-row>
                            <v-col cols="12" sm="6">
                                <strong>Username:</strong> {{ this.username }}
                            </v-col>
                            <v-col cols="12" sm="6">
                                <strong>Email:</strong> {{ this.email }}
                            </v-col>

                        </v-row>
                        <v-row>
                            <v-col cols="12" sm="6">
                                <strong>First Name:</strong> {{ this.first_name }}
                            </v-col>
                            <v-col cols="12" sm="6">
                                <strong>Last Name:</strong> {{ this.last_name }}
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12" sm="3">
                                <strong>Role:</strong> {{ this.role }}
                            </v-col>
                            <v-col cols="12" sm="3">
                                <strong>Contact Number:</strong> {{ this.contact_number }}
                            </v-col>
                            <v-col cols="12" sm="3">
                                <strong>Is Verified:</strong> {{ this.is_verified }}
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="12" sm="3">
                                <strong>Address:</strong> {{ this.address }}
                            </v-col>
                            <v-col cols="12" sm="3">
                                <strong>City:</strong> {{ this.city }}
                            </v-col>

                            <v-col cols="12" sm="3">
                                <strong>State:</strong> {{ this.state }}
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12">

                <h1 class="text-h6 py-4">Additonal Information</h1>
                <v-card>
                    <v-card-text>
                        <v-row v-if="role === 'bank'">
                            <v-col cols="12" sm="6">
                                <strong>Bank Name:</strong> {{ this.bank_name }}
                            </v-col>
                            <v-col cols="12" sm="6">
                                <strong>Bank Branch:</strong> {{ this.bank_branch }}
                            </v-col>
                            <v-alert v-if="is_verified === 'No'" type="warning" class="mt-4">
                                <strong>Warning!</strong> Your account is not verified yet. Please contact the admin.
                            </v-alert>
                        </v-row>
                        <v-row v-if="role === 'customer'">
                            <v-col cols="12" sm="12">
                                <strong>Max Income:</strong> {{ this.max_income }}
                            </v-col>
                            <v-alert v-if="is_verified === 'No'" type="warning" class="mt-4">
                                <strong>Warning!</strong> Your account is not verified yet. Please contact the admin.
                            </v-alert>
                        </v-row>
                        <v-row v-if="role === 'provider'">
                            <v-col cols="12" sm="12">
                                <strong>Max Amount:</strong> {{ this.max_amount }}
                            </v-col>
                            <v-alert v-if="is_verified === 'No'" type="warning" class="mt-4">
                                <strong>Warning!</strong> Your account is not verified yet. Please contact the admin.
                            </v-alert>
                        </v-row>
                    </v-card-text>

                </v-card>
            </v-col>
            <v-col cols="12">
                <v-btn color="error" @click="logout">Log Out</v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
import { mapMutations } from 'vuex';
import { toast } from 'bulma-toast';
import axios from 'axios';
export default {
    name: 'MyAccount',
    data() {
        return {
            role: '', // from state
            username: '',
            email: '',
            first_name: '',
            last_name: '',
            address: '',
            city: '',
            state: '',
            contact_number: '',
            is_verified: '',
            bank_name: '',
            bank_branch: '',

            max_income: '',

            max_amount: '',
        }
    },
    mounted() {
        this.getAccountInfo();
        this.role = this.$store.state.role;
    },
    methods: {
        ...mapMutations({
            vuexLogout: 'logout'
        }),
        logout() {
            axios.post('/logout/')
                .catch(error => {
                    console.log(error);
                });
            this.vuexLogout();

            axios.defaults.headers.common['Authorization'] = '';

            this.$router.push('/login');
            toast({
                message: 'Log out successfully',
                type: 'is-danger',
                position: 'bottom-right',
                duration: 3000,
            })
        },
        async getAccountInfo() {
            await axios
                .get('/me/')
                .then(response => {
                    this.username = response.data.username;
                    this.email = response.data.email;
                    this.first_name = response.data.first_name;
                    this.last_name = response.data.last_name;
                    this.address = response.data.address;
                    this.city = response.data.city;
                    this.state = response.data.state;
                    this.contact_number = response.data.contact_number;
                    if (response.data.is_verified == true) {
                        this.is_verified = 'Yes';
                    } else {
                        this.is_verified = 'No';
                    }
                    this.bank_name = response.data.bank_name;
                    this.bank_branch = response.data.bank_branch;
                    this.max_income = response.data.max_income;
                    this.max_amount = response.data.max_amount;
                })
                .catch(error => {
                    console.log(error);
                });
        },
    }
}
</script>

