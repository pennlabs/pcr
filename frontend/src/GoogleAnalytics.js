import { Component } from 'react';
import { withRouter } from 'react-router-dom';


class GoogleAnalytics extends Component {
    componentWillUpdate({ location, history }) {
        if (location.pathname === this.props.location.pathname) {
            return;
        }

        if (history.action === 'PUSH') {
            window.ga('set', 'page', location.pathname + location.search);
            window.ga('send', 'pageview');
        }
    }

    render() {
        return null;
    }
}


export default withRouter(GoogleAnalytics);
