<template>
  <v-container>
    <v-layout>
      <v-flex xs12>
        <v-card>
          <v-card-text>
            <v-flex xs12>
              <v-text-field v-model="link" label="Enter any quiz link to take quiz" type="link" solo single-line></v-text-field>
                <n-link :to="`/${link}`">
                  <v-btn class="indigo" dark>Take quiz</v-btn>
                </n-link>
            </v-flex>
          </v-card-text>
        </v-card>
        <v-row class="mt-2">
          <v-col>
            <v-card>
              <v-card-title><h1 class="display-1">Login</h1></v-card-title>
              <v-card-text>
                <v-flex xs12>
                  <v-text-field v-model="email1" label="Email" type="email" solo single-line></v-text-field>
                  <v-text-field v-model="password1" label="Password" type="password" solo single-line></v-text-field>
                  <v-btn block class="indigo" dark @click="login">Login</v-btn>
                </v-flex>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col>
            <v-card>
              <v-card-title><h1 class="display-1">Sign Up</h1></v-card-title>
              <v-card-text>
                <v-flex xs12>
                  <v-text-field v-model="name" label="Name" type="name" solo single-line></v-text-field>
                  <v-text-field v-model="email2" label="Email" type="email" solo single-line></v-text-field>
                  <v-text-field v-model="password2" label="Password" type="password" solo single-line></v-text-field>
                  <v-btn block class="indigo" dark @click="signup">Sign Up</v-btn>
                </v-flex>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  middleware: 'guest',
  data() {
    return {
      link: '',
      email1: '',
      password1: '',
      name: '',
      email2: '',
      password2: '',
    }
  },
  methods: {
    login() {
      this.$axios
        .$post(
          `https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=${
            process.env.FIREBASE_KEY
          }`,
          {
            email: this.email1,
            password: this.password1,
            returnSecureToken: true
          }
        )
        .then(res => {
          this.handleTokenLogin(res)
        })
        .catch(error => {
          this.$notify({
            group: 'notify',
            title: 'Error in Login',
            text: `${error.response.data.error.message}`
          });
        })
    },
    signup() {
      this.$axios
        .$post(
          `https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=${
            process.env.FIREBASE_KEY
          }`,
          {
            email: this.email2,
            password: this.password2,
            returnSecureToken: true
          }
        )
        .then(res => {
          this.handleTokenSignup(res)
        })
        .catch(error => {
          this.$notify({
            group: 'notify',
            title: 'Error in Sign Up',
            text: `${error.response.data.error.message}`
          });
        })
    },
    handleTokenLogin(data) {
      this.$cookies.set('token', data.idToken)
      this.$cookies.set('emailId', data.email)
      this.$store.commit('auth/setEmailId', data.email)
      this.$axios.$post('/api/getUser',
      {
        email: data.email
      }).then(res => {
        this.$cookies.set('userName', res.name)
        this.$store.commit('auth/setUserName', res.name)
      })
      this.$store.commit('auth/setLoggedIn', true)
      this.$router.push('/home')
    },
    handleTokenSignup(data) {
      this.$axios.$post('/api/createUser',
      {
        email: data.email,
        name: this.name
      })
      this.$cookies.set('token', data.idToken)
      this.$cookies.set('emailId', data.email)
      this.$store.commit('auth/setEmailId', data.email)
      this.$cookies.set('userName', this.name)
      this.$store.commit('auth/setUserName', this.name)
      this.$store.commit('auth/setLoggedIn', true)
      this.$router.push('/home')
    }
  }
}
</script>

<style></style>