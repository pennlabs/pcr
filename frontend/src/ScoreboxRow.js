import React, { Component } from 'react';

class ScoreboxRow extends Component {
  // state
  constructor(props) {

    super(props)

    this.state = {
    }
  }

  render() {
    return (
      <div className="scorebox-desc-row">
        <div className="scoredesc">
              <p className="title">{this.props.value}</p>
              <p className="subtitle">{this.props.num_sections} Sections</p>
          </div>
          <div className="scoreboxrow">
              <div className="scorebox course rating-okay">
                  <p className="num">{this.props.course}</p>
                  <p className="desc">Course</p>
              </div>
              <div className="scorebox instructor rating-okay">
                  <p className="num">{this.props.instructor}</p>
                  <p className="desc">Instructor</p>
              </div>
              <div className="scorebox difficulty rating-good">
                  <p className="num">{this.props.difficulty}</p>
                  <p className="desc">Difficulty</p>
              </div>
          </div>
      </div>
    );
  }
}

export default ScoreboxRow;
