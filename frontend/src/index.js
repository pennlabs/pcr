import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Switch, BrowserRouter as Router } from 'react-router-dom';
import ReviewPage from './ReviewPage';
import InfoPage from './InfoPage';
import AuthPage from './AuthPage';
import GoogleAnalytics from './GoogleAnalytics';


window.Raven.config('https://1eab3b29efe0416fa948c7cd23ed930a@sentry.pennlabs.org/5').install();


ReactDOM.render(<Router>
    <Switch>
        <Route exact path="/" component={ReviewPage} />
        <Route path="/:type(course|department|instructor)/:code" component={AuthPage} />
        <Route path="/:page(about|faq|cart)" component={InfoPage} />
        <Route component={InfoPage} />
    </Switch>
    <GoogleAnalytics />
</Router>, document.getElementById('root'));
