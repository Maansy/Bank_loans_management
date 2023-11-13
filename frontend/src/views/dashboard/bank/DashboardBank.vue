<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" text>Fund Requests</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="headers" :items="fundRequests" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.fund.name }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                            <td align="center">{{ item.user.user.username }}</td>
                            <td align="center">{{ item.created_at }}</td>
                            <td align="center">{{ item.is_approved }}</td>
                            <td align="center">
                                <v-btn small v-bind:color="type === 0 ? 'success' : 'error'" @click="approveReq(item.id)">
                                    Appprove
                                </v-btn>
                                <v-btn small v-bind:color="type === 1 ? 'success' : 'error'" @click="rejectReq(item.id)">
                                    Reject
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
                <v-btn color="primary" text>Approved Fund Requests</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="secondHeaders" :items="approvedRequests" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.fund.name }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                            <td align="center">{{ item.user.user.username }}</td>
                            <td align="center">{{ item.created_at }}</td>
                            <td align="center">{{ item.assigned_by.user.username }}</td>
                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" text>Rejected Fund Requests</v-btn>
            </v-col>
            <v-col cols="12">
                <v-data-table :headers="secondHeaders" :items="rejectedRequests" class="elevation-1">
                    <template v-slot:item="{ item }">
                        <tr>
                            <td align="center">{{ item.fund.name }}</td>
                            <td align="center">{{ item.payed_amount }}</td>
                            <td align="center">{{ item.user.user.username }}</td>
                            <td align="center">{{ item.created_at }}</td>
                            <td align="center">{{ item.assigned_by.user.username }}</td>
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
                { title: 'Fund Name', key: 'fund.name', align: 'center' },
                { title: 'Payed Amount', key: 'payed_amount', align: 'center' },
                { title: 'User', key: 'user.user.username', align: 'center' },
                { title: 'Created At', key: 'created_at', align: 'center' },
                { title: 'Is Approved', key: 'is_approved', align: 'center' },
                { title: 'Actions', key: 'actions', align: 'center' },
            ],
            secondHeaders: [
                { title: 'Fund Name', key: 'fund.name', align: 'center' },
                { title: 'Payed Amount', key: 'payed_amount', align: 'center' },
                { title: 'User', key: 'user.user.username', align: 'center' },
                { title: 'Created At', key: 'created_at', align: 'center' },
                { title: 'Assigned by', key: 'assigned_by.user.username', align: 'center' },
            ],
            fundRequests: [],
            approvedRequests: [],
            rejectedRequests: [],
        };
    },
    mounted() {
        this.fetchFundRequests();
        this.fetchApprovedRequests();
        this.fetchRejectedRequests();
    },
    methods: {
        async fetchFundRequests() {
            try {
                // const fundId = this.$route.params.fundId;
                const response = await axios.get('/get-non-assigned-fund-request/');
                this.fundRequests = response.data;
            } catch (error) {
                console.error('Error fetching fund requests:', error);
            }
        },
        async approveReq(id) {
            try {
                await axios.put(`/approve-fund-request/${id}/`)
                    .then((response) => {
                        this.fetchFundRequests();
                        this.fetchApprovedRequests();
                        this.fetchRejectedRequests();
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            } catch (error) {
                console.error('Error approving fund request:', error);
            }
        },
        async rejectReq(id) {
            try {
                await axios.put(`/reject-fund-request/${id}/`)
                    .then((response) => {
                        this.fetchFundRequests();
                        this.fetchApprovedRequests();
                        this.fetchRejectedRequests();
                    })
                    .catch((error) => {
                        console.log(error);
                    });
                console.log("Reject: ", id);
            } catch (error) {
                console.error('Error rejecting fund request:', error);
            }
        },
        async fetchApprovedRequests() {
            try {
                // const fundId = this.$route.params.fundId;
                const response = await axios.get('/get-approved-fund-request/');
                this.approvedRequests = response.data;
            } catch (error) {
                console.error('Error fetching fund requests:', error);
            }
        },
        async fetchRejectedRequests() {
            try {
                // const fundId = this.$route.params.fundId;
                const response = await axios.get('/get-rejected-fund-request/');
                this.rejectedRequests = response.data;
            } catch (error) {
                console.error('Error fetching fund requests:', error);
            }
        }
    }

}
</script>