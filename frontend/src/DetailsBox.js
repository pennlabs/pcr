import React, { Component } from 'react';
import ReactTable from 'react-table';
import { api_history } from './api';

class DetailsBox extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            viewingRatings: true,
            selectedSemester: null
        };
    }

    componentDidUpdate(prevProps) {
        if (prevProps.instructor !== this.props.instructor || prevProps.course !== this.props.course) {
            api_history(this.props.course, this.props.instructor).then((res) => {
                this.setState({
                    data: res
                });
            });
        }
    }

    render() {
        function compareSemesters(a, b) {
            const ay = parseInt(a.semester.split(" ")[1]);
            const by = parseInt(b.semester.split(" ")[1]);

            if (ay !== by) {
                return by - ay;
            }

            return a.semester.localeCompare(b.semester);
        }

        // TODO: select default comment (most recent semester) when comments are loaded
        // TODO: combine duplicate semesters (caused by multiple sections per semester) into one semester
        // TODO: fix react table column headers, add method to toggle columns

        return (
          <div id="course-details" className="box clearfix">
          { !this.state.data ?
              <div id="select-prof">
              <div>
                  <h3 id="select-prof-text">Select a professor to see comments and more details.</h3>
                  <object type="image/svg+xml" data="/static/image/prof.svg">
                    <img alt="Professor Icon" src="/static/image/prof.png" />
                  </object>
              </div>
            </div> :
            <div id="course-details-wrapper">
              <h3>{this.state.data.instructor.name}</h3>
              <div className="btn-group mb-3">
                  <button onClick={() => { this.setState({ viewingRatings: true }); }} id="view_ratings" className={"btn btn-sm " + (this.state.viewingRatings ? "btn-sub-primary" : "btn-sub-secondary")}>Ratings</button>
                  <button onClick={() => { this.setState({ viewingRatings: false }); }} id="view_comments" className={"btn btn-sm " + (!this.state.viewingRatings ? "btn-sub-primary" : "btn-sub-secondary")}>Comments</button>
              </div>
              {this.state.viewingRatings ? <div id="course-details-data">
                  <ReactTable showPagination={false} style={{ maxHeight: '400px' }} data={ Object.values(this.state.data.sections).map((i) => ({...i.ratings, semester: i.semester, name: i.course_name})) } columns={ ["semester", "name"].concat(Object.keys(Object.values(this.state.data.sections)[0].ratings)).map((info) => ({ id: info, Header: info, accessor: info, Cell: props => isNaN(props.value) ? props.value : <center>{props.value.toFixed(2)}</center> })) } />
              </div> :
              <div id="course-details-comments" className="clearfix">
                  <div className="list">{ Object.values(this.state.data.sections).sort(compareSemesters).map((info, i) => <div key={i} onClick={() => { this.setState({ selectedSemester: info.semester }); }} className={this.state.selectedSemester === info.semester ? "selected": ""}>{info.semester}</div>) }</div>
                  <div className="comments">{ Object.values(this.state.data.sections).filter((info) => info.semester === this.state.selectedSemester).map((info, i) => <div key={i}>{info.comments || "This professor does not have any comments for this semester."}</div>) }</div>
              </div>}
            </div> }
          </div>
        );
    }
}

export default DetailsBox;
