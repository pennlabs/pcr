import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { redirect_for_logout } from './api';


/**
 * The footer of every page.
 */
class Footer extends Component {
    render() {
        return (<div style={this.props.style} id="footer">
            <div id="footer-inner">
                <Link to="/about">About</Link> | <Link to="/faq">FAQs</Link> | <a target="_blank" rel="noopener noreferrer" href="https://airtable.com/shrVygSaHDL6BswfT">Feedback</a> | <a onClick={redirect_for_logout} href="#">Logout</a>

                <p id="copyright">
                Made with <i style={{color: '#F56F71'}} className="fa fa-heart" /> by <a href="https://pennlabs.org"><strong>Penn Labs</strong></a> | Hosted by <a href="https://www.stwing.upenn.edu/"><strong>STWing</strong></a>
                </p>
            </div>
        </div>);
    }
}


export default Footer;
