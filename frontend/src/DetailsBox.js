import React, { Component } from 'react';
import ScoreTable from './ScoreTable';
import ColumnSelector from './ColumnSelector';
import { api_history } from './api';


function compareSemesters(a, b) {
    const ay = parseInt(a.split(" ")[1]);
    const by = parseInt(b.split(" ")[1]);

    if (ay !== by) {
        return by - ay;
    }

    return b.localeCompare(a);
}


class DetailsBox extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            viewingRatings: true,
            selectedSemester: null,
            semesterList: [],
            columns: []
        };
    }

    componentDidUpdate(prevProps) {
        if (prevProps.instructor !== this.props.instructor || prevProps.course !== this.props.course) {
            if (this.props.instructor !== null) {
                api_history(this.props.course, this.props.instructor).then((res) => {
                    const list = [...new Set(Object.values(res.sections).filter((a) => a.comments).sort((a, b) => compareSemesters(a.semester, b.semester)).map((a) => a.semester))];
                    this.setState((state) => ({
                        data: res,
                        columns: [
                            {id: 'semester', width: 150, Header: 'Semester', accessor: 'semester', sortMethod: compareSemesters, show: true, required: true},
                            {id: 'name', width: 300, Header: 'Name', accessor: 'name', show: true, required: true}
                        ].concat(Object.keys(Object.values(res.sections)[0].ratings).map((info) => ({
                            id: info,
                            width: 150,
                            Header: info.substring(1).split(/(?=[A-Z])/).join(" ").replace("T A", "TA").replace(/Recommend/g, "Rec."),
                            accessor: info,
                            Cell: props => <center>{isNaN(props.value) ? "N/A" : props.value.toFixed(2)}</center>,
                            show: true
                        }))),
                        semesterList: list,
                        selectedSemester: list.length ? (list.indexOf(state.selectedSemester) !== -1 ? state.selectedSemester : list[0]) : null
                    }));
                });
            }
            else {
                this.setState({
                    data: null,
                    semesterList: []
                });
            }
        }
    }

    render() {
        return (
          <div id="course-details" className="box clearfix">
          { this.props.instructor && !this.state.data ? <div>Loading...</div> : !this.state.data ?
              <div id="select-prof">
              <div>
                  <h3 id="select-prof-text">Select a professor to see comments and more details.</h3>
                  <object type="image/svg+xml" data="/static/image/prof.svg">
                    <img alt="Professor Icon" src="/static/image/prof.png" />
                  </object>
              </div>
            </div> :
            <div id="course-details-wrapper">
              <h3><a style={{ color: '#b2b2b2', textDecoration: 'none' }} href={"/instructor/" + this.props.instructor}>{this.state.data.instructor.name}</a></h3>
              <div className="btn-group">
                  <button onClick={() => { this.setState({ viewingRatings: true }); }} id="view_ratings" className={"btn btn-sm " + (this.state.viewingRatings ? "btn-sub-primary" : "btn-sub-secondary")}>Ratings</button>
                  <button onClick={() => { this.setState({ viewingRatings: false }); }} id="view_comments" className={"btn btn-sm " + (!this.state.viewingRatings ? "btn-sub-primary" : "btn-sub-secondary")}>Comments</button>
              </div>
              <ColumnSelector onSelect={(cols) => this.setState({ columns: cols })} columns={this.state.columns} buttonStyle="btn-sub" />
              {this.state.viewingRatings ? <div id="course-details-data">
                  <ScoreTable
                  data={ Object.values(this.state.data.sections).map((i) => ({...i.ratings, semester: i.semester, name: i.course_name})) }
                  columns={this.state.columns} noun="section" />
              </div> :
              <div id="course-details-comments" className="clearfix mt-2">
                  <div className="list">{ this.state.semesterList.map((info, i) => <div key={i} onClick={() => { this.setState({ selectedSemester: info }); }} className={this.state.selectedSemester === info ? "selected": ""}>{info}</div>) }</div>
                  <div className="comments">{ Object.values(this.state.data.sections).filter((info) => info.semester === this.state.selectedSemester && info.comments).map((info) => info.comments).join(", ") || "This instructor does not have any comments for this course." }</div>
              </div>}
            </div> }
          </div>
        );
    }
}

export default DetailsBox;
