import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router } from 'react-router-dom';
import ReviewPage from './ReviewPage';
import InfoPage from './InfoPage';
import AuthPage from './AuthPage';

ReactDOM.render(<Router>
    <Route exact path="/" component={ReviewPage} />
    <Route path="/:type(course|department|instructor)/:code" component={AuthPage} />
    <Route path="/:page(about|faq|cart)" component={InfoPage} />
</Router>, document.getElementById('root'));
