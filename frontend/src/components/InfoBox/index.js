import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { Bar } from 'react-chartjs-2'
import reactStringReplace from 'react-string-replace'

import { Popover } from '../common'
import Tags from './InfoBoxTags'
import Ratings from './InfoBoxRatings'
import { apiContact } from '../../utils/api'

/**
 * Information box on the left most side, containing scores and descriptions
 * of course or professor.
 *
 */

class InfoBox extends Component {
  constructor(props) {
    super(props)
    const {
      data: { code },
    } = props
    this.state = {
      contact: null,
      inCourseCart: Boolean(localStorage.getItem(code)),
    }

    this.handleAdd = this.handleAdd.bind(this)
    this.handleAddAverage = this.handleAddAverage.bind(this)
    this.handleAddInstructor = this.handleAddInstructor.bind(this)
    this.handleRemove = this.handleRemove.bind(this)
    this.getChartData = this.getChartData.bind(this)
  }

  componentDidMount() {
    const { type, data } = this.props
    if (type === 'instructor') {
      apiContact(data.name).then(res => this.setState({ contact: res }))
    }
  }

  getChartData() {
    return {
      labels: Object.values(this.props.selected_courses).map(
        a => a.original.code
      ),
      datasets: [
        'rCourseQuality',
        'rInstructorQuality',
        'rDifficulty',
        'rWorkRequired',
      ].map((a, i) => ({
        label: a
          .substring(1)
          .split(/(?=[A-Z])/)
          .join(' '),
        data: Object.values(this.props.selected_courses).map(
          b => (b.original[a] || { average: 0 }).average
        ),
        backgroundColor: ['#6274f1', '#ffc107', '#76bf96', '#df5d56'][i],
      })),
    }
  }

  handleAddAverage() {
    const {
      data: { code: course, average_ratings: average, recent_ratings: recent },
    } = this.props
    const info = Object.keys(average).map(category => ({
      category,
      average: average[category],
      recent: recent[category],
    }))
    localStorage.setItem(
      course,
      JSON.stringify({
        version: 1,
        course,
        instructor: 'Average Professor',
        info,
      })
    )
  }

  handleAddInstructor(key) {
    const {
      instructors: { [key]: content = {} },
      code: course,
    } = this.props.data
    const {
      name: instructor,
      average_reviews: average,
      recent_reviews: recent,
    } = content
    const info = Object.keys(average).map(category => ({
      category,
      average: average[category],
      recent: recent[category],
    }))
    localStorage.setItem(
      course,
      JSON.stringify({
        version: 1,
        course,
        instructor,
        info,
      })
    )
  }

  handleAdd(key) {
    return () => {
      if (key === 'average') this.handleAddAverage()
      else this.handleAddInstructor(key)
      if (window.onCartUpdated) window.onCartUpdated()
      this.setState({ inCourseCart: true })
    }
  }

  handleRemove() {
    localStorage.removeItem(this.props.data.code)
    this.setState({ inCourseCart: false })
    window.onCartUpdated()
  }

  render() {
    const {
      type: pageType,
      data,
      liveData,
      selected_courses: selectedCourses,
    } = this.props

    if (!data) {
      return <h1>Loading data...</h1>
    }

    const {
      instructors,
      code,
      description,
      aliases,
      name,
      notes,
      num_sections: numSections,
      num_sections_recent: numSectionsRecent,
      average_ratings: averageRatings = {},
      recent_ratings: recentRatings = {},
    } = data

    const {
      rInstructorQuality: avgInstructorQuality,
      rCourseQuality: avgCourseQuality,
      rDifficulty: avgDifficulty,
    } = averageRatings

    const {
      rInstructorQuality: recentInstructorQuality,
      rCourseQuality: recentCourseQuality,
      rDifficulty: recentDifficulty,
    } = recentRatings

    return (
      <div className="box">
        <div id="banner-info" data-type="course">
          {pageType === 'course' && (
            <div className="course">
              <div className="title">
                {(code || '').replace('-', ' ')}

                <span className="float-right">
                  {this.state.inCourseCart ? (
                    <span
                      onClick={this.handleRemove}
                      className="courseCart btn btn-action"
                      title="Remove from Cart"
                    >
                      <i className="fa fa-fw fa-trash-alt" />
                    </span>
                  ) : (
                    <Popover
                      button={
                        <span
                          className="courseCart btn btn-action"
                          title="Add to Cart"
                        >
                          <i className="fa fa-fw fa-cart-plus" />
                        </span>
                      }
                    >
                      <div className="popover-title">Add to Cart</div>
                      <div
                        className="popover-content"
                        style={{ maxHeight: 400, overflowY: 'auto' }}
                      >
                        <div id="divList">
                          <ul className="professorList">
                            <li>
                              <button onClick={this.handleAdd('average')}>
                                Average Professor
                              </button>
                            </li>
                            {Object.keys(instructors)
                              .sort((a, b) =>
                                instructors[a].name.localeCompare(
                                  instructors[b].name
                                )
                              )
                              .map((key, i) => (
                                <li key={i}>
                                  <button onClick={this.handleAdd(key)}>
                                    {instructors[key].name}
                                  </button>
                                </li>
                              ))}
                          </ul>
                        </div>
                      </div>
                    </Popover>
                  )}{' '}
                  <a
                    target="_blank"
                    rel="noopener noreferrer"
                    title="Get Alerted"
                    href={`https://penncoursealert.com/?course=${this.props.code}&source=pcr`}
                    className="btn btn-action"
                  >
                    <i className="fas fa-fw fa-bell" />
                  </a>
                </span>
              </div>
              {Boolean(aliases.length) && (
                <div className="crosslist">
                  Also:{' '}
                  {aliases.map((cls, i) => [
                    i > 0 && ', ',
                    <Link key={i} to={`/course/${cls}`}>
                      {cls}
                    </Link>,
                  ])}
                </div>
              )}
              <p className="subtitle">{name}</p>
              {notes.map((note, i) => (
                <div key={i} className="note">
                  <i className="fa fa-thumbtack" /> {note}
                </div>
              ))}
              {pageType === 'course' && liveData && (
                <Tags
                  {...liveData}
                  data={data}
                  existingInstructors={Object.values(instructors).map(
                    a => a.name
                  )}
                />
              )}
            </div>
          )}

          {pageType === 'instructor' && (
            <div className="instructor">
              <div className="title">{name}</div>
              {this.state.contact && (
                <div>
                  <p className="desc">
                    Email:
                    <a href={`mailto:${this.state.contact.email}`}>
                      {this.state.contact.email.toLowerCase()}
                    </a>
                  </p>
                </div>
              )}
              {notes.map((note, i) => (
                <div key={i} className="note">
                  <i className="fa fa-thumbtack" /> {note}
                </div>
              ))}
            </div>
          )}

          {pageType === 'department' && (
            <div className="department">
              <div className="title">{name}</div>
              <p className="subtitle">{code}</p>
            </div>
          )}
        </div>

        {pageType !== 'department' && (
          <div id="banner-score">
            <Ratings
              value="Average"
              instructor={avgInstructorQuality}
              course={avgCourseQuality}
              difficulty={avgDifficulty}
              num_sections={numSections}
            />

            <Ratings
              value="Recent"
              instructor={recentInstructorQuality}
              course={recentCourseQuality}
              difficulty={recentDifficulty}
              num_sections={numSectionsRecent}
            />
          </div>
        )}

        {pageType === 'department' && (
          <div className="department-content">
            {selectedCourses && Object.keys(selectedCourses).length ? (
              <div id="row-select-chart-container">
                <Bar
                  data={this.getChartData()}
                  options={{
                    scales: {
                      yAxes: [
                        {
                          display: true,
                          ticks: {
                            min: 0,
                            max: 4,
                          },
                        },
                      ],
                    },
                  }}
                />
              </div>
            ) : (
              <div id="row-select-placeholder">
                <object type="image/svg+xml" data="/static/image/selectrow.svg">
                  <img alt="Select Row" src="/static/image/selectrow.svg" />
                </object>
                <div id="row-select-text">
                  Select a few rows to begin comparing courses.
                </div>
              </div>
            )}
          </div>
        )}

        {pageType === 'course' && (
          <p className="desc">
            {reactStringReplace(
              description,
              /([A-Z]{2,4}[ -]\d{3})/g,
              (m, i) => (
                <Link to={`/course/${m.replace(' ', '-')}`} key={i}>
                  {m}
                </Link>
              )
            )}
          </p>
        )}
      </div>
    )
  }
}

export default InfoBox
