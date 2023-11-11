import { createStore } from 'vuex'

function setCookie(name, value, days) {
  let expires = "";
  if (days) {
    let date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
  let nameEQ = name + "=";
  let ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

function eraseCookie(name) {
  // Set the cookie with an expiration date in the past
  document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    user: {
      id: '',
      username: '',
      email: '',
    },
    role: '',
    isVerified: false,
  },
  mutations: {
    initializeStore(state) {
      let token = getCookie('token');
      let role = getCookie('role');
      if (token) {
        state.token = token;
        state.isAuthenticated = true;
        state.role = role;
      } else {
        state.token = '';
        state.isAuthenticated = false;
        state.role = '';
        state.isVerified = false;
      }
    },
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = true;
      setCookie('token', token, 7); // Set for 7 days, adjust as needed
    },
    setUser(state, user) {
      state.user = user;
    },
    setRole(state, role) {
      state.role = role;
      setCookie('role', role, 7); // Set for 7 days, adjust as needed
    },
    setIsVerified(state, isVerified) {
      state.isVerified = isVerified;
    },
    logout(state) {
      state.token = '';
      state.isAuthenticated = false;
      state.user = { id: '', username: '', email: '', };
      state.role = '';
      eraseCookie('token');
      eraseCookie('role');
    }
  },
  actions: {
    // Actions can be added here for asynchronous operations
    initializeAuthentication({ commit }) {
      commit('initializeStore');
    },
  },
  modules: {
    // Other modules
  }
})
