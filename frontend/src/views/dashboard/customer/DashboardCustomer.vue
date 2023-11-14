<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" text> In Progress</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers" :items="approved_loans" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.loan }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                            <td align="center">{{ item.duration }}</td>
                            <td align="center">{{ item.monthly_payment }}</td>
                            <td align="center">
                                <v-btn small @click="pay_amount(item.monthly_payment, item.id)"
                                    v-bind:color="type === 0 ? 'success' : 'error'">
                                    Pay ${{ item.monthly_payment }}
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
                <v-data-table :headers="headers1" :items="rejected_loans" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.loan.name }}</td>
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
                <v-data-table :headers="headers1" :items="non_approved_loans" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.loan.name }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" text>Your Loans</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers2" :items="sibscibations" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.loan }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                            <td align="center">{{ item.duration }}</td>
                            <td align="center">{{ item.monthly_payment }}</td>
                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
        <v-divider></v-divider>
        <!-- <v-row>
            <v-col cols="12">
                <v-btn color="primary" text>Loans Payment</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers1" :items="payed_loans" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.loan }}</td>
                            <td align="center">{{ item.interest }}</td>
                            <td align="center">{{ item.monthly_payment }}</td>
                            <td align="center">
                                <v-btn small @click="pay_amount(item.monthly_payment, item.id)"
                                    v-bind:color="type === 0 ? 'success' : 'error'">
                                    Pay ${{ item.monthly_payment }}
                                </v-btn>
                            </td>
                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
        <v-divider></v-divider> -->
    </v-container>
</template>


<script>
import axios from 'axios';
export default {
    name: 'DashboardCustomer',
    data() {
        return {
            type: 0,
            headers: [
                { title: 'Loan Name', key: '', align: 'center' },
                {title: 'Amount', key: '', align: 'center'},
                {title: 'Duration in months', key: '', align: 'center'},

                { title: 'Monthly Payment', key: '', align: 'center' },
                { title: 'Actions', key: 'actions', align: 'center' },
            ],
            
            headers1: [
                { title: 'Loan Name', key: '', align: 'center' },
                { title: 'Amount', key: '', align: 'center' },

            ],

            headers2: [
                { title: 'Loan Name', key: '', align: 'center' },
                {title: 'Amount', key: '', align: 'center'},
                {title: 'Duration in months', key: '', align: 'center'},

                { title: 'Monthly Payment', key: '', align: 'center' },
            ],

            approved_loans: [],
            non_approved_loans: [],
            rejected_loans: [],
            sibscibations : [],
        };
    },
    mounted() {
        this.fetchApprovedLoans();
        this.fetchRejectedLoans();
        this.fetchWatingLoans();
        this.fetchScribations();
    },
    methods: {
        async fetchApprovedLoans() {
            try {
                const response = await axios.get('/get-inprogress-loan/');
                this.approved_loans = response.data;
                console.log(this.approved_loans);
            } catch (error) {
                console.log(error);
            }

        },
        async fetchRejectedLoans() {
            try {
                const response = await axios.get('/get-rejected-loans/');
                this.rejected_loans = response.data;
            } catch (error) {
                console.log(error);
            }
        },
        async fetchWatingLoans() {
            try {
                const response = await axios.get('/get-waiting-approve-loans/');
                this.non_approved_loans = response.data;
            } catch (error) {
                console.log(error);
            }
        },
        async fetchScribations(){
            try {
                const response = await axios.get('/get-subscribed-loans/');
                this.sibscibations = response.data;
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
                const response = await axios.post('/create-checkout-session-loan/', { amount:amount , id:id });
                const sessionId = response.data.sessionId;
                await stripe.redirectToCheckout({ sessionId });
            } catch (error) {
                console.error('Error with Stripe checkout:', error);
                // Handle errors
            }
        },

    }

}
</script>