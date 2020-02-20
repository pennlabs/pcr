import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import withLayout from './withLayout'
import { Popover } from '../components/common'
import { getColumnName } from '../utils/helpers'

class Cart extends Component {
  constructor(props) {
    super(props)

    this.state = {
      showChooseCols: false,
      isAverage: localStorage.getItem('meta-column-type') !== 'recent',
      courses: [],
      excludedCourses: [],
      boxValues: ['N/A', 'N/A', 'N/A', 'N/A'],
      boxLabels: [
        'rCourseQuality',
        'rInstructorQuality',
        'rDifficulty',
        'rWorkRequired',
      ],
    }

    // TODO: Move regeneration logic into Redux or React Context
    this.regenerateRatings = this.regenerateRatings.bind(this)
  }

  componentDidMount() {
    window.addEventListener('storage', this.regenerateRatings)
    this.regenerateRatings()
  }

  componentWillUnmount() {
    window.removeEventListener('storage', this.regenerateRatings)
  }

  regenerateRatings() {
    const courses = Object.keys(localStorage)
      .filter(k => !k.startsWith('meta-'))
      .map(k => {
        const out = JSON.parse(localStorage.getItem(k))
        if (typeof out !== 'object') {
          return null
        }
        const typeDict = {}
        if (typeof out.info !== 'undefined') {
          out.info.forEach(v => {
            typeDict[v.category] = v
          })
          out.info = typeDict
        }
        out.course = k
        return out
      })
      .filter(a => a !== null)

    this.setState(({ boxLabels, excludedCourses, isAverage }) => ({
      courses,
      boxValues: boxLabels.map(type => {
        const scoreList = courses
          .filter(
            a =>
              typeof a !== 'undefined' &&
              excludedCourses.indexOf(a.course) === -1
          )
          .map(
            a =>
              ((a.info || { type: null })[type] || {
                average: null,
                recent: null,
              })[isAverage ? 'average' : 'recent']
          )
          .filter(a => a !== null && !isNaN(a))
          .map(a => parseFloat(a))
        return scoreList.length
          ? (scoreList.reduce((a, b) => a + b) / scoreList.length).toFixed(1)
          : 'N/A'
      }),
    }))

    window.onCartUpdated()
  }

  render() {
    // TODO: Move these values into a constants file
    const checkboxValues = [
      'rCourseQuality',
      'rInstructorQuality',
      'rDifficulty',
      'rAmountLearned',
      'rWorkRequired',
      'rReadingsValue',
      'rCommAbility',
      'rInstructorAccess',
      'rStimulateInterest',
      'rTAQuality',
      'rRecommendMajor',
      'rRecommendNonMajor',
    ]
    const checkboxLabels = [
      'Course Quality',
      'Instructor Quality',
      'Difficulty',
      'Amount Learned',
      'Amount of Work',
      'Value of Readings',
      'Instructor Communication',
      'Instructor Accessibility',
      'Ability to Stimulate Interest',
      'TA Quality',
      'Recommend for Majors',
      'Recommend for Non-Majors',
    ]

    const propertyShortNames = {
      rCourseQuality: 'Course',
      rInstructorQuality: 'Instructor',
      rDifficulty: 'Difficulty',
      rAmountLearned: 'Learned',
      rWorkRequired: 'Workload',
      rReadingsValue: 'Reading',
      rCommAbility: 'Instr Comm',
      rInstructorAccess: 'Access',
      rStimulateInterest: 'Interest',
      rTAQuality: 'TA Quality',
      rRecommendMajor: 'Major',
      rRecommendNonMajor: 'Non-Major',
    }

    const {
      boxLabels,
      boxValues,
      courses,
      excludedCourses,
      showChooseCols,
      isAverage,
    } = this.state

    return (
      <center className="box" style={{ margin: '30px auto', maxWidth: 720 }}>
        <p className="courseCartHeader title">My Course Cart</p>
        <p className="courseCartDesc">
          The course cart is a feature for you to see all the relevant reviews
          for your selected courses at once with at-a-glance statistics. Search
          for courses to add them to your cart.
        </p>
        <div id="bannerScore">
          <div className="scoreboxrow courseCartRow">
            {boxLabels.map((a, i) => (
              <div
                key={i}
                className={`mb-2 scorebox ${
                  ['course', 'instructor', 'difficulty', 'workload'][i % 4]
                }`}
              >
                <p className="num">{boxValues[i]}</p>
                <p className="desc">{propertyShortNames[a]}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="clear" />
        <div className="fillerBox" />
        {showChooseCols && (
          <div className="box">
            <h3 style={{ fontSize: '1.5em' }}>Choose columns to display</h3>
            <div className="clearfix" style={{ textAlign: 'left' }}>
              {checkboxValues.map((a, i) => (
                <div style={{ width: '50%', display: 'inline-block' }} key={i}>
                  <input
                    type="checkbox"
                    onChange={e => {
                      const pos = boxLabels.indexOf(a)
                      if (pos === -1) {
                        this.setState(state => {
                          state.boxValues.push('N/A')
                          state.boxLabels.push(a)
                          return {
                            boxValues: state.boxValues,
                            boxLabels: state.boxLabels,
                          }
                        })
                      } else {
                        this.setState(state => {
                          state.boxValues.splice(pos, 1)
                          state.boxLabels.splice(pos, 1)
                          return {
                            boxValues: state.boxValues,
                            boxLabels: state.boxLabels,
                          }
                        })
                      }
                      this.regenerateRatings()
                    }}
                    checked={boxLabels.indexOf(a) !== -1}
                    value={a}
                    id={`checkbox_${a}`}
                    name={a}
                    className="mr-1"
                  />
                  <label htmlFor={`checkbox_${a}`}>{checkboxLabels[i]}</label>
                </div>
              ))}
            </div>
          </div>
        )}
        <button
          className="btn btn-primary mr-2"
          onClick={() =>
            this.setState(state => ({
              showChooseCols: !state.showChooseCols,
            }))
          }
        >
          Choose Categories
        </button>
        <div className="btn-group">
          <span
            className={`btn ${isAverage ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => {
              this.setState({ isAverage: true }, () =>
                localStorage.setItem('meta-column-type', 'average')
              )
              this.regenerateRatings()
            }}
          >
            Average
          </span>
          <span
            className={`btn ${isAverage ? 'btn-secondary' : 'btn-primary'}`}
            onClick={() => {
              this.setState({ isAverage: false }, () =>
                localStorage.setItem('meta-column-type', 'recent')
              )
              this.regenerateRatings()
            }}
          >
            Most Recent
          </span>
        </div>
        <div className="clear" />
        <div id="boxHelpTag">
          Click a course to exclude it from the average.
        </div>
        <div id="courseBox">
          {courses.map((a, i) => (
            <Popover
              key={i}
              button={
                <div
                  onClick={() => {
                    this.setState({
                      excludedCourses:
                        excludedCourses.indexOf(a.course) !== -1
                          ? excludedCourses.filter(b => b !== a.course)
                          : excludedCourses.concat([a.course]),
                    })
                    this.regenerateRatings()
                  }}
                  style={{ display: 'inline-block' }}
                  className={`courseInBox${
                    excludedCourses.indexOf(a.course) !== -1
                      ? ' courseInBoxGrayed'
                      : ''
                  }`}
                >
                  {a.course}
                  <Link to={`/course/${a.course}`}>
                    <i className="fa fa-link" />
                  </Link>
                  <i
                    className="fa fa-times"
                    onClick={() => {
                      localStorage.removeItem(a.course)
                      this.regenerateRatings()
                    }}
                  />
                </div>
              }
              hover
            >
              <b>{a.course}</b>
              <br />
              {a.instructor}
              <br />
              {Object.values(a.info)
                .sort((x, y) => x.category.localeCompare(y.category))
                .map((b, i) => (
                  <div key={i}>
                    {getColumnName(b.category)}{' '}
                    <span className="float-right ml-3">
                      {isAverage ? b.average : b.recent}
                    </span>
                  </div>
                ))}
            </Popover>
          ))}
        </div>
      </center>
    )
  }
}

export const CartPage = withLayout(Cart)
