import React from 'react'
import 'react-app-polyfill/ie11'
import 'react-app-polyfill/stable'

import ReactDOM from 'react-dom'
import { Route, Switch, BrowserRouter as Router } from 'react-router-dom'
import { ReviewPage, AuthPage, InfoPage } from './pages'
import GoogleAnalytics from './components/GoogleAnalytics'

if (window.location.hostname !== 'localhost') {
  window.Raven.config(
    'https://1eab3b29efe0416fa948c7cd23ed930a@sentry.pennlabs.org/5'
  ).install()
}

ReactDOM.render(
  <Router>
    <Switch>
      <Route exact path="/" component={ReviewPage} />
      <Route
        path="/:type(course|department|instructor)/:code"
        component={AuthPage}
      />
      <Route path="/:page(about|faq|cart)" component={InfoPage} />
      <Route component={InfoPage} />
    </Switch>
    <GoogleAnalytics />
  </Router>,
  document.getElementById('root')
)
