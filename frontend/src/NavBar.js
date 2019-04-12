import React, { Component } from 'react';
import SearchBar from './SearchBar';


class NavBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div id="header">
                <span className="float-left">
                    <a href="/"><div id="logo"></div></a>
                    <SearchBar onSelect={this.props.onSelect} />
                </span>
                    <span className="float-right">
                    <a href="/cart" id="cart-icon" title="Course Cart">
                        <i id="cart" className="fa fa-shopping-cart"></i>
                        <span id="cart-count"></span>
                    </a>
                </span>
            </div>
        );
    }
}

export default NavBar;
