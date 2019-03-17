/* eslint react/prop-types: 0 */
import React, { Component } from 'react';

class Tags extends Component {
  // state
  constructor(props) {

    super(props);

    this.state = {
    };

  }

  // add # of lecture and # of recitation here if desired
  render() {
    return (
      <div id="live">
        <span className="badge badge-info" title="" data-original-title={"This course will be taught in <b>" + this.props.term + "</b>."}>{this.props.term}</span>
        <span className="badge badge-primary" title="" data-original-title={"This course is <b>" + this.props.credit + "</b> credit unit(s)."}>{this.props.credits} CU</span>
      </div>
    );
  }
}

export default Tags;
