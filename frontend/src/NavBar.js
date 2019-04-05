import React, { Component } from 'react';


class NavBar extends Component {
    render() {
        return (
            <div id="header">
                <span className="float-left">
                    <a href="/"><div id="logo"></div></a>
                    <form id="search">
                    <input type="text" />
                    <button><i className="fa fa-search"></i></button>
                </form>
                </span>
                    <span className="float-right">
                    <a href="#" id="cart-icon" title="Course Cart">
                        <i id="cart" className="fa fa-shopping-cart"></i>
                        <span id="cart-count"></span>
                    </a>
                </span>
            </div>
        );
    }
}

export default NavBar;
