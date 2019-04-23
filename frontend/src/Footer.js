import React, { Component } from 'react';
import { Link } from 'react-router-dom';


class Footer extends Component {
    render() {
        return (<div style={this.props.style} id="footer">
            <div id="footer-inner">
                <Link to="/about">About</Link> | <Link to="/faq">FAQs</Link> | <a href="https://docs.google.com/spreadsheet/viewform?formkey=dFNZYW92cFM1YnpKUzlLcXRDZVQ4VGc6MQ#gid=0faq">Feedback</a> | <Link to="/logout">Logout</Link>

                <p id="copyright">
                Copyright &copy; {new Date().getFullYear()} <a href="https://pennlabs.org"><strong>Penn Labs</strong></a> | Hosted by <a href="https://stwing.upenn.edu/"><strong>STWing</strong></a>
                </p>
            </div>
        </div>);
    }
}


export default Footer;
