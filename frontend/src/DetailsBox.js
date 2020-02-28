import React, { forwardRef, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import ScoreTable from './ScoreTable'
import ColumnSelector from './ColumnSelector'
import { apiHistory } from './api'
import { getColumnName, orderColumns } from './ScoreBox'

// TODO: Move functions like compareSemesters and getColumnName in ScoreBox into a utils file
export function compareSemesters(a, b) {
  const ay = parseInt(a.split(' ')[1])
  const by = parseInt(b.split(' ')[1])
  const as = a.split(' ')[0]
  const bs = b.split(' ')[0]

  if (ay !== by) {
    return by - ay
  }

  const mapping = { Fall: 'A', Summer: 'B', Spring: 'C' }

  return mapping[as].localeCompare(mapping[bs])
}

/**
 * The box below the course ratings table that contains student comments and semester information.
 */
export const DetailsBox = forwardRef(({ course, instructor, type }, ref) => {
  const [data, setData] = useState(null)
  const [viewingRatings, setViewingRatings] = useState(true)
  const [selectedSemester, setSelectedSemester] = useState(null)
  const [semesterList, setSemesterList] = useState([])
  const [columns, setColumns] = useState([])
  const [filtered, setFiltered] = useState([])
  const [filterAll, setFilterAll] = useState('')

  useEffect(() => {
    if (instructor !== null && course !== null) {
      apiHistory(course, instructor).then(res => {
        const list = [
          ...new Set(
            Object.values(res.sections)
              .filter(a => a.comments)
              .sort((a, b) => compareSemesters(a.semester, b.semester))
              .map(a => a.semester)
          ),
        ]
        setData(res)
        setColumns(
          [
            {
              id: 'semester',
              width: 150,
              Header: 'Semester',
              accessor: 'semester',
              sortMethod: compareSemesters,
              show: true,
              required: true,
            },
            {
              id: 'name',
              width: 300,
              Header: 'Name',
              accessor: 'name',
              show: true,
              required: true,
              filterMethod: (filter, rows) => {
                if (filter.value === '') {
                  return true
                }
                return (
                  rows.name
                    .toLowerCase()
                    .includes(filter.value.toLowerCase()) ||
                  rows.semester
                    .toLowerCase()
                    .includes(filter.value.toLowerCase())
                )
              },
            },
            {
              id: 'forms',
              width: 150,
              Header: 'Forms',
              accessor: 'forms_returned',
              show: true,
              required: true,
              Cell: props =>
                typeof props.value === 'undefined' ? (
                  <center className="empty">N/A</center>
                ) : (
                  <center>
                    {props.value} / {props.original.forms_produced}{' '}
                    <small style={{ color: '#aaa', fontSize: '0.8em' }}>
                      (
                      {(
                        (props.value / props.original.forms_produced) *
                        100
                      ).toFixed(1)}
                      %)
                    </small>
                  </center>
                ),
            },
          ].concat(
            orderColumns(
              Object.keys(Object.values(res.sections)[0].ratings)
            ).map(info => ({
              id: info,
              width: 150,
              Header: getColumnName(info),
              accessor: info,
              Cell: props => (
                <center className={!props.value ? 'empty' : ''}>
                  {isNaN(props.value) ? 'N/A' : props.value.toFixed(2)}
                </center>
              ),
              show: true,
            }))
          )
        )
        setSemesterList(list)
        setSelectedSemester(
          list.length
            ? list.indexOf(selectedSemester) !== -1
              ? selectedSemester
              : list[0]
            : null
        )
      })
    }
  }, [course, instructor, selectedSemester])

  return (
    <div id="course-details" className="box" ref={ref}>
      {((type === 'course' && instructor) ||
        (type === 'instructor' && course)) &&
      !data ? (
        <div>Loading...</div>
      ) : !data ? (
        <div id="select-row">
          <div>
            <h3 id="select-row-text">
              {type === 'instructor'
                ? 'Select a course to see individual sections, comments, and more details.'
                : 'Select an instructor to see individual sections, comments, and more details.'}
            </h3>
            {type === 'course' ? (
              <object type="image/svg+xml" data="/static/image/prof.svg">
                <img alt="Professor Icon" src="/static/image/prof.png" />
              </object>
            ) : (
              <object
                type="image/svg+xml"
                id="select-course-icon"
                data="/static/image/books-and-bag.svg"
              >
                <img alt="Class Icon" src="/static/image/books-and-bag.png" />
              </object>
            )}
          </div>
        </div>
      ) : (
        <div id="course-details-wrapper">
          <h3>
            <Link
              style={{ color: '#b2b2b2', textDecoration: 'none' }}
              to={
                type === 'course'
                  ? `/instructor/${instructor}`
                  : `/course/${course}`
              }
            >
              {type === 'course' ? data.instructor.name : course}
            </Link>
          </h3>
          <div className="clearfix">
            <div className="btn-group">
              <button
                onClick={() => {
                  setViewingRatings(true)
                }}
                id="view_ratings"
                className={`btn btn-sm ${
                  viewingRatings ? 'btn-sub-primary' : 'btn-sub-secondary'
                }`}
              >
                Ratings
              </button>
              <button
                onClick={() => {
                  setViewingRatings(false)
                }}
                id="view_comments"
                className={`btn btn-sm ${
                  !viewingRatings ? 'btn-sub-primary' : 'btn-sub-secondary'
                }`}
              >
                Comments
              </button>
            </div>
            <ColumnSelector
              name="details"
              onSelect={cols => setColumns(cols)}
              columns={columns}
              buttonStyle="btn-sub"
            />
            {viewingRatings && (
              <div className="float-right">
                <label className="table-search">
                  <input
                    value={filterAll}
                    onChange={val =>
                      setFiltered([{ id: 'name', value: val.target.value }]) &&
                      setFilterAll(val.target.value)
                    }
                    type="search"
                    className="form-control form-control-sm"
                  />
                </label>
              </div>
            )}
          </div>
          {viewingRatings ? (
            <div id="course-details-data">
              <ScoreTable
                sorted={[{ id: 'semester', desc: false }]}
                filtered={filtered}
                data={Object.values(data.sections).map(i => ({
                  ...i.ratings,
                  semester: i.semester,
                  name: i.course_name,
                  forms_produced: i.forms_produced,
                  forms_returned: i.forms_returned,
                }))}
                columns={columns}
                noun="section"
              />
            </div>
          ) : (
            <div id="course-details-comments" className="clearfix mt-2">
              <div className="list">
                {semesterList.map((info, i) => (
                  <div
                    key={i}
                    onClick={() => {
                      setSelectedSemester(info)
                    }}
                    className={selectedSemester === info ? 'selected' : ''}
                  >
                    {info}
                  </div>
                ))}
              </div>
              <div className="comments">
                {Object.values(data.sections)
                  .filter(
                    info => info.semester === selectedSemester && info.comments
                  )
                  .map(info => info.comments)
                  .join(', ') ||
                  'This instructor does not have any comments for this course.'}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
})

export default DetailsBox
