import React, { Component } from 'react'
import Cookies from 'universal-cookie'
import InfoBox from './InfoBox'
import ErrorBox from './ErrorBox'
import ScoreBox from './ScoreBox'
import NavBar from './NavBar'
import DetailsBox from './DetailsBox'
import SearchBar from './SearchBar'
import Footer from './Footer'
import { apiReviewData, apiLive, apiLiveInstructor } from './api'

/**
 * Enable or disable the Penn Labs recruitment banner.
 */
const SHOW_RECRUITMENT_BANNER = false

/**
 * Represents a course, instructor, or department review page.
 */
class ReviewPage extends Component {
  constructor(props) {
    super(props)
    this.myRef = React.createRef()

    this.cookies = new Cookies()

    this.state = {
      type: this.props.match.params.type,
      code: this.props.match.params.code,
      data: null,
      error: null,
      error_detail: null,
      rowCode: null,
      liveData: null,
      selected_courses: null,
      showBanner:
        SHOW_RECRUITMENT_BANNER && !this.cookies.get('hide_pcr_banner'),
    }

    this.navigateToPage = this.navigateToPage.bind(this)
    this.getReviewData = this.getReviewData.bind(this)
    this.showRowHistory = this.showRowHistory.bind(this)
    this.showDepartmentGraph = this.showDepartmentGraph.bind(this)
  }

  componentDidMount() {
    this.getReviewData()
  }

  componentDidUpdate(prevProps) {
    if (
      this.props.match.params.type !== prevProps.match.params.type ||
      this.props.match.params.code !== prevProps.match.params.code
    ) {
      // TODO: Switch to functional component and use useEffect(() => {...}, [])
      // eslint-disable-next-line react/no-did-update-set-state
      this.setState(
        {
          type: this.props.match.params.type,
          code: this.props.match.params.code,
          data: null,
          rowCode: null,
          error: null,
        },
        this.getReviewData
      )
    }
  }

  getPageInfo() {
    const pageInfo = window.location.pathname.substring(1).split('/')

    if (['course', 'instructor', 'department'].indexOf(pageInfo[0]) === -1) {
      pageInfo[0] = null
      pageInfo[1] = null
    }

    return pageInfo
  }

  getReviewData() {
    const { type, code } = this.state
    if (type && code) {
      apiReviewData(type, code)
        .then(result => {
          if (result.error) {
            this.setState({
              error: result.error,
              error_detail: result.detail,
            })
          } else {
            this.setState({
              data: result,
            })
            if (this.state.type === 'instructor') {
              apiLiveInstructor(result.name.replace(/[^A-Za-z0-9 ]/g, '')).then(
                data => {
                  this.setState(state => ({
                    liveData: state.data.name === result.name ? data : null,
                  }))
                }
              )
            }
          }
        })
        .catch(() => {
          this.setState({
            error:
              'Could not retrieve review information at this time. Please try again later!',
          })
        })
    }

    if (type === 'course') {
      apiLive(code)
        .then(result => {
          this.setState({ liveData: result })
        })
        .catch(() => {
          this.setState({ liveData: null })
        })
    } else {
      this.setState({ liveData: null })
    }
  }

  navigateToPage(value) {
    if (!value) {
      return
    }
    this.props.history.push(value)
  }

  showRowHistory(rowCode) {
    this.setState({ rowCode }, () => {
      if (rowCode)
        window.scrollTo({
          behavior: 'smooth',
          top: this.myRef.current.offsetTop,
        })
    })
  }

  showDepartmentGraph(val) {
    this.setState({
      selected_courses: val,
    })
  }

  static getDerivedStateFromError() {
    return { error: 'An unknown error occured.' }
  }

  render() {
    if (this.state.error) {
      return (
        <div>
          <NavBar />
          <ErrorBox detail={this.state.error_detail}>
            {this.state.error}
          </ErrorBox>
          <Footer />
        </div>
      )
    }

    if (!this.state.code) {
      return (
        <div id="content" className="row">
          {this.state.showBanner && (
            <div id="banner">
              <span role="img" aria-label="Party Popper Emoji">
                🎉
              </span>{' '}
              <b>Want to build impactful products like Penn Course Review?</b>{' '}
              Join Penn Labs this spring! Apply{' '}
              <a
                href="https://pennlabs.org/apply"
                target="_blank"
                rel="noopener noreferrer"
              >
                here
              </a>
              !{' '}
              <span role="img" aria-label="Party Popper Emoji">
                🎉
              </span>
              <span
                className="close"
                onClick={e => {
                  this.setState({ showBanner: false })
                  this.cookies.set('hide_pcr_banner', true, {
                    expires: new Date(Date.now() + 12096e5),
                  })
                  e.preventDefault()
                }}
              >
                <i className="fa fa-times" />
              </span>
            </div>
          )}
          <div className="col-md-12">
            <div id="title">
              <img src="/static/image/logo.png" alt="Penn Course Review" />{' '}
              <span className="title-text">Penn Course Review</span>
            </div>
          </div>
          <SearchBar isTitle />
          <Footer style={{ marginTop: 150 }} />
        </div>
      )
    }

    const {
      code,
      data,
      rowCode,
      liveData,
      selected_courses: selectedCourses,
      type,
    } = this.state

    const handleSelect = {
      instructor: this.showRowHistory,
      course: this.showRowHistory,
      department: this.showDepartmentGraph,
    }[type]

    return (
      <div>
        <NavBar />
        {this.state.data ? (
          <div id="content" className="row">
            <div className="col-sm-12 col-md-4 sidebar-col box-wrapper">
              <InfoBox
                type={type}
                code={code}
                data={data}
                liveData={liveData}
                selected_courses={selectedCourses}
              />
            </div>
            <div className="col-sm-12 col-md-8 main-col">
              <ScoreBox
                data={data}
                type={type}
                liveData={liveData}
                onSelect={handleSelect}
              />
              {type === 'course' && (
                <DetailsBox
                  type={type}
                  course={code}
                  instructor={rowCode}
                  ref={this.myRef}
                />
              )}
              {type === 'instructor' && (
                <DetailsBox
                  type={type}
                  course={rowCode}
                  instructor={code}
                  ref={this.myRef}
                />
              )}
            </div>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: 45 }}>
            <i
              className="fa fa-spin fa-cog fa-fw"
              style={{ fontSize: '150px', color: '#aaa' }}
            />
            <h1 style={{ fontSize: '2em', marginTop: 15 }}>
              Loading {code}
              ...
            </h1>
          </div>
        )}
        <Footer />
      </div>
    )
  }
}

export default ReviewPage
