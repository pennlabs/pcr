import React, { Component } from 'react';
import Cookies from 'js-cookie';

import ReviewPage from './ReviewPage';
import { redirect_for_auth, set_auth_token } from './api';


class AuthPage extends Component {
    constructor(props) {
        super(props);

        const token = Cookies.get('token');
        if (typeof token !== 'undefined') {
            set_auth_token(token);
            Cookies.remove('doing_token_auth');
            this.state = { isAuthed: true, authFailed: false };
        }
        else {
            if (typeof Cookies.get('doing_token_auth') === 'undefined') {
                Cookies.set('doing_token_auth', 'true');
                redirect_for_auth();
                this.state = { isAuthed: false, authFailed: false };
            }
            else {
                Cookies.remove('doing_token_auth');
                this.state = { isAuthed: false, authFailed: true };
            }
        }
    }

    render() {
        if (this.state.authFailed) {
            return <div>Failed to perform Shibboleth authentication. Refresh the page to try again.</div>;
        }

        return this.state.isAuthed ? <ReviewPage {...this.props} /> : null;
    }
}


export default AuthPage;
