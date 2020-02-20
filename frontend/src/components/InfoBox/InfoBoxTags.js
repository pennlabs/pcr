/* eslint react/prop-types: 0 */
import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { convertInstructorName } from '../../utils/helpers'
import { CourseDetails, Popover, PopoverTitle } from '../common'

/**
 * Shows information about course availability, prerequisites, and new instructors.
 */
class Tags extends Component {
  render() {
    const existing = this.props.existing_instructors.map(convertInstructorName)
    const newInstructors = {}
    if (this.props.instructors) {
      this.props.instructors.forEach(i => {
        const key = convertInstructorName(i)
        newInstructors[key] = i
      })
    }
    existing.forEach(i => {
      delete newInstructors[i]
    })

    const isTaught = Object.values(this.props.courses).length > 0
    let mostRecent = null

    if (!isTaught) {
      const semesterTaught = Math.max(
        ...Object.values(this.props.data.instructors)
          .map(a => a.most_recent_semester)
          .filter(a => typeof a !== 'undefined')
          .map(a => {
            const x = a.split(' ')
            return parseInt(x[1]) * 3 + { Spring: 0, Summer: 1, Fall: 2 }[x[0]]
          })
      )
      if (semesterTaught > 0) {
        mostRecent = `${
          ['Spring', 'Summer', 'Fall'][semesterTaught % 3]
        } ${Math.floor(semesterTaught / 3)}`
      }
    }

    const syllabi = [].concat
      .apply(
        [],
        Object.values(this.props.courses).map(a =>
          Object.values(a)
            .map(b => ({
              url: b.syllabus_url,
              name: `${b.section_id_normalized} - ${(b.instructors || [])
                .map(c => c.name)
                .join(', ') || 'Unknown'}`,
            }))
            .filter(b => b.url)
        )
      )
      .sort((a, b) => a.name.localeCompare(b.name))
    const prereqString = [].concat
      .apply(
        [],
        Object.values(this.props.courses).map(a =>
          Object.values(a)
            .map(b => (b.prerequisite_notes || []).join(' '))
            .filter(b => b)
        )
      )
      .join(' ')
    const prereqs = [
      ...new Set(prereqString.match(/[A-Z]{2,4}[ -]\d{3}/g)),
    ].map(a => a.replace(' ', '-'))

    const courseName = this.props.data.code.replace('-', ' ')

    return (
      <div>
        <div id="live">
          {isTaught ? (
            <PopoverTitle
              title={
                <span>
                  {courseName} will be taught in <b>{this.props.term}</b>.
                </span>
              }
            >
              <span className="badge badge-info">{this.props.term}</span>
            </PopoverTitle>
          ) : (
            <PopoverTitle
              title={
                <span>
                  {courseName} was last taught in <b>{mostRecent}</b>.
                </span>
              }
            >
              <span className="badge badge-secondary">{mostRecent}</span>
            </PopoverTitle>
          )}
          {isTaught && (
            <PopoverTitle
              title={
                <span>
                  {courseName} is <b>{this.props.credits}</b> credit unit
                  {this.props.credits === 1 || 's'}
                </span>
              }
            >
              <span className="badge badge-primary">
                {this.props.credits} CU
              </span>
            </PopoverTitle>
          )}
          {Object.values(this.props.courses).map((info, i) => {
            if (!info.length) {
              return null
            }
            const desc = info[0].activity_description
            const open = info.filter(a => !a.is_closed && !a.is_cancelled)
            return (
              <PopoverTitle
                key={i}
                title={
                  <span>
                    <b>{open.length}</b> out of
                    <b>{info.length}</b> {desc.toLowerCase()} sections are open
                    for {courseName}.
                    <ul style={{ marginBottom: 0 }}>
                      {info
                        .sort((x, y) =>
                          x.section_id_normalized.localeCompare(
                            y.section_id_normalized
                          )
                        )
                        .map((data, i) => (
                          <CourseDetails key={i} data={data} />
                        ))}
                    </ul>
                  </span>
                }
              >
                <span
                  className={`badge ${
                    open.length ? 'badge-success' : 'badge-danger'
                  }`}
                >
                  {desc}
                  <span className="count">
                    {open.length}/{info.length}
                  </span>
                </span>
              </PopoverTitle>
            )
          })}
          {!!syllabi.length && (
            <Popover
              button={
                <span className="badge badge-secondary">
                  {syllabi.length}{' '}
                  {syllabi.length !== 1 ? 'Syllabi' : 'Syllabus'}
                </span>
              }
            >
              {syllabi.map((a, i) => (
                <div key={i}>
                  <a target="_blank" rel="noopener noreferrer" href={a.url}>
                    {a.name}
                  </a>
                </div>
              ))}
            </Popover>
          )}
        </div>
        {!!prereqs.length && (
          <div className="prereqs">
            Prerequisites:
            {prereqs.map((a, i) => [
              i > 0 && ', ',
              <span key={i}>
                <Link to={`/course/${a}`}>{a.replace('-', ' ')}</Link>
              </span>,
            ])}
          </div>
        )}
        {!!Object.keys(newInstructors).length && (
          <div>
            New Instructors:
            {Object.values(newInstructors)
              .sort()
              .map((item, i) => (
                <span key={i}>
                  {i > 0 && ', '}
                  {this.props.instructor_links[item] ? (
                    <Link
                      to={`/instructor/${this.props.instructor_links[item]}`}
                    >
                      {item}
                    </Link>
                  ) : (
                    item
                  )}
                </span>
              ))}
          </div>
        )}
      </div>
    )
  }
}

export default Tags
