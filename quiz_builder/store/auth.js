export const state = () => ({
    loggedIn: false,
    userName: '',
    emailId: ''
})

export const mutations = {
    setLoggedIn(state, payload) {
        state.loggedIn = payload
    },
    setUserName(state, payload) {
        state.userName = payload
    },
    setEmailId(state, payload) {
      state.emailId = payload
    }
}
