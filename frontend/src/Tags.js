/* eslint react/prop-types: 0 */
import React, { Component } from 'react';
import { PopoverTitle } from './Popover';

// Converts an instructor name into a unique key that should be the same for historical data and the Penn directory.
const nameCache = {};

function convertInstructorName(name) {
    if (name in nameCache) {
        return nameCache[name];
    }
    const out = name.toUpperCase().replace(/[^a-zA-Z\s]/g, '').replace(/ [A-Z]+ /g, ' ');
    nameCache[name] = out;
    return out;
}

class Tags extends Component {
  render() {
    const existing = this.props.existing_instructors.map(convertInstructorName);
    const new_instructors = {};
    this.props.instructors.forEach((i) => {
        const key = convertInstructorName(i);
        new_instructors[key] = i;
    });
    existing.forEach((i) => {
        delete new_instructors[i];
    });

    return (
        <div>
            <div id="live">
                <PopoverTitle title={"This course will be taught in " + this.props.term + "."}><span className="badge badge-info">{this.props.term}</span></PopoverTitle>
                <PopoverTitle title={"This course is " + this.props.credits + " credit unit(s)."}><span className="badge badge-primary">{this.props.credits} CU</span></PopoverTitle>
                {Object.values(this.props.courses).map((info, i) => {
                    const desc = info[0].activity_description;
                    const open = info.filter((a) => !a.is_closed && !a.is_cancelled).length;
                    return <PopoverTitle key={i} title={open + " out of " + info.length + " " + desc.toLowerCase() + " sections are open for this course."}><span className={"badge " + (open ? "badge-success" : "badge-danger")}>{desc}<span className="count">{open}/{info.length}</span></span></PopoverTitle>;
                })}
            </div>
            {!!Object.keys(new_instructors).length && <small>New Instructors: {Object.values(new_instructors).sort().map((item, i) => <span key={i}>{i > 0 && ", "}{this.props.instructor_links[item] ? <a href={this.props.instructor_links[item]}>{item}</a> : item}</span>)}</small>}
        </div>
    );
  }
}

export { Tags, convertInstructorName };
export default Tags;
