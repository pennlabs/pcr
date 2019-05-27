import React, { Component } from 'react';


/**
 * A component that appears if an error occurs in the page.
 */
export default class ErrorBox extends Component {
    render() {
        return <div style={{ textAlign: 'center', padding: 45 }}>
            <i className='fa fa-exclamation-circle' style={{ fontSize: '150px', color: '#aaa' }}></i>
            <h1 style={{ fontSize: '1.5em', marginTop: 15 }}>{this.props.children}</h1>
            <small>If this problem persists, contact Penn Labs at <a href='mailto:contact@pennlabs.org'>contact@pennlabs.org</a>.</small>
        </div>
    }
}
