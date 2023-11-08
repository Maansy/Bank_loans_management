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
            <v-btn text color="white" to="/dashboard/leads">
                Leads
            </v-btn>
            <v-btn text color="white" to="/dashboard/clients">
                Clients
            </v-btn>
            <v-btn text color="white" to="/dashboard/team">
                Team
            </v-btn>
            <v-btn text color="white" to="/dashboard/my-account">
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
  