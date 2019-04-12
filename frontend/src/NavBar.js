import React, { Component } from 'react';
import AsyncSelect from 'react-select/lib/Async';
import { css } from 'emotion';
import { api_autocomplete } from './api';


class NavBar extends Component {
    constructor(props) {
        super(props);

        this.state = {
            autocompleteOptions: []
        };

        this.autocompleteCallback = this.autocompleteCallback.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
        api_autocomplete().then((result) => {
            var formattedAutocomplete = [
                {
                    label: "Departments",
                    options: result.departments.map((i) => {
                        return {...i, value: i.url, label: i.title, group: i.category};
                    })
                },
                {
                    label: "Courses",
                    options: result.courses.map((i) => {
                        return {...i, value: i.url, label: i.title, group: i.category};
                    })
                },
                {
                    label: "Instructors",
                    options: result.instructors.map((i) => {
                        return {...i, value: i.url, label: i.title, group: i.category};
                    })
                }
            ];
            this.setState(state => ({
                autocompleteOptions: formattedAutocomplete
            }));
            if (this._autocompleteCallback) {
                this._autocompleteCallback();
                this._autocompleteCallback = null;
            }
        });
    }

    autocompleteCallback(inputValue, callback) {
        inputValue = inputValue.toLowerCase();

        if (this.state.autocompleteOptions.length) {
            callback([
                {
                    label: "Departments",
                    options: this.state.autocompleteOptions[0].options.filter((i) => i.keywords.toLowerCase().indexOf(inputValue) !== -1).splice(0, 10)
                },
                {
                    label: "Courses",
                    options: this.state.autocompleteOptions[1].options.filter((i) => i.keywords.toLowerCase().indexOf(inputValue) !== -1).splice(0, 25)
                },
                {
                    label: "Instructors",
                    options: this.state.autocompleteOptions[2].options.filter((i) => i.keywords.toLowerCase().indexOf(inputValue) !== -1).splice(0, 25)
                }
            ]);
        }
        else {
            this._autocompleteCallback = (data) => { this.autocompleteCallback(inputValue, callback); };
        }
    }

    handleChange(value) {
        if (this.props.onSelected) {
            this.props.onSelected(value);
        }
    }

    render() {
        return (
            <div id="header">
                <span className="float-left">
                    <a href="/"><div id="logo"></div></a>
                    <form id="search">
                        <AsyncSelect onChange={this.handleChange} loadOptions={this.autocompleteCallback} defaultOptions components={{
                            Option: (props) => {
                                const { children,  className, cx, getStyles, isDisabled, isFocused, isSelected, innerRef, innerProps } = props;
                                return (<div ref={innerRef}
                                className={cx(css(getStyles('option', props)),
                                    {
                                        'option': true,
                                        'option--is-disabled': isDisabled,
                                        'option--is-focused': isFocused,
                                        'option--is-selected': isSelected,
                                    },
                                    className
                                )} {...innerProps}>
                                <b>{children}</b>
                                <div style={{ color: '#aaa', fontSize: '0.8em' }}>{props.data.desc}</div>
                                </div>);
                            }
                        }} />
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
