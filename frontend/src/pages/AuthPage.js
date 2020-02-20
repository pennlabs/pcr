import React, { useEffect, useState } from 'react'
import Cookies from 'js-cookie'

import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { ReviewPage } from './ReviewPage'
import { ErrorBox } from '../components/common'
import { redirectForAuth, apiIsAuthenticated } from '../api'

/**
 * A wrapper around a review page that performs Shibboleth authentication.
 */

export const AuthPage = props => {
  const [authed, setAuthed] = useState(false)
  const [authFailed, setAuthFailed] = useState(false)

  useEffect(() => {
    const tempCookie = 'doing_token_auth'
    apiIsAuthenticated(authed => {
      if (authed) {
        Cookies.remove(tempCookie)
        setAuthed(true)
        setAuthFailed(false)
      } else {
        if (typeof Cookies.get(tempCookie) === 'undefined') {
          Cookies.set(tempCookie, 'true', { expires: 1 / 1440 })
          redirectForAuth()
          setAuthed(false)
          setAuthFailed(false)
        } else {
          Cookies.remove(tempCookie)
          setAuthed(false)
          setAuthFailed(true)
        }
      }
    })
  }, [])

  if (authFailed) {
    return (
      <>
        <Navbar />
        <ErrorBox>
          Could not perform Platform authentication.
          <br />
          Refresh this page to try again.
        </ErrorBox>
        <Footer />
      </>
    )
  }
  // TODO: Add loading spinner instead of null
  return authed ? <ReviewPage {...props} /> : null
}
