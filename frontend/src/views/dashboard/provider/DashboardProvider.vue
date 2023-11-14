<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" text> Waiting Payment</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers" :items="approved_funds" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.fund.name }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                            <td align="center">
                                <v-btn small @click="pay_amount(item.payed_amount, item.id)"
                                    v-bind:color="type === 0 ? 'success' : 'error'">
                                    Pay ${{ item.payed_amount }}
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
                <v-btn color="primary" text>Rejected</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers1" :items="rejected_funds" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.fund.name }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" text>Waiting For Bank Response</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers1" :items="non_approved_funds" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.fund.name }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" text>Payed Funds</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers2" :items="payed_funds" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.fund_name }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                            <td align="center">{{ item.total_amount }}</td>

                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
        <v-divider></v-divider>
    </v-container>
</template>


<script>
import axios from 'axios';
export default {
    name: 'DashboardProvider',
    data() {
        return {
            type: 0,
            headers: [
                { title: 'Fund Name', key: '', align: 'center' },
                { title: 'Payment amount', key: '', align: 'center' },
                { title: 'Actions', key: 'actions', align: 'center' },
            ],
            headers1: [
                { title: 'Fund Name', key: '', align: 'center' },
                { title: 'Payment amount', key: '', align: 'center' },
            ],
            headers2: [
                { title: 'Fund Name', key: '', align: 'center' },
                { title: 'Payment amount', key: '', align: 'center' },
                { title: 'Amount After Period', key: '', align: 'center' },

            ],
            approved_funds: [],
            non_approved_funds: [],
            rejected_funds: [],
            payed_funds: [],
        };
    },
    mounted() {
        this.fetchApprovedFunds();
        this.fetchRejectedFunds();
        this.fetchWatingFunds();
        this.fetchPayedFunds();
    },
    methods: {
        async fetchApprovedFunds() {
            try {
                const response = await axios.get('/get-approved-fund-waiting-payment/');
                this.approved_funds = response.data;
            } catch (error) {
                console.log(error);
            }

        },
        async fetchRejectedFunds() {
            try {
                const response = await axios.get('/get-rejected-funds/');
                this.rejected_funds = response.data;
            } catch (error) {
                console.log(error);
            }
        },
        async fetchWatingFunds() {
            try {
                const response = await axios.get('/get-waiting-approve-funds/');
                this.non_approved_funds = response.data;
            } catch (error) {
                console.log(error);
            }
        },
        async fetchPayedFunds() {
            try {
                const response = await axios.get('/get-payed-funds-with-interests/');
                this.payed_funds = response.data;
            } catch (error) {
                console.log(error);
            }
        },
        async pay_amount(payed_amount,id) {
            this.stripeCheckout(payed_amount,id);
        },
        async stripeCheckout(amount, id) {
            const stripe = Stripe('pk_test_51O6FfiCPlb6OgBYTTtNVQhyhaNBiwTNrT2KfyuXOi8zjopPigOBqqHCx0KTWxO93ks5iuuStW3PAJy2ZYnmn6vS300jEVHSn0K'); // Replace with your Stripe public key
            try {
                const response = await axios.post('/create-stripe-checkout-session/', { amount:amount , id:id });
                const sessionId = response.data.sessionId;
                await stripe.redirectToCheckout({ sessionId });
                console.log(response.data);
            } catch (error) {
                console.error('Error with Stripe checkout:', error);
            }
        },

    }

}
</script>