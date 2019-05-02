import React, { Component } from 'react';
import Cookies from 'js-cookie';

import NavBar from './NavBar';
import Footer from './Footer';
import ErrorBox from './ErrorBox';
import ReviewPage from './ReviewPage';
import { redirect_for_auth, set_auth_token } from './api';


class AuthPage extends Component {
    constructor(props) {
        super(props);

        const temp_cookie_name = 'doing_token_auth';
        const token = Cookies.get('token');
        if (typeof token !== 'undefined') {
            set_auth_token(token);
            Cookies.remove(temp_cookie_name);
            this.state = { isAuthed: true, authFailed: false };
        }
        else {
            if (typeof Cookies.get(temp_cookie_name) === 'undefined') {
                Cookies.set(temp_cookie_name, 'true');
                redirect_for_auth();
                this.state = { isAuthed: false, authFailed: false };
            }
            else {
                Cookies.remove(temp_cookie_name);
                this.state = { isAuthed: false, authFailed: true };
            }
        }
    }

    render() {
        if (this.state.authFailed) {
            return <div>
                <NavBar />
                <ErrorBox>Could not perform Shibboleth authentication.<br />Refresh this page to try again.</ErrorBox>
                <Footer />
            </div>;
        }

        return this.state.isAuthed ? <ReviewPage {...this.props} /> : null;
    }
}


export default AuthPage;
