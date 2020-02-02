import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { Bar } from 'react-chartjs-2'
import reactStringReplace from 'react-string-replace'

import Tags from './Tags'
import ScoreboxRow from './ScoreboxRow'
import Popover from './Popover'
import { api_contact } from './api'

/**
 * Information box on the left most side, containing scores and descriptions
 * of course or professor.
 *
 */

class InfoBox extends Component {
  constructor(props) {
    super(props)

    this.state = {
      contact: null,
      inCourseCart: !!localStorage.getItem(this.props.data.code),
    }

    this.handleAdd = this.handleAdd.bind(this)
    this.handleRemove = this.handleRemove.bind(this)
    this.getChartData = this.getChartData.bind(this)
  }

  componentDidMount() {
    const { type, data } = this.props
    if (type === 'instructor') {
      api_contact(data.name).then(res => this.setState({ contact: res }))
    }
  }

  getChartData() {
    return {
      labels: Object.values(this.props.selected_courses).map(
        a => a.original.code,
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
          b => (b.original[a] || { average: 0 }).average,
        ),
        backgroundColor: ['#6274f1', '#ffc107', '#76bf96', '#df5d56'][i],
      })),
    }
  }

  handleAdd(key) {
    return () => {
      let content
      if (key === 'average') {
        const average_reviews = {}
        const recent_reviews = {}
        Object.values(this.props.data.instructors).forEach(i => {
          Object.keys(i.recent_reviews).forEach(j => {
            if (!(j in recent_reviews)) {
              recent_reviews[j] = []
            }
            recent_reviews[j].push(i.recent_reviews[j])
          })
          Object.keys(i.average_reviews).forEach(j => {
            if (!(j in average_reviews)) {
              average_reviews[j] = []
            }
            average_reviews[j].push(i.average_reviews[j])
          })
        })
        Object.keys(average_reviews).forEach(i => {
          average_reviews[i] = (
            average_reviews[i].reduce((a, b) => a + b) /
            average_reviews[i].length
          ).toFixed(2)
        })
        Object.keys(recent_reviews).forEach(i => {
          recent_reviews[i] = (
            recent_reviews[i].reduce((a, b) => a + b) / recent_reviews[i].length
          ).toFixed(2)
        })
        content = {
          name: 'Average Professor',
          average_reviews,
          recent_reviews,
        }
      } else {
        content = this.props.data.instructors[key]
      }
      localStorage.setItem(
        this.props.data.code,
        JSON.stringify({
          version: 1,
          course: this.props.data.code,
          instructor: content.name,
          info: Object.keys(content.average_reviews).map(a => ({
            category: a,
            average: content.average_reviews[a],
            recent: content.recent_reviews[a],
          })),
        }),
      )
      this.setState({ inCourseCart: true })
      window.onCartUpdated()
    }
  }

  handleRemove() {
    localStorage.removeItem(this.props.data.code)
    this.setState({ inCourseCart: false })
    window.onCartUpdated()
  }

  render() {
    const pageType = this.props.type
    const { instructors } = this.props.data

    if (!this.props.data) {
      return <h1>Loading data...</h1>
    }

    return (
      <div className='box'>
        <div id='banner-info' data-type='course'>
          {pageType === 'course' && (
            <div className='course'>
              <div className='title'>
                {(this.props.data.code || '').replace('-', ' ')}

                <span className='float-right'>
                  {this.state.inCourseCart ? (
                    <span
                      onClick={this.handleRemove}
                      className='courseCart btn btn-action'
                      title='Remove from Cart'
                    >
                      <i className='fa fa-fw fa-trash-alt' />
                    </span>
                  ) : (
                    <Popover
                      button={
                        <span
                          className='courseCart btn btn-action'
                          title='Add to Cart'
                        >
                          <i className='fa fa-fw fa-cart-plus' />
                        </span>
                      }
                    >
                      <div className='popover-title'>Add to Cart</div>
                      <div
                        className='popover-content'
                        style={{ maxHeight: 400, overflowY: 'auto' }}
                      >
                        <div id='divList'>
                          <ul className='professorList'>
                            <li>
                              <button onClick={this.handleAdd('average')}>
                                Average Professor
                              </button>
                            </li>
                            {Object.keys(instructors)
                              .sort((a, b) =>
                                instructors[a].name.localeCompare(
                                  instructors[b].name,
                                ),
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
                    target='_blank'
                    rel='noopener noreferrer'
                    title='Get Alerted'
                    href={`https://penncoursealert.com/?course=${this.props.code}&source=pcr`}
                    className='btn btn-action'
                  >
                    <i className='fas fa-fw fa-bell' />
                  </a>
                </span>
              </div>

              {!!this.props.data.aliases.length && (
                <div className='crosslist'>
                  Also:
                  {this.props.data.aliases.map((cls, i) => [
                    i > 0 && ', ',
                    <Link key={i} to={`/course/${cls}`}>
                      {cls}
                    </Link>,
                  ])}
                </div>
              )}

              <p className='subtitle'>{this.props.data.name}</p>

              {this.props.data.notes.map((note, i) => (
                <div key={i} className='note'>
                  <i className='fa fa-thumbtack' /> {note}
                </div>
              ))}

              {this.props.type === 'course' && this.props.live_data && (
                <Tags
                  {...this.props.live_data}
                  data={this.props.data}
                  existing_instructors={Object.values(
                    this.props.data.instructors,
                  ).map(a => a.name)}
                />
              )}
            </div>
          )}

          {pageType === 'instructor' && (
            <div className='instructor'>
              <div className='title'>{this.props.data.name}</div>
              {this.state.contact && (
                <div>
                  <p className='desc'>
                    Email:
                    <a href={`mailto:${this.state.contact.email}`}>
                      {this.state.contact.email.toLowerCase()}
                    </a>
                  </p>
                </div>
              )}
              {this.props.data.notes.map((note, i) => (
                <div key={i} className='note'>
                  <i className='fa fa-thumbtack' /> {note}
                </div>
              ))}
            </div>
          )}

          {pageType === 'department' && (
            <div className='department'>
              <div className='title'>{this.props.data.name}</div>
              <p className='subtitle'>{this.props.data.code}</p>
            </div>
          )}
        </div>

        {pageType !== 'department' && (
          <div id='banner-score'>
            <ScoreboxRow
              value='Average'
              instructor={this.props.data.average_ratings.rInstructorQuality}
              course={this.props.data.average_ratings.rCourseQuality}
              difficulty={this.props.data.average_ratings.rDifficulty}
              num_sections={this.props.data.num_sections}
            />

            <ScoreboxRow
              value='Recent'
              instructor={this.props.data.recent_ratings.rInstructorQuality}
              course={this.props.data.recent_ratings.rCourseQuality}
              difficulty={this.props.data.recent_ratings.rDifficulty}
              num_sections={this.props.data.num_sections_recent}
            />
          </div>
        )}

        {pageType === 'department' && (
          <div className='department-content'>
            {this.props.selected_courses &&
            Object.keys(this.props.selected_courses).length ? (
              <div id='row-select-chart-container'>
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
                <div id='row-select-placeholder'>
                  <object type='image/svg+xml' data='/static/image/selectrow.svg'>
                    <img alt='Select Row' src='/static/image/selectrow.svg' />
                  </object>
                  <div id='row-select-text'>
                  Select a few rows to begin comparing courses.
                  </div>
                </div>
              )}
          </div>
        )}

        {pageType === 'course' && (
          <p className='desc'>
            {reactStringReplace(
              this.props.data.description,
              /([A-Z]{2,4}[ -]\d{3})/g,
              (m, i) => (
                <Link to={`/course/${m.replace(' ', '-')}`} key={i}>
                  {m}
                </Link>
              ),
            )}
          </p>
        )}
      </div>
    )
  }
}

export default InfoBox
