import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';


class Footer extends Component {
    render() {
        return (<div style={this.props.style} id="footer">
            <div id="footer-inner">
                <Link to="/about">About</Link> | <Link to="/faq">FAQs</Link> | <a target="_blank" rel="noopener noreferrer" href="https://docs.google.com/spreadsheet/viewform?formkey=dFNZYW92cFM1YnpKUzlLcXRDZVQ4VGc6MQ#gid=0faq">Feedback</a> | <a onClick={() => Cookies.remove('token')} href="/logout">Logout</a>

                <p id="copyright">
                Made with <i style={{color: '#F56F71'}} className="fa fa-heart" /> by <a href="https://pennlabs.org"><strong>Penn Labs</strong></a> | Hosted by <a href="https://stwing.upenn.edu/"><strong>STWing</strong></a>
                </p>
            </div>
        </div>);
    }
}


export default Footer;
