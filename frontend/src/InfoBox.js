import React, { Component } from 'react';
import Tags from './Tags';
import ScoreboxRow from './ScoreboxRow'


class InfoBox extends Component {

  constructor(props) {

    super(props)

    this.state = {
      items: null,
      average_ratings: null,
      tag_data: null
    }
  }

  componentDidMount() {
    // "http://localhost:8000/api/display/instructor/6470-RAJIV-GANDHI?token=public"
    // "http://localhost:8000/api/display/course/CIS-121?token=public"
    // "http://localhost:8000/api/display/department/CIS?token=public"
    fetch("http://localhost:8000/api/display/department/CIS?token=public")
      .then(res => res.json())
      .then(
        (result) => {
          console.log('result')
          console.log(result)
          this.setState(state => ({
            items: result,
            average_ratings: result.average_ratings,
            recent_ratings: result.recent_ratings
          }))
        })

    fetch("http://localhost:8000/live/CIS-121")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState(state => ({
            tag_data: result
          }))
        })
  }

  render() {
    // console.log("hi")
    // console.log(window)
    var pageType = window.pageType // ["COURSES", "INSTRUCTOR", "DEPARTMENT"]
    console.log(window.pageType)
    // console.log("pagetype")
    // console.log(pageType)
    var pageIdentifier = window.pageIdentifier
    console.log(pageIdentifier)
    // console.log(pageIdentifier)
    // console.log(window)

    if (!this.state.items) {
      return (<h1>Loading data</h1>);
    }
    if (!this.state.tag_data) {
      return (<h1>Null tag data</h1>);
    }

    // do not show pages if course is not offered this semester or if page type is instructor
    var noTags = !this.state.tag_data.term // noTags is true if term is Null

    return (
        <div className="box">
          <div id="banner-info" data-type="course">
            { pageType === "course" &&
              <div className="course">
                <div className="title">{this.state.items.code}

                  <span className="float-right">
                    <span id="popup" className="courseCart btn btn-action" title="Add to Cart"><i className="fa fa-fw fa-cart-plus"></i></span>
                    <a target="_blank" title="Get Alerted" href="https://penncoursealert.com/?course=CIS-121&amp;source=pcr" className="btn btn-action"><i className="fas fa-fw fa-bell"></i></a>
                  </span>

                </div>

                <div className="crosslist"></div>

                <p className="subtitle">{this.state.items.name}</p>

                { !noTags &&
                  <Tags
                    term={this.state.tag_data.term}
                    credits={this.state.tag_data.credits}
                    />
                }
              </div>
            }

            { pageType === "instructor" &&
                <div className="instructor">
                  <div className="title">{this.state.items.name}</div>
                  <p className="desc">Email: <a href="mailto:rajiv@cis.upenn.edu">hard coded email</a></p>
                </div>
            }

            { pageType === "department" &&
              <div className="department">
                <div className="title">{this.state.items.name}</div>
                <p className="subtitle">{this.state.items.code}</p>
              </div>
            }

          </div>

          { pageType != "department" &&
            <div id="banner-score">
              <ScoreboxRow
                value="Average"
                instructor={this.state.average_ratings.rInstructorQuality}
                course={this.state.average_ratings.rCourseQuality}
                difficulty={this.state.average_ratings.rDifficulty}
                num_sections={this.state.items.num_sections}/>

              <ScoreboxRow
                value="Recent"
                instructor={this.state.recent_ratings.rInstructorQuality}
                course={this.state.recent_ratings.rCourseQuality}
                difficulty={this.state.recent_ratings.rDifficulty}
                num_sections={this.state.items.num_sections}/>
            </div>
          }

          // <link type="text/css" href="%PUBLIC_URL%/static/css/bootstrap.min.css" rel="stylesheet" />
          { pageType === "department" &&
            <div class="department-content">
              <div id="row-select-placeholder">
                  <object type="image/svg+xml" data="%PUBLIC_URL%/static/image/selectrow.svg">
                    <img src="%PUBLIC_URL%/static/image/selectrow.svg" />
                  </object>
                  <div id="row-select-text">Select a few rows to begin comparing courses.</div>
              </div>
              <div id="row-select-chart-container">
                  <canvas id="row-select-chart"></canvas>
                  <button id="chart-clear" class="btn btn-action">Clear Chart</button>
              </div>
            </div>
          }

          { pageType === "course" &&
            <p className="desc">{this.state.items.description}</p>
          }

        </div>
    );
  }
}

export default InfoBox;
