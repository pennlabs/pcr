import React, { Component } from 'react';
import ReactTable from 'react-table';
import { api_history } from './api';

class DetailsBox extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null
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
              <span className="btn-group">
                  <button id="view_ratings" className="btn btn-sm btn-sub-primary">Ratings</button>
                  <button id="view_comments" className="btn btn-sm btn-sub-secondary">Comments</button>
              </span>
              <span><button id="course-details-dropdown" className="btn btn-sm btn-sub-primary ml-2"><i className="fa fa-plus"></i></button></span>
              <div id="course-details-data">
                  <ReactTable showPagination={false} data={ Object.values(this.state.data.sections).map((i) => ({...i.ratings, semester: i.semester, name: i.course_name})) } columns={ ["semester", "name"].concat(Object.keys(Object.values(this.state.data.sections)[0].ratings)).map((info) => ({ id: info, Header: info, accessor: info })) } />
              </div>
              <div id="course-details-comments" className="clearfix">
                  <div className="list">{ Object.values(this.state.data.sections).map((info, i) => <div key={i}>{info.semester}</div>) }</div>
                  <div className="comments">{ Object.values(this.state.data.sections).map((info, i) => <div key={i}>{info.comments}</div>) }</div>
                  <p className="empty">This professor does not have any comments.</p>
              </div>
            </div> }
          </div>
        );
    }
}

export default DetailsBox;
