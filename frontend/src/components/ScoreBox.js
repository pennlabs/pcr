import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import ScoreTable from './ScoreTable'
import ColumnSelector from './ColumnSelector'
import { compareSemesters } from './DetailsBox'
import { convertInstructorName } from './Tags'
import { CourseDetails, PopoverTitle } from './common'

import 'react-table/react-table.css'

export function getColumnName(key) {
  return key
    .substring(1)
    .split(/(?=[A-Z])/)
    .join(' ')
    .replace('T A', 'TA')
    .replace(/Recommend/g, 'Rec.')
}

const capitalize = str => str.replace(/(?:^|\s)\S/g, e => e.toUpperCase())

export function orderColumns(cols) {
  const colSet = new Set(cols)
  const fixedCols = [
    'latest_semester',
    'num_semesters',
    'rCourseQuality',
    'rInstructorQuality',
    'rDifficulty',
    'rAmountLearned',
  ].filter(a => colSet.has(a))
  const fixedColsSet = new Set(fixedCols)
  return fixedCols.concat(cols.filter(a => !fixedColsSet.has(a)).sort())
}

/*
 * Setting this to true colors all other cells depending on its value when compared to the selected row.
 */
const ENABLE_RELATIVE_COLORS = false

/**
 * The top right box of a review page with the table of numerical scores.
 */
class ScoreBox extends Component {
  constructor(props) {
    super(props)

    this.state = {
      data: null,
      columns: null,
      isAverage: localStorage.getItem('meta-column-type') !== 'recent',
      filtered: [],
      currentInstructors: {},
      currentCourses: {},
      filterAll: '',
      selected: null,
    }

    this.handleClick = this.handleClick.bind(this)
    this.updateLiveData = this.updateLiveData.bind(this)
    this.handleSelect = this.handleSelect.bind(this)
  }

  handleClick(val) {
    return () => {
      localStorage.setItem('meta-column-type', val ? 'average' : 'recent')
      this.setState({ isAverage: val })
      this.refs.table.resort()
    }
  }

  handleSelect(selected) {
    this.setState({ selected })
    return this.props.onSelect(selected)
  }

  updateLiveData() {
    const instructorTaught = {}
    const { data, liveData, type } = this.props
    if (type === 'course') {
      Object.values(data.instructors).forEach(a => {
        const key = convertInstructorName(a.name)
        if (a.most_recent_semester) {
          const parts = a.most_recent_semester.split(' ')
          instructorTaught[key] =
            parseInt(parts[1]) * 3 + { Spring: 0, Summer: 1, Fall: 2 }[parts[0]]
        } else {
          instructorTaught[key] = 0
        }
      })

      if (liveData) {
        const instructorsThisSemester = {}
        const { instructors = [], courses } = liveData
        instructors.forEach(a => {
          const data = {
            open: 0,
            all: 0,
            sections: [],
          }
          const key = convertInstructorName(a)
          Object.values(courses).forEach(cat => {
            const coursesByInstructor = cat
              .filter(
                a =>
                  a.instructors
                    .map(b => convertInstructorName(b.name))
                    .indexOf(key) !== -1
              )
              .filter(a => !a.is_cancelled)
            data.open += coursesByInstructor.filter(a => !a.is_closed).length
            data.all += coursesByInstructor.length
            data.sections = data.sections.concat(
              coursesByInstructor.map(a => a)
            )
          })
          instructorsThisSemester[key] = data
          instructorTaught[key] = Infinity
        })

        this.setState(state => ({
          currentInstructors: instructorTaught,
          data: state.data.map(a => ({
            ...a,
            star: instructorsThisSemester[convertInstructorName(a.name)],
          })),
        }))
      } else {
        this.setState(state => ({
          currentInstructors: instructorTaught,
          data: state.data.map(a => ({ ...a, star: null })),
        }))
      }
    } else if (type === 'instructor') {
      if (liveData) {
        const courses = {}
        Object.values(liveData.courses).forEach(a => {
          const key = `${a.course_department}-${a.course_number}`
          if (!(key in courses)) {
            courses[key] = []
          }
          courses[key].push(a)
        })
        this.setState({
          currentCourses: courses,
        })
      }
    }
  }

  componentDidUpdate(prevProps) {
    if (prevProps.liveData !== this.props.liveData) {
      this.updateLiveData()
    }
  }

  componentDidMount() {
    const { data: results, liveData, type } = this.props

    const columns = {}
    const isCourse = type === 'course'
    const isInstructor = type === 'instructor'
    const infoMap = isCourse ? results.instructors : results.courses

    const EXTRA_KEYS = ['latest_semester', 'num_semesters']
    const SEM_SORT_KEY = 'latest_semester'

    const data = Object.keys(infoMap).map(key => {
      const val = isCourse ? results.instructors[key] : results.courses[key]
      const output = {}
      Object.keys(val.average_reviews).forEach(col => {
        output[col] = {
          average: val.average_reviews[col].toFixed(2),
          recent: val.recent_reviews[col].toFixed(2),
        }
        columns[col] = true
      })
      if (isInstructor) {
        EXTRA_KEYS.forEach(col => {
          output[col] = val[col]
          columns[col] = true
        })
      }
      output.key = isCourse ? key : val.code
      output.name = val.name
      output.semester = val.most_recent_semester
      output.code = val.code
      return output
    })

    const cols = []

    if (isInstructor) {
      EXTRA_KEYS.forEach(colName =>
        cols.push({
          id: colName,
          Header: capitalize(colName.replace('_', ' ')),
          accessor: colName,
          sortMethod:
            SEM_SORT_KEY === colName
              ? compareSemesters
              : (a, b) => (a > b ? 1 : -1),
          Cell: props => {
            const classes = []
            const value = props.value ? props.value : 'N/A'

            if (!props.value) {
              classes.push('empty')
            }

            if (this.state.isAverage) {
              classes.push('cell_average')
            } else {
              classes.push('cell_recent')
            }
            return (
              <center>
                <span className={classes.join(' ')}>{value}</span>
              </center>
            )
          },
          width: 140,
          show: true,
        })
      )
    }

    orderColumns(Object.keys(columns))
      // Remove columns that don't start with r, as they are not RatingBit values and
      // shouldn't be generated by this logic
      .filter(key => key && key.charAt(0) === 'r')
      .forEach(key => {
        const header = getColumnName(key)
        cols.push({
          id: key,
          Header: header,
          accessor: key,
          sortMethod: (a, b) => {
            if (a && b) {
              a = this.state.isAverage ? a.average : a.recent
              b = this.state.isAverage ? b.average : b.recent
              return a > b ? 1 : -1
            }
            return a ? 1 : -1
          },
          Cell: props => {
            const classes = []
            const value = props.value
              ? this.state.isAverage
                ? props.value.average
                : props.value.recent
              : 'N/A'

            if (!props.value) {
              classes.push('empty')
            }

            if (this.state.isAverage) {
              classes.push('cell_average')
            } else {
              classes.push('cell_recent')
            }

            if (
              ENABLE_RELATIVE_COLORS &&
              this.state.selected in infoMap &&
              props.original.key !== this.state.selected
            ) {
              const other =
                infoMap[this.state.selected][
                  this.state.isAverage ? 'average_reviews' : 'recent_reviews'
                ][props.column.id]
              if (Math.abs(value - other) > 0.01) {
                if (value > other) {
                  classes.push('lower')
                } else {
                  classes.push('higher')
                }
              }
            }

            return (
              <center>
                <span className={classes.join(' ')}>{value}</span>
              </center>
            )
          },
          width: 140,
          show: true,
        })
      })

    cols.unshift({
      id: 'name',
      Header: isCourse ? 'Instructor' : 'Course',
      accessor: 'name',
      width: 270,
      show: true,
      required: true,
      Cell: props => (
        <span>
          {isCourse && (
            <Link
              to={`/instructor/${props.original.key}`}
              title={`Go to ${props.value}`}
              className="mr-1"
              style={{ color: 'rgb(102, 146, 161)' }}
            >
              <i className="instructor-link far fa-user" />
            </Link>
          )}
          {props.value}
          {props.original.star && liveData && (
            <PopoverTitle
              title={
                <span>
                  <b>{props.value}</b> is teaching during
                  <b>{liveData.term}</b> and
                  <b>{props.original.star.open}</b> out of
                  <b>{props.original.star.all}</b> section(s) are open.
                  <ul>
                    {props.original.star.sections
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
              <i
                className={`fa-star ml-1 ${
                  props.original.star.open ? 'fa' : 'far'
                }`}
              />
            </PopoverTitle>
          )}
          {isInstructor && !!this.state.currentCourses[props.original.code] && (
            <PopoverTitle
              title={
                <span>
                  <b>{results.name}</b> will teach
                  <b>{props.original.code.replace('-', ' ')}</b> in
                  <b>
                    {
                      this.state.currentCourses[props.original.code][0]
                        .term_normalized
                    }
                  </b>
                  .
                  <ul>
                    {this.state.currentCourses[props.original.code].map(
                      (data, i) => (
                        <CourseDetails key={i} data={data} />
                      )
                    )}
                  </ul>
                </span>
              }
            >
              <i
                className={`ml-1 fa-star ${
                  this.state.currentCourses[props.original.code].filter(
                    a => !a.is_closed && !a.is_cancelled
                  ).length
                    ? 'fa'
                    : 'far'
                }`}
              />
            </PopoverTitle>
          )}
        </span>
      ),
      sortMethod: (a, b) => {
        const aname = convertInstructorName(a)
        const bname = convertInstructorName(b)
        const hasStarA = this.state.currentInstructors[aname]
        const hasStarB = this.state.currentInstructors[bname]
        if (hasStarA && !hasStarB) {
          return -1
        }
        if (!hasStarA && hasStarB) {
          return 1
        }
        if (hasStarA !== hasStarB) {
          return hasStarB - hasStarA
        }
        return a.localeCompare(b)
      },
      filterMethod: (filter, rows) => {
        if (filter.value === '') {
          return true
        }
        return rows[filter.id]
          .toLowerCase()
          .includes(filter.value.toLowerCase())
      },
    })
    if (!isCourse) {
      cols.unshift({
        id: 'code',
        Header: 'Code',
        accessor: 'code',
        width: 100,
        show: true,
        required: true,
        Cell: props => (
          <center>
            <Link to={`/course/${props.value}`} title={`Go to ${props.value}`}>
              {props.value}
            </Link>
          </center>
        ),
      })
    }
    this.setState({ data, columns: cols })

    if (liveData) {
      this.updateLiveData()
    }
  }

  render() {
    const { data, columns, filterAll, filtered } = this.state
    const { type } = this.props
    const isCourse = type === 'course'

    if (!data) {
      return <h1>Loading Data...</h1>
    }

    return (
      <div className="box">
        <div className="clearfix">
          <div className="btn-group">
            <button
              onClick={this.handleClick(true)}
              className={`btn btn-sm ${
                this.state.isAverage ? 'btn-primary' : 'btn-secondary'
              }`}
            >
              Average
            </button>
            <button
              onClick={this.handleClick(false)}
              className={`btn btn-sm ${
                this.state.isAverage ? 'btn-secondary' : 'btn-primary'
              }`}
            >
              Most Recent
            </button>
          </div>
          <ColumnSelector
            name="score"
            type={type}
            columns={columns}
            onSelect={columns => this.setState({ columns })}
          />
          <div className="float-right">
            <label className="table-search">
              <input
                value={filterAll}
                onChange={val =>
                  this.setState({
                    filtered: [{ id: 'name', value: val.target.value }],
                    filterAll: val.target.value,
                  })
                }
                type="search"
                className="form-control form-control-sm"
              />
            </label>
          </div>
        </div>
        <ScoreTable
          multi={type === 'department'}
          sorted={[{ id: isCourse ? 'name' : 'code', desc: false }]}
          ref="table"
          filtered={filtered}
          data={data}
          columns={columns}
          onSelect={this.handleSelect}
          noun={isCourse ? 'instructor' : 'course'}
        />
      </div>
    )
  }
}

export default ScoreBox