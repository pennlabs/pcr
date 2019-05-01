import React, { Component } from 'react';
import Cookies from 'js-cookie';

import ReviewPage from './ReviewPage';
import { redirect_for_auth, set_auth_token } from './api';


class AuthPage extends Component {
    constructor(props) {
        super(props);

        const token = Cookies.get('token');
        if (typeof token !== 'undefined') {
            set_auth_token();
            this.state = { isAuthed: true };
        }
        else {
            redirect_for_auth();
            this.state = { isAuthed: false };
        }
    }

    render() {
        return this.state.isAuthed ? <ReviewPage {...this.props} /> : null;
    }
}


export default AuthPage;
