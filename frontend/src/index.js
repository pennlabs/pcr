import React from 'react'
import 'react-app-polyfill/ie11'
import 'react-app-polyfill/stable'

import ReactDOM from 'react-dom'
import { Route, Switch, BrowserRouter as Router } from 'react-router-dom'
import { AboutPage, AuthPage, ErrorPage, FAQPage, InfoPage, ReviewPage } from './pages'
import { GoogleAnalytics } from './components/common'

if (window.location.hostname !== 'localhost') {
  window.Raven.config(
    'https://1eab3b29efe0416fa948c7cd23ed930a@sentry.pennlabs.org/5'
  ).install()
}

ReactDOM.render(
  <Router>
    <Switch>
      <Route exact path="/" component={ReviewPage} />
      <Route path="/about" component={AboutPage} />
      <Route path="/faq" component={FAQPage} />
      <Route
        path="/:type(course|department|instructor)/:code"
        component={AuthPage}
      />
      <Route path="/:page(cart)" component={InfoPage} />
      <Route component={ErrorPage} />
    </Switch>
    <GoogleAnalytics />
  </Router>,
  document.getElementById('root')
)
