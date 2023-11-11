import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import HomeView from '../views/HomeView.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import MyAccount from '../views/dashboard/MyAccount.vue'
import DashboardBank from '../views/dashboard/bank/DashboardBank.vue'
import CreateLoan from '../views/dashboard/bank/CreateLoan.vue'
import CreateFund from '../views/dashboard/bank/CreateFund.vue'
import DashboardCustomer from '../views/dashboard/customer/DashboardCustomer.vue'
import Loans from '../views/dashboard/customer/Loans.vue'
import DashboardProvider from '../views/dashboard/provider/DashboardProvider.vue'
import Funds from '../views/dashboard/provider/Funds.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp,
    meta: {
      youAreLogin: true
    }
  },
  {
    path: '/Login',
    name: 'LogIn',
    component: LogIn,
    meta: {
      youAreLogin: true
    }
  },
  {
    path: '/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/customer-dashboard',
    name: 'DashboardCustomer',
    component: DashboardCustomer,
    meta: {
      requireLogin: true,
      youAreCustomer: true
    }
  },
  {
    path: '/loans',
    name: 'Loans',
    component: Loans,
    meta: {
      requireLogin: true,
      youAreCustomer: true
    }
  },
  {
    path: '/provider-dashboard',
    name: 'DashboardProvider',
    component: DashboardProvider,
    meta: {
      requireLogin: true,
      youAreProvider: true
    }
  },
  {
    path: '/funds',
    name: 'Funds',
    component: Funds,
    meta: {
      requireLogin: true,
      youAreProvider: true
    }
  },
  {
    path: '/bank-dashboard',
    name: 'DashboardBank',
    component: DashboardBank,
    meta: {
      requireLogin: true,
      youAreBanker: true
    }
  },
  {
    path: '/create-loan',
    name: 'CreateLoan',
    component: CreateLoan,
    meta: {
      requireLogin: true,
      youAreBanker: true
    }
  },
  {
    path: '/create-fund',
    name: 'CreateFund',
    component: CreateFund,
    meta: {
      requireLogin: true,
      youAreBanker: true
    }
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// if you are not authenticated, you can't go to any page
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin)) {
    if (!store.state.isAuthenticated) {
      next('/login'); // Redirect to login if not authenticated
    } else {
      next(); // Proceed to the route
    }
  } else {
    next(); // No authentication required
  }
});

// if you are authenticated, you can't go to login or sign-up page
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.youAreLogin)) {
    if (store.state.isAuthenticated) {
      next('/my-account'); // Redirect to login if not authenticated
    } else {
      next(); // Proceed to the route
    }
  } else {
    next(); // No authentication required
  }
});

// handle banker pages
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.youAreBanker)) {
    if (store.state.role != 'bank') {
      next('/my-account'); 
    } else {
      next(); // Proceed to the route
    }
  } else {
    next(); // No authentication required
  }
});

// // handle provider pages
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.youAreProvider)) {
    if (store.state.role === 'customer') {
      next('/my-account'); // Redirect to login if not authenticated
    } else {
      next(); // Proceed to the route
    }
  } else {
    next(); // No authentication required
  }
});


// // handle customer pages
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.youAreCustomer)) {
    if (store.state.role === 'provider') {
      next('/my-account'); // Redirect to login if not authenticated
    } else {
      next(); // Proceed to the route
    }
  } else {
    next(); // No authentication required
  }
});


export default router
