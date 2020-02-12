import React, { Component } from 'react'
import Cookies from 'js-cookie'

import NavBar from './NavBar'
import Footer from './Footer'
import ErrorBox from './ErrorBox'
import ReviewPage from './ReviewPage'
import { redirectForAuth, apiIsAuthenticated } from './api'

/**
 * A wrapper around a review page that performs Shibboleth authentication.
 */
class AuthPage extends Component {
  constructor(props) {
    super(props)

    this.state = {
      isAuthed: false,
      authFailed: false,
    }

    const tempCookie = 'doing_token_auth'
    apiIsAuthenticated(authed => {
      if (authed) {
        Cookies.remove(tempCookie)
        this.setState({ isAuthed: true, authFailed: false })
      } else {
        if (typeof Cookies.get(tempCookie) === 'undefined') {
          Cookies.set(tempCookie, 'true', { expires: 1 / 1440 })
          redirectForAuth()
          this.setState({ isAuthed: false, authFailed: false })
        } else {
          Cookies.remove(tempCookie)
          this.setState({ isAuthed: false, authFailed: true })
        }
      }
    })
  }

  render() {
    const { authFailed, isAuthed } = this.state
    if (authFailed) {
      return (
        <div>
          <NavBar />
          <ErrorBox>
            Could not perform Platform authentication.
            <br />
            Refresh this page to try again.
          </ErrorBox>
          <Footer />
        </div>
      )
    }
    // TODO: Add loading spinner instead of null
    return isAuthed ? <ReviewPage {...this.props} /> : null
  }
}

export default AuthPage
