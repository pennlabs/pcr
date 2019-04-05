import React, { Component } from 'react';

class DetailsBox extends Component {
    render() {
        return (
          <div id="course-details" class="box clearfix">
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
              <span class="btn-group">
                  <button id="view_ratings" class="btn btn-sm btn-sub-primary">Ratings</button>
                  <button id="view_comments" class="btn btn-sm btn-sub-secondary">Comments</button>
              </span>
              <span><button id="course-details-dropdown" class="btn btn-sm btn-sub-primary ml-2"><i class="fa fa-plus"></i></button></span>
              <div id="course-details-data"></div>
              <div id="course-details-comments" class="clearfix" style={{ display:'none' }}>
                  <div class="list"></div>
                  <div class="comments"></div>
                  <p class="empty">This professor does not have any comments.</p>
              </div>
            </div>
          </div>
        );
    }
}

export default DetailsBox;
