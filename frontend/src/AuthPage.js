import React, { Component } from 'react';
import ReviewPage from './ReviewPage';
import { api_auth } from './api';


class AuthPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isAuthed: false,
            authUrl: null
        };

        this.checkAuth = this.checkAuth.bind(this);
    }

    componentWillUpdate() {
        if (!this.state.isAuthed && this.state.authUrl) {
            document.body.style.overflow = 'hidden';
        }
        else {
            document.body.style.overflow = null;
        }
    }

    componentWillUnmount() {
        document.body.style.overflow = null;
    }

    checkAuth() {
        api_auth().then(() => {
            this.setState({
                isAuthed: true
            });
        }).catch((url) => {
            this.setState({
                isAuthed: false,
                authUrl: url
            });
        });
    }

    componentDidMount() {
        this.checkAuth();
    }

    render() {
        return this.state.isAuthed ? <ReviewPage {...this.props} /> : (this.state.authUrl ? <iframe title="Penn Authentication" style={{ width: '100vw', height: '100vh' }} onLoad={this.checkAuth} src={this.state.authUrl} /> : <div></div>);
    }
}


export default AuthPage;
