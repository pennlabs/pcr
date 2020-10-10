import React, { Component } from 'react'
import Cookies from 'universal-cookie'
import InfoBox from '../components/InfoBox'
import ScoreBox from '../components/ScoreBox'
import Navbar from '../components/Navbar'
import DetailsBox from '../components/DetailsBox'
import SearchBar from '../components/SearchBar'
import Footer from '../components/Footer'
import { ErrorBox } from '../components/common'
import { apiReviewData, apiLive, apiLiveInstructor } from '../utils/api'

/**
 * Enable or disable different banners.
 */
const SHOW_RECRUITMENT_BANNER = false
const SHOW_SURVEY_BANNER = true
const SURVEY_LINK = 'https://airtable.com/shrTGx0iFbAYDfdES'

const RecruitmentBanner = ({ hideBanner }) => (
  <div id="banner">
    <span role="img" aria-label="Party Popper Emoji">
      🎉
    </span>{' '}
    <b>Want to build impactful products like Penn Course Review?</b> Join Penn
    Labs this fall! Apply{' '}
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
        hideBanner()
        e.preventDefault()
      }}
    >
      <i className="fa fa-times" />
    </span>
  </div>
)

const SurveyBanner = ({ hideSurvey }) => (
  <div id="banner" style={{ backgroundColor: '#84B8BA' }}>
    <span
      className="close"
      onClick={e => {
        hideSurvey()
        e.preventDefault()
      }}
    >
      <i className="fa fa-times" />
    </span>
    <h3>
      {' '}
      <span role="img" aria-label="Waving Hand Emoji">
        👋
      </span>{' '}
      <b>Hello there!</b> Do you have a moment?
    </h3>
    How would you describe the courses you've taken? Fill out this short survey to help us improve Penn Course Review{' '}
    <a href={SURVEY_LINK} target="_blank" rel="noopener noreferrer">
      here
    </a>
    !{' '}
  </div>
)

/**
 * Represents a course, instructor, or department review page.
 */
export class ReviewPage extends Component {
  constructor(props) {
    super(props)
    this.tableRef = React.createRef()
    this.cookies = new Cookies()
    this.state = {
      type: this.props.match.params.type,
      code: this.props.match.params.code,
      data: null,
      error: null,
      error_detail: null,
      rowCode: null,
      liveData: null,
      selectedCourses: {},
      isAverage: localStorage.getItem('meta-column-type') !== 'recent',
      showBanner:
        SHOW_RECRUITMENT_BANNER && !this.cookies.get('hide_pcr_banner'),
      showSurvey: SHOW_SURVEY_BANNER && !this.cookies.get('hide_survey_banner'),
    }

    this.navigateToPage = this.navigateToPage.bind(this)
    this.getReviewData = this.getReviewData.bind(this)
    this.setIsAverage = this.setIsAverage.bind(this)
    this.showRowHistory = this.showRowHistory.bind(this)
    this.showDepartmentGraph = this.showDepartmentGraph.bind(this)
    this.hideBanner = this.hideBanner.bind(this)
    this.hideSurvey = this.hideSurvey.bind(this)
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

  setIsAverage(isAverage) {
    this.setState({ isAverage }, () =>
      localStorage.setItem('meta-column-type', isAverage ? 'average' : 'recent')
    )
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
        .then(data => {
          const { error, detail, name } = data
          if (error) {
            this.setState({
              error,
              error_detail: detail,
            })
          } else {
            this.setState({ data }, () => {
              if (type === 'instructor')
                apiLiveInstructor(
                  name.replace(/[^A-Za-z0-9 ]/g, '')
                ).then(liveData => this.setState({ liveData }))
            })
          }
        })
        .catch(() =>
          this.setState({
            error:
              'Could not retrieve review information at this time. Please try again later!',
          })
        )
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

  showRowHistory(nextCode) {
    const { rowCode } = this.state
    if (nextCode === rowCode) {
      this.setState({ rowCode: null })
      return
    }
    this.setState({ rowCode: nextCode }, () => {
      if (nextCode) {
        window.scrollTo({
          behavior: 'smooth',
          top: this.tableRef.current.offsetTop,
        })
      }
    })
  }

  showDepartmentGraph(selectedCourses) {
    this.setState({ selectedCourses })
  }

  hideBanner() {
    this.setState({ showBanner: false })
    this.cookies.set('hide_pcr_banner', true, {
      expires: new Date(Date.now() + 12096e5),
    })
  }

  hideSurvey() {
    this.setState({ showSurvey: false })
    this.cookies.set('hide_survey_banner', true, {
      expires: new Date(Date.now() + 12096e5),
    })
  }

  static getDerivedStateFromError() {
    return { error: 'An unknown error occured.' }
  }

  render() {
    if (this.state.error) {
      return (
        <div>
          <Navbar />
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
            <RecruitmentBanner hideBanner={this.hideBanner} />
          )}
          {this.state.showSurvey && (
            <SurveyBanner hideSurvey={this.hideSurvey} />
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
      isAverage,
      selectedCourses,
      type,
    } = this.state

    const handleSelect = {
      instructor: this.showRowHistory,
      course: this.showRowHistory,
      department: this.showDepartmentGraph,
    }[type]

    return (
      <div>
        <Navbar />
        {this.state.data ? (
          <div id="content" className="row">
            <div className="col-sm-12 col-md-4 sidebar-col box-wrapper">
              <InfoBox
                type={type}
                code={code}
                data={data}
                liveData={liveData}
                selectedCourses={selectedCourses}
              />
            </div>
            <div className="col-sm-12 col-md-8 main-col">
              <ScoreBox
                data={data}
                type={type}
                liveData={liveData}
                onSelect={handleSelect}
                isAverage={isAverage}
                setIsAverage={this.setIsAverage}
              />
              {type === 'course' && (
                <DetailsBox
                  type={type}
                  course={code}
                  instructor={rowCode}
                  ref={this.tableRef}
                />
              )}
              {type === 'instructor' && (
                <DetailsBox
                  type={type}
                  course={rowCode}
                  instructor={code}
                  ref={this.tableRef}
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
