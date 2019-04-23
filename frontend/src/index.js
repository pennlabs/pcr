import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router } from 'react-router-dom';
import ReviewPage from './ReviewPage';

ReactDOM.render(<Router>
    <Route exact path="/" component={ReviewPage} />
    <Route path="/:type(course|department|instructor)/:code" component={ReviewPage} />
</Router>, document.getElementById('root'));
