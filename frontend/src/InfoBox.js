import React, { Component } from 'react';
import Tags from './Tags';
import ScoreboxRow from './ScoreboxRow';
import { api_contact } from './api';


class InfoBox extends Component {

  constructor(props) {
    super(props);

    this.state = {
      items: this.props.data,
      average_ratings: this.props.data.average_ratings,
      recent_ratings: this.props.data.recent_ratings,
      contact: null
    };
  }

  componentDidMount() {
    if (this.props.type === "instructor") {
        api_contact(this.props.data.name).then((res) => {
            this.setState({
                contact: res
            });
        });
    }
  }

  render() {
    const pageType = this.props.type;

    if (!this.state.items) {
        return <h1>Loading data...</h1>;
    }

    return (
        <div className="box">
          <div id="banner-info" data-type="course">
            { pageType === "course" &&
              <div className="course">
                <div className="title">{(this.state.items.code || "").replace('-', ' ')}

                  <span className="float-right">
                    <span id="popup" className="courseCart btn btn-action" title="Add to Cart"><i className="fa fa-fw fa-cart-plus"></i></span>{' '}
                    <a target="_blank" rel="noopener noreferrer" title="Get Alerted" href={"https://penncoursealert.com/?course=" + this.props.code + "&source=pcr"} className="btn btn-action"><i className="fas fa-fw fa-bell"></i></a>
                  </span>

                </div>

                {this.state.items.aliases && <div className="crosslist">(Also: {this.state.items.aliases.map((cls, i) => <span>{i > 0 && ", "}<a key={i} href={"/course/" + cls}>{cls}</a></span>)})</div>}

                <p className="subtitle">{this.state.items.name}</p>

                { (this.props.live_data && this.props.live_data.term) &&
                  <Tags {...this.props.live_data} existing_instructors={Object.values(this.state.items.instructors).map((a) => a.name)} />
                }
              </div>
            }

            { pageType === "instructor" &&
                <div className="instructor">
                  <div className="title">{this.state.items.name}</div>
                  {this.state.contact &&
                      <div>
                        <p className="desc">Email: <a href={"mailto:" + this.state.contact.email}>{this.state.contact.email}</a></p>
                      </div>
                  }
                </div>
            }

            { pageType === "department" &&
              <div className="department">
                <div className="title">{this.state.items.name}</div>
                <p className="subtitle">{this.state.items.code}</p>
              </div>
            }

          </div>

          { pageType !== "department" &&
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

          { pageType === "department" &&
            <div className="department-content">
              <div id="row-select-placeholder">
                  <object type="image/svg+xml" data="/static/image/selectrow.svg">
                    <img alt="Select Row" src="/static/image/selectrow.svg" />
                  </object>
                  <div id="row-select-text">Select a few rows to begin comparing courses.</div>
              </div>
              <div id="row-select-chart-container">
                  <canvas id="row-select-chart"></canvas>
                  <button id="chart-clear" className="btn btn-action">Clear Chart</button>
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
