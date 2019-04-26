/* eslint react/prop-types: 0 */
import React, { Component } from 'react';
import Popover, { PopoverTitle } from './Popover';
import { Link } from 'react-router-dom';

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

    const is_taught = Object.values(this.props.courses).length > 0;
    var most_recent = null;

    if (!is_taught) {
        const semester_taught = Math.max(...Object.values(this.props.data.instructors).map((a) => a.most_recent_semester).filter((a) => typeof a !== 'undefined').map((a) => {
            const x = a.split(" ");
            return parseInt(x[1]) * 3 + {'Spring': 0, 'Summer': 1, 'Fall': 2}[x[0]];
        }));
        most_recent = ['Spring', 'Summer', 'Fall'][semester_taught % 3] + " " + Math.floor(semester_taught / 3);
    }

    const syllabi = [].concat.apply([], Object.values(this.props.courses).map((a) => Object.values(a).map((b) => ({url: b.syllabus_url, name: b.section_id_normalized + ' - ' + (b.instructors.map((c) => c.name).join(', ') || 'Unknown')})).filter((b) => b.url))).sort((a, b) => a.name.localeCompare(b.name));
    const prereq_string = [].concat.apply([], Object.values(this.props.courses).map((a) => Object.values(a).map((b) => b.prerequisite_notes.join(" ")).filter((b) => b))).join(" ");
    const prereqs = [...new Set(prereq_string.match(/[A-Z]{2,4}[ -]\d{3}/g))].map((a) => a.replace(' ', '-'));

    return (
        <div>
            <div id="live">
                {is_taught ? <PopoverTitle title={<span>This course will be taught in <b>{this.props.term}</b>.</span>}><span className="badge badge-info">{this.props.term}</span></PopoverTitle>
                           : <PopoverTitle title={<span>This course was last taught in <b>{most_recent}</b>.</span>}><span className="badge badge-secondary">{most_recent}</span></PopoverTitle>}
                {is_taught && <PopoverTitle title={<span>This course is <b>{this.props.credits}</b> credit unit(s).</span>}><span className="badge badge-primary">{this.props.credits} CU</span></PopoverTitle>}
                {Object.values(this.props.courses).map((info, i) => {
                    const desc = info[0].activity_description;
                    const open = info.filter((a) => !a.is_closed && !a.is_cancelled);
                    return <PopoverTitle key={i} title={<span><b>{open.length}</b> out of <b>{info.length}</b> {desc.toLowerCase()} sections are open for this course.<ul style={{ marginBottom: 0 }}>{open.map((a) => a.section_id_normalized).sort().map((a, i) => <li key={i}>{a}</li>)}</ul></span>}><span className={"badge " + (open ? "badge-success" : "badge-danger")}>{desc}<span className="count">{open.length}/{info.length}</span></span></PopoverTitle>;
                })}
                {!!syllabi.length && <Popover button={<span className="badge badge-secondary">{syllabi.length} {syllabi.length !== 1 ? 'Syllabi' : 'Syllabus'}</span>}>
                    {syllabi.map((a, i) => <div key={i}><a target="_blank" rel="noopener noreferrer" href={a.url}>{a.name}</a></div>)}
                </Popover>}
            </div>
            {!!prereqs.length && <div className="prereqs">Prerequisites: {prereqs.map((a, i) => [i > 0 && ", ", <span key={i}><Link to={"/course/" + a}>{a}</Link></span>])}</div>}
            {!!Object.keys(new_instructors).length && <div>New Instructors: {Object.values(new_instructors).sort().map((item, i) => <span key={i}>{i > 0 && ", "}{this.props.instructor_links[item] ? <Link to={this.props.instructor_links[item]}>{item}</Link> : item}</span>)}</div>}
        </div>
    );
  }
}

export { Tags, convertInstructorName };
export default Tags;
