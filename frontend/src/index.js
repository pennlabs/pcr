import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Switch, Router } from 'react-router-dom';
import { createBrowserHistory } from 'history';
import ReviewPage from './ReviewPage';
import InfoPage from './InfoPage';
import AuthPage from './AuthPage';

var history = createBrowserHistory();
history.listen(function(loc) {
    window.ga('set', 'page', loc.pathname + loc.search);
    window.ga('send', 'pageview');
});

ReactDOM.render(<Router history={history}>
    <Switch>
        <Route exact path="/" component={ReviewPage} />
        <Route path="/:type(course|department|instructor)/:code" component={AuthPage} />
        <Route path="/:page(about|faq|cart)" component={InfoPage} />
        <Route component={InfoPage} />
    </Switch>
</Router>, document.getElementById('root'));
