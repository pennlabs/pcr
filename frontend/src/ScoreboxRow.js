import React, { Component } from 'react';

class ScoreboxRow extends Component {
  // state
  constructor(props) {

    super(props)

    this.state = {
      //board = Array(9).fill(null)
    }
  }

  // events like handleClick

  render() {
    return (
      <div className="scoreboxrow">
        <div className="scoredesc">
              <p className="title">{this.props.value}</p>
              <p className="subtitle">23 Sections</p>
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
