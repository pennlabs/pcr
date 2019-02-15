import React, { Component } from 'react';

class Tags extends Component {
  // state
  constructor(props) {

    super(props)

    this.state = {
      //board = Array(9).fill(null)
    }
  }

  // events like handleClick

  render() {
    i
    return (
      <div id="live">
        <span className="badge badge-info" title="" data-original-title="This course will be taught in <b>Spring 2019</b>.">Spring 2019</span>
        <span className="badge badge-primary" title="" data-original-title="This course is <b>1.0</b> credit unit(s).">1.0 CU</span>
        <span className="badge badge-success" title="" data-original-title="<b>13</b> out of <b>15</b> recitation sections are open for this course.">Recitation
          <span className="count">13/15</span>
        </span>
       <span className="badge badge-success" title="" data-original-title="<b>2</b> out of <b>2</b> lecture sections are open for this course.">Lecture
        </span>
      </div>
    );
  }
}

export default Tags;
