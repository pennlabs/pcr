/* eslint react/prop-types: 0 */
import React, { Component } from 'react';

class Tags extends Component {
  render() {
    const existing = this.props.existing_instructors.map((a) => a.toUpperCase().replace(/[^a-zA-Z\s]/g, ''));
    const new_instructors = {};
    this.props.instructors.forEach((i) => {
        const key = i.toUpperCase().replace(/[^a-zA-Z\s]/g, '');
        new_instructors[key] = i;
    });
    existing.forEach((i) => {
        delete new_instructors[i];
    });

    return (
        <div>
            <div id="live">
                <span className="badge badge-info" title={"This course will be taught in " + this.props.term + "."}>{this.props.term}</span>
                <span className="badge badge-primary" title={"This course is " + this.props.credits + " credit unit(s)."}>{this.props.credits} CU</span>
                {Object.values(this.props.courses).map((info, i) => {
                    const desc = info[0].activity_description;
                    const open = info.filter((a) => !a.is_closed && !a.is_cancelled).length;
                    return <span key={i} className={"badge " + (open ? "badge-success" : "badge-danger")} title={open + " out of " + info.length + " lecture sections are open for this course."}>{desc}<span className="count">{open}/{info.length}</span></span>;
                })}
            </div>
            {!!Object.keys(new_instructors).length && <small>New Instructors: {Object.values(new_instructors).sort().join(", ")}</small>}
        </div>
    );
  }
}

export default Tags;
