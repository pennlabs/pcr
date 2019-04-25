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
        if (!this.props.hover) {
            document.addEventListener('click', this.onHide);
        }
        if (!this.dialogElement) {
            this.dialogElement = document.createElement('div');
            this.dialogElement.style.position = 'static';
            document.body.appendChild(this.dialogElement);
            this.componentDidUpdate();
        }
    }

    componentWillUnmount() {
        if (!this.props.hover) {
            document.removeEventListener('click', this.onHide);
        }
        document.body.removeChild(this.dialogElement);
    }

    onHide(e) {
        if (!this.refs.button) {
            return;
        }
        const buttonElement = ReactDOM.findDOMNode(this.refs.button);
        if (buttonElement.contains(e.target)) {
            return;
        }
        if (!this.dialogElement.contains(e.target)) {
            this.setState({
                isShown: false
            });
        }
    }

    onToggle(val) {
        const buttonElement = ReactDOM.findDOMNode(this.refs.button).getBoundingClientRect();
        this.setState((state) => ({
            isShown: typeof val === 'undefined' ? !state.isShown : val,
            position: [buttonElement.left, buttonElement.bottom]
        }));
    }

    componentDidUpdate() {
        ReactDOM.render(
            this.state.isShown ? <div style={{
                ...this.props.style,
                    position: 'absolute',
                    backgroundColor: 'white',
                    zIndex: 1,
                    margin: 10,
                    marginLeft: 0,
                    padding: 15,
                    boxShadow: '0 0 14px 0 rgba(0, 0, 0, 0.07)',
                    borderRadius: 4.8,
                    top: this.state.position && this.state.position[1],
                    left: this.state.position && this.state.position[0]
            }}>{this.props.children}</div> : undefined, this.dialogElement);
    }

    render() {
        return (
            <span ref="button"
                style={{cursor: 'pointer'}}
                onClick={!this.props.hover ? () => this.onToggle() : undefined}
                onMouseEnter={this.props.hover ? () => this.onToggle(true) : undefined}
                onMouseLeave={this.props.hover ? () => this.onToggle(false) : undefined}>{this.props.button || <button>Toggle</button>}</span>
        );
    }
}


class PopoverTitle extends Component {
    render() {
        return <Popover hover button={this.props.children}>{this.props.title}</Popover>;
    }
}


export { PopoverTitle };
export default Popover;
