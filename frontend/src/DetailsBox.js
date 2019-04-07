import React, { Component } from 'react';

class DetailsBox extends Component {
    render() {
        return (
          <div id="course-details" className="box clearfix">
            <div id="select-prof">
              <div>
                  <h3 id="select-prof-text">Select a professor to see comments and more details.</h3>
                  <object type="image/svg+xml" data="/static/image/prof.svg">
                    <img src="/static/image/prof.png" />
                  </object>
              </div>
            </div>
            <div id="course-details-wrapper" style={{ display:'none' }}>
              <h3></h3>
              <span className="btn-group">
                  <button id="view_ratings" className="btn btn-sm btn-sub-primary">Ratings</button>
                  <button id="view_comments" className="btn btn-sm btn-sub-secondary">Comments</button>
              </span>
              <span><button id="course-details-dropdown" className="btn btn-sm btn-sub-primary ml-2"><i className="fa fa-plus"></i></button></span>
              <div id="course-details-data"></div>
              <div id="course-details-comments" className="clearfix" style={{ display:'none' }}>
                  <div className="list"></div>
                  <div className="comments"></div>
                  <p className="empty">This professor does not have any comments.</p>
              </div>
            </div>
          </div>
        );
    }
}

export default DetailsBox;
