import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router } from 'react-router-dom';
import ReviewPage from './ReviewPage';
import InfoPage from './InfoPage';

ReactDOM.render(<Router>
    <Route exact path="/" component={ReviewPage} />
    <Route path="/:type(course|department|instructor)/:code" component={ReviewPage} />
    <Route path="/:page(about|faq|cart)" component={InfoPage} />
</Router>, document.getElementById('root'));
