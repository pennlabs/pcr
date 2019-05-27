import React, { Component } from 'react';

/**
 * Three colored boxes with numerical rating values, used in the course description box.
 */
class ScoreboxRow extends Component {
  render() {
    function numOrNA(num) {
        return isNaN(num) ? "N/A" : num.toFixed(1);
    }

    function getColor(num) {
        if (isNaN(num)) {
            return "rating-good";
        }

        num = num.toFixed(1);

        if (num < 2) {
            return "rating-bad";
        }

        if (num < 3) {
            return "rating-okay";
        }

        return "rating-good";
    }

    return (
      <div className="scorebox-desc-row">
        <div className="scoredesc">
              <p className="title">{this.props.value}</p>{' '}
              <p className="subtitle">{this.props.num_sections} Sections</p>
          </div>
          <div className="scoreboxrow">
              <div className={"scorebox course " + getColor(this.props.course)}>
                  <p className="num">{numOrNA(this.props.course)}</p>
                  <p className="desc">Course</p>
              </div>
              <div className={"scorebox instructor " + getColor(this.props.instructor)}>
                  <p className="num">{numOrNA(this.props.instructor)}</p>
                  <p className="desc">Instructor</p>
              </div>
              <div className={"scorebox difficulty " + getColor(this.props.difficulty)}>
                  <p className="num">{numOrNA(this.props.difficulty)}</p>
                  <p className="desc">Difficulty</p>
              </div>
          </div>
      </div>
    );
  }
}

export default ScoreboxRow;
