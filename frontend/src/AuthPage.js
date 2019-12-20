import React, { Component } from 'react';
import Cookies from 'js-cookie';

import NavBar from './NavBar';
import Footer from './Footer';
import ErrorBox from './ErrorBox';
import ReviewPage from './ReviewPage';
import { redirect_for_auth, api_is_authenticated } from './api';


/**
 * A wrapper around a review page that performs Shibboleth authentication.
 */
class AuthPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isAuthed: false,
            authFailed: false
        };

        const temp_cookie_name = 'doing_token_auth';
        api_is_authenticated((authed) => {
            if (authed) {
                Cookies.remove(temp_cookie_name);
                this.setState({ isAuthed: true, authFailed: false });
            }
            else {
                if (typeof Cookies.get(temp_cookie_name) === 'undefined') {
                    Cookies.set(temp_cookie_name, 'true', { expires: 1/1440 });
                    redirect_for_auth();
                    this.setState({ isAuthed: false, authFailed: false });
                }
                else {
                    Cookies.remove(temp_cookie_name);
                    this.setState({ isAuthed: false, authFailed: true });
                }
            }
        });
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
