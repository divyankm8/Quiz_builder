<template>
  <v-app>
    <no-ssr>
      <notifications group="notify" />
    </no-ssr>
    <v-content>
      <v-toolbar color="indigo" dark>
        <v-toolbar-side-icon></v-toolbar-side-icon>
        <v-toolbar-title>
          <n-link to="/">Quiz Builder App</n-link>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-sm-and-down">
          <v-btn flat v-if="$auth()" @click="home">Welcome {{ userName }}</v-btn>
          <v-btn flat v-if="$auth()" @click="logout">
            Logout
          </v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <transition>
        <nuxt />
      </transition>
    </v-content>
  </v-app>
</template>

<script>
export default {
  computed: {
    userName() {
      return this.$store.state.auth.userName
    }
  },
  methods:{
    logout() {
      this.$cookies.remove('token')
      this.$cookies.remove('emailId')
      this.$cookies.remove('userName')
      this.$store.commit('auth/setLoggedIn', false)
      this.$store.commit('auth/setEmailId', '')
      this.$store.commit('auth/setUserName', '')
      this.$router.push('/')
    },
    home() {
      this.$router.push('/home')
    }
  }
}
</script>

<style>
a {
  text-decoration: none;
  color: white;
}
</style>
