import React, { Component } from 'react';
import ReactDOM from 'react-dom';


class Popover extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isShown: false
        };

        this.onToggle = this.onToggle.bind(this);
        this.onHide = this.onHide.bind(this);
    }

    componentDidMount() {
        document.addEventListener('click', this.onHide);
    }

    componentWillUnmount() {
        document.removeEventListener('click', this.onHide);
    }

    onHide(e) {
        const popupElement = ReactDOM.findDOMNode(this.refs.popup);
        if (!popupElement.contains(e.target)) {
            this.setState({
                isShown: false
            });
        }
    }

    onToggle() {
        this.setState((state) => ({
            isShown: !state.isShown
        }));
    }

    render() {
        return (
            <div ref="popup" style={{ position: 'relative' }}>
                <div onClick={this.onToggle}>{this.props.button || <button>Toggle</button>}</div>
                <div style={{
                    position: 'absolute',
                    backgroundColor: 'white',
                    zIndex: 1,
                    margin: 10,
                    padding: 15,
                    boxShadow: '0 0 14px 0 rgba(0, 0, 0, 0.07)',
                    borderRadius: 4.8,
                    display: this.state.isShown ? 'block' : 'none'
                }}>
                    {this.props.children}
                </div>
            </div>
        );
    }
}

export default Popover;
