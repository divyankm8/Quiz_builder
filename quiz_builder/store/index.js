export const actions = {
    nuxtServerInit(
      { commit },
      {
        req,
        app: { $cookies }
      }
    ) {
      if (req.headers.cookie) {
        if ($cookies.get('token')) {
          commit('auth/setLoggedIn', true)
          commit('auth/setUserName', $cookies.get('userName'))
          commit('auth/setEmailId', $cookies.get('emailId'))
        }
      }
    }
  }
  