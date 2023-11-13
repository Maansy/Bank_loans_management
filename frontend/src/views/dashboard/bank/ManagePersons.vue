<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" text>Provider Requests</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers" :items="nonVerifiedProviders" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.user.first_name }}  {{ item.user.last_name }}</td>
                            <td align="center">{{ item.user.username }}</td>
                            <td align="center">{{ item.city }}</td>
                            <td align="center">{{ item.created_at }}</td>
                            <td align="center">{{ item.is_verified }}</td>
                            <td align="center">
                                <v-btn small v-bind:color="type === 0 ? 'success' : 'error'" @click="approveProvider(item.id)">
                                    Appprove
                                </v-btn>
                            </td>
                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" text>Customer Requests</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers" :items="nonVerifiedCustomers" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.user.first_name }}  {{ item.user.last_name }}</td>
                            <td align="center">{{ item.user.username }}</td>
                            <td align="center">{{ item.city }}</td>
                            <td align="center">{{ item.created_at }}</td>
                            <td align="center">{{ item.is_verified }}</td>
                            <td align="center">
                                <v-btn small v-bind:color="type === 0 ? 'success' : 'error'" @click="approveCustomer(item.id)">
                                    Appprove
                                </v-btn>
                            </td>
                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
import axios from 'axios';
export default {
    name: 'DashboardBank',
    data() {
        return {
            type: 0,
            headers: [
                { title: 'Name', key: '', align: 'center' },
                { title: 'Username', key: '', align: 'center' },
                { title: 'City', key: '', align: 'center' },
                { title: 'Created At', key: '', align: 'center' },
                { title: 'Is Approved', key: '', align: 'center' },
                { title: 'Actions', key: 'actions', align: 'center' },
            ],
            nonVerifiedProviders: [],
            nonVerifiedCustomers: [],
        };
    },
    mounted() {
        this.fetchNonVerifiedProviders();
        this.fetchNonVerifiedCustomers();
    },
    methods: {
        async approveProvider(id) {
            try {
                await axios.put(`/verify-provider/${id}/`)
                    .then((response) => {
                        this.fetchNonVerifiedProviders();
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            } catch (error) {
                console.error('Error approving fund request:', error);
            }
        },
        async approveCustomer(id) {
            try {
                await axios.put(`/verify-customer/${id}/`)
                    .then((response) => {
                        this.fetchNonVerifiedCustomers();
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            } catch (error) {
                console.error('Error rejecting fund request:', error);
            }
        },
        async fetchNonVerifiedProviders() {
            try {
                const response = await axios.get('/get-non-verified-providers/');
                this.nonVerifiedProviders = response.data;

            } catch (error) {
                console.error('Error fetching fund requests:', error);
            }
        },
        async fetchNonVerifiedCustomers() {
            try {
                const response = await axios.get('/get-non-verified-customers/');
                this.nonVerifiedCustomers = response.data;
            } catch (error) {
                console.error('Error fetching fund requests:', error);
            }
        },
    }

}
</script>