import React, { Component } from 'react';
import SearchBar from './SearchBar';
import { Link } from 'react-router-dom';


/**
 * The navigation bar at the top of the page, containing the logo, search bar, and cart icon.
 */
class NavBar extends Component {
    constructor(props) {
        super(props);

        this.state = {
            courseCount: Object.keys(localStorage).filter((a) => !a.startsWith("meta-")).length
        };

        this.onStorageChange = this.onStorageChange.bind(this);
    }

    onStorageChange() {
        this.setState({
            courseCount: Object.keys(localStorage).filter((a) => !a.startsWith("meta-")).length
        });
    }

    componentDidMount() {
        window.addEventListener("storage", this.onStorageChange);
        window.onCartUpdated = this.onStorageChange;
    }

    componentWillUnmount() {
        window.removeEventListener("storage", this.onStorageChange);
        window.onCartUpdated = null;
    }

    render() {
        return (
            <div id="header">
                <span className="float-left">
                    <Link to="/" title="Go to Penn Course Review Home"><div id="logo"></div></Link>
                    <SearchBar />
                </span>
                    <span className="float-right">
                    <Link to="/cart" id="cart-icon" title="Course Cart">
                        <i id="cart" className="fa fa-shopping-cart"></i>
                        {this.state.courseCount > 0 && <span id="cart-count">{this.state.courseCount}</span>}
                    </Link>
                </span>
            </div>
        );
    }
}

export default NavBar;
