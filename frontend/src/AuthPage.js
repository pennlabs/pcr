import React, { Component } from 'react'
import Cookies from 'js-cookie'

import NavBar from './NavBar'
import Footer from './Footer'
import ErrorBox from './ErrorBox'
import ReviewPage from './ReviewPage'
import { redirect_for_auth, api_is_authenticated } from './api'

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
  }

  render() {
    const { authFailed, isAuthed } = this.state
    if (authFailed) {
      return (
        <div>
          <NavBar />
          <ErrorBox>
            Could not perform Shibboleth authentication.
            <br />
            Refresh this page to try again.
          </ErrorBox>
          <Footer />
        </div>
      )
    }

    return isAuthed ? <ReviewPage {...this.props} /> : null
  }
}

export default AuthPage
