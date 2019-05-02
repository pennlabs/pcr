import React, { Component } from 'react';
import AsyncSelect from 'react-select/lib/Async';
import { components } from 'react-select';
import { css } from 'emotion';
import { api_autocomplete } from './api';
import { withRouter } from 'react-router-dom';


class SearchBar extends Component {
    constructor(props) {
        super(props);

        this.state = {
            autocompleteOptions: [],
            searchValue: null
        };

        this._autocompleteCallback = [];
        this.autocompleteCallback = this.autocompleteCallback.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
        api_autocomplete().then((result) => {
            var formattedAutocomplete = [
                {
                    label: "Departments",
                    options: result.departments.map((i) => {
                        return {...i, value: i.url, label: i.title, group: i.category, keywords: i.keywords + " " + i.desc};
                    })
                },
                {
                    label: "Courses",
                    options: result.courses.map((i) => {
                        return {...i, value: i.url, label: i.title, group: i.category, keywords: i.keywords + " " + i.desc};
                    })
                },
                {
                    label: "Instructors",
                    options: result.instructors.map((i) => {
                        return {...i, value: i.url, label: i.title, group: i.category, keywords: i.keywords + " " + i.desc};
                    })
                }
            ];

            this.setState(state => ({
                autocompleteOptions: formattedAutocomplete
            }), () => {
                this._autocompleteCallback.forEach((x) => x(this.state.autocompleteOptions));
                this._autocompleteCallback = [];
            });
        }).catch((e) => {
            window.Raven.captureException(e);
            this.setState(state => ({
                autocompleteOptions: []
            }), () => {
                this._autocompleteCallback.forEach((x) => x(this.state.autocompleteOptions));
                this._autocompleteCallback = [];
            });
        });
    }

    filterOptionsList(autocompleteOptions, inputValue) {
        inputValue = inputValue.toLowerCase();
        return [
            {
                label: "Departments",
                options: autocompleteOptions[0].options.filter((i) => i.keywords.toLowerCase().indexOf(inputValue) !== -1).splice(0, 10)
            },
            {
                label: "Courses",
                options: autocompleteOptions[1].options.filter((i) => i.keywords.toLowerCase().indexOf(inputValue) !== -1).splice(0, 25)
            },
            {
                label: "Instructors",
                options: autocompleteOptions[2].options.filter((i) => i.keywords.toLowerCase().indexOf(inputValue) !== -1).splice(0, 25)
            }
        ];
    }

    autocompleteCallback(inputValue) {
        return new Promise((resolve, reject) => {
            if (this.state.autocompleteOptions.length) {
                resolve(this.state.autocompleteOptions);
            }
            else {
                this._autocompleteCallback.push(resolve);
            }
        }).then((res) => this.filterOptionsList(res, inputValue));
    }

    handleChange(value) {
        this.props.history.push("/" + value.url);
        this.setState({
            searchValue: null
        });
    }

    render() {
        return (
            <div id="search" style={{ margin: '0 auto' }}>
                <AsyncSelect onChange={this.handleChange} value={this.state.searchValue} placeholder={this.props.isTitle ? "Search for a class or professor" : ""} loadOptions={this.autocompleteCallback} defaultOptions components={{
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
                        <span style={{ color: '#aaa', fontSize: '0.8em', marginLeft: 3 }}>{props.data.desc}</span>
                        </div>);
                    },
                    DropdownIndicator: this.props.isTitle ? null : (props) => <components.DropdownIndicator {...props}><i className="fa fa-search mr-1"></i></components.DropdownIndicator>
                }} styles={{
                    container: styles => ({ ...styles, width: this.props.isTitle ? 'calc(100vw - 60px)' : 'calc(100vw - 200px)', maxWidth: this.props.isTitle ? 600 : 514 }),
                    control: (styles, state) => ({
                        ...styles, borderRadius: this.props.isTitle ? 0 : 32,
                        boxShadow: !this.props.isTitle ? 'none' : (state.isFocused ? '0px 2px 14px #ddd' : '0 2px 14px 0 rgba(0, 0, 0, 0.07)'),
                        backgroundColor: this.props.isTitle ? 'white' : '#f8f8f8',
                        borderColor: 'transparent',
                        cursor: 'pointer',
                        '&:hover': { },
                        fontSize: this.props.isTitle ? '30px' : null
                    }),
                    input: styles => ({ ...styles, marginLeft: this.props.isTitle ? 0 : 10, outline: 'none', border: 'none' }),
                    option: styles => ({ ...styles, paddingTop: 5, paddingBottom: 5, cursor: 'pointer' }),
                    placeholder: styles => ({ ...styles, whiteSpace: 'nowrap', color: '#b2b2b2' })
                }} />
            </div>
        );
    }
}

export default withRouter(SearchBar);
