import React, { Component } from 'react';
import ReviewPage from './ReviewPage';
import { get_auth_url, get_auth_origin, set_auth_token } from './api';


class AuthPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isAuthed: false,
            authUrl: get_auth_url()
        };

        this.receiveMessage = this.receiveMessage.bind(this);
        this.forceReauth = this.forceReauth.bind(this);
    }

    componentWillUpdate() {
        if (!this.state.isAuthed && this.state.authUrl) {
            document.body.style.overflow = 'hidden';
        }
        else {
            document.body.style.overflow = null;
        }
    }

    receiveMessage(e) {
        if (e.origin !== get_auth_origin()) {
            return;
        }
        if (e.data.type !== 'pcrAuth') {
            return;
        }
        if (typeof e.data.token !== 'string' || !e.data.token.startsWith('user_')) {
            return;
        }
        set_auth_token(e.data.token);
        this.setState({ isAuthed: true });
        document.body.style.overflow = null;
    }

    forceReauth() {
        this.setState({
            isAuthed: false
        });
    }

    componentWillUnmount() {
        window.auth = null;
        window.removeEventListener('message', this.receiveMessage, false);
        document.body.style.overflow = null;
    }

    componentDidMount() {
        window.auth = this;
        window.addEventListener('message', this.receiveMessage, false);
    }

    render() {
        return this.state.isAuthed ? <ReviewPage {...this.props} /> : <iframe title="Penn Authentication" style={{ width: '100vw', height: '100vh' }} src={this.state.authUrl} />;
    }
}


export default AuthPage;
