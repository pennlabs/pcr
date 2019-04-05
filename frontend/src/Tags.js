/* eslint react/prop-types: 0 */
import React, { Component } from 'react';

class Tags extends Component {
  // state
  constructor(props) {
    super(props);
  }

  // add # of lecture and # of recitation here if desired
  render() {
    return (
      <div id="live">
        <span className="badge badge-info" title={"This course will be taught in " + this.props.term + "."}>{this.props.term}</span>
        <span className="badge badge-primary" title={"This course is " + this.props.credits + " credit unit(s)."}>{this.props.credits} CU</span>
        {Object.values(this.props.courses).map((info, i) => {
            const desc = info[0].activity_description;
            const open = info.filter((a) => !a.is_closed && !a.is_cancelled).length;
            console.log(info);
            return <span key={i} className="badge badge-success" title={open + " out of " + info.length + " lecture sections are open for this course."}>{desc}<span className="count">{open}/{info.length}</span></span>;
        })}
      </div>
    );
  }
}

export default Tags;
