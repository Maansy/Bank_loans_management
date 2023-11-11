<template>
    <v-app-bar app dark>
        <v-toolbar-title>
            <router-link to="/" class="white--text">Bank Loans</router-link>
        </v-toolbar-title>

        <v-spacer></v-spacer> <!-- This component is used to push the navigation to the right -->

        <template v-if="!$store.state.isAuthenticated">
            <v-btn text color="white" to="/login">
                <strong>Login</strong>
            </v-btn>
            <v-btn text color="white" to="/sign-up">
                Register
            </v-btn>
        </template>

        <template v-else>
            <template v-if="$store.state.isVerified">
                <template v-if="$store.state.role === 'bank'">
                    <v-btn text color="white" to="/bank-dashboard">
                        Dashboard
                    </v-btn>
                    <v-btn text color="white" to="/create-loan">
                        Create Loan
                    </v-btn>
                    <v-btn text color="white" to="/create-fund">
                        Create Fund
                    </v-btn>
                </template>

                <template v-else-if="$store.state.role === 'customer'">
                    <v-btn text color="white" to="/customer-dashboard">
                        Dashboard
                    </v-btn>
                    <v-btn text color="white" to="/loans">
                        Loans
                    </v-btn>
                </template>

                <template v-else-if="$store.state.role === 'provider'">
                    <v-btn text color="white" to="/provider-dashboard">
                        Dashboard
                    </v-btn>
                    <v-btn text color="white" to="/funds">
                        Funds
                    </v-btn>
                </template>
            </template>

            <v-btn text color="white" to="/my-account">
                Account
            </v-btn>
        </template>

    </v-app-bar>
</template>
  
<script>
export default {
    name: 'Navbar',
};
</script>
  