import React, { Component } from 'react';
import SearchBar from './SearchBar';


class NavBar extends Component {
    constructor(props) {
        super(props);

        this.state = {
            courseCount: Object.keys(localStorage).filter((a) => !a.startsWith("columns")).length
        };

        this.onStorageChange = this.onStorageChange.bind(this);
    }

    onStorageChange() {
        this.setState({
            courseCount: Object.keys(localStorage).filter((a) => !a.startsWith("columns")).length
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
                    <a href="/"><div id="logo"></div></a>
                    <SearchBar onSelect={this.props.onSelect} />
                </span>
                    <span className="float-right">
                    <a href="/cart" id="cart-icon" title="Course Cart">
                        <i id="cart" className="fa fa-shopping-cart"></i>
                        {this.state.courseCount > 0 && <span id="cart-count">{this.state.courseCount}</span>}
                    </a>
                </span>
            </div>
        );
    }
}

export default NavBar;
