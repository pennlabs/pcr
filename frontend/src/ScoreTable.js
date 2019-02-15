import React, { Component } from 'react';
import Tags from './Tags';
import ScoreboxRow from './ScoreboxRow'
import './static/css/base.css';
import 'bootstrap/dist/css/bootstrap.min.css';
// import './static/css/bootstrap.min.css';
// import './static/js/bootstrap.min.js';
// css of the react component
// each react component can only import the css file it needs
// index

// import './App.css'

class ScoreTable extends Component {
  // state
  constructor(props) {

    super(props)

    this.state = {
      items: null,
      average_ratings: null,
      tag_data: null
    }
  }

  componentDidMount() {
    // make sure that
    fetch("http://localhost:8000/api/display/course/CIS-121?token=public")
      .then(res => res.json())
      .then(
        (result) => {
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

  // render -> compoentditmount -> 121 info -> render -> load live data -> load datat again

  // events like handleClick

  // while develpoing, see everything pop up
  render() {
    //var average = this.state.items.average_ratings
    //console.log(average.rInstructorQuality)
    //console.log(this.state.tag_data) // only show up when the request is finished
    console.log(this.state)

    if (!this.state.items) {
      return (<h1>Loading data</h1>);
    }
    if (!this.state.tag_data) {
      return (<h1>Null tag data</h1>);
    }
    var noTags = !this.state.tag_data.term // noTags is true if term is Null

    //console.log(this.state.items.average_ratings.rInstructorQuality)
    return (
      <div className="col-sm-12 col-md-4 box-wrapper sidebar-col">
        <div className="box">
          <div id="banner-info" data-type="course">
            <div className="title">{this.state.items.code}

              <span className="float-right">
                <span id="popup" className="courseCart btn btn-action" title="Add to Cart"><i className="fa fa-fw fa-cart-plus"></i></span>
                <a target="_blank" title="Get Alerted" href="https://penncoursealert.com/?course=CIS-121&amp;source=pcr" className="btn btn-action"><i className="fas fa-fw fa-bell"></i></a>
              </span>
            </div>

            <div className="crosslist"></div>

            <p className="subtitle">{this.state.items.name}</p>

            <Tags noTags={noTags} term={this.state.tag_items.term} /> // pass live data to tags
          </div>

          <ScoreboxRow
            value="Average"
            instructor={this.state.average_ratings.rInstructorQuality}
            course={this.state.average_ratings.rCourseQuality}
            difficulty={this.state.average_ratings.rDifficulty}/>

          <ScoreboxRow
            value="Recent"
            instructor={this.state.recent_ratings.rInstructorQuality}
            course={this.state.recent_ratings.rCourseQuality}
            difficulty={this.state.recent_ratings.rDifficulty}/>

        <p className="desc">{this.state.items.description}
        </p>
        </div>
      </div>

    );
  }
}

export default ScoreTable;
