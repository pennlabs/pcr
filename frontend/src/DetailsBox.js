import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import ScoreTable from './ScoreTable';
import ColumnSelector from './ColumnSelector';
import { api_history } from './api';
import { getColumnName, orderColumns } from './ScoreBox';


function compareSemesters(a, b) {
    const ay = parseInt(a.split(" ")[1]);
    const by = parseInt(b.split(" ")[1]);

    if (ay !== by) {
        return by - ay;
    }

    return b.localeCompare(a);
}


/**
 * The box below the course ratings table that contains student comments and semester information.
 */
class DetailsBox extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            viewingRatings: true,
            selectedSemester: null,
            semesterList: [],
            columns: [],
            filtered: [],
            filterAll: ""
        };
    }

    componentDidUpdate(prevProps) {
        if (prevProps.instructor !== this.props.instructor || prevProps.course !== this.props.course) {
            if (this.props.instructor !== null && this.props.course !== null) {
                api_history(this.props.course, this.props.instructor).then((res) => {
                    const list = [...new Set(Object.values(res.sections).filter((a) => a.comments).sort((a, b) => compareSemesters(a.semester, b.semester)).map((a) => a.semester))];
                    this.setState((state) => ({
                        data: res,
                        columns: [
                            {id: 'semester', width: 150, Header: 'Semester', accessor: 'semester', sortMethod: compareSemesters, show: true, required: true},
                            {id: 'name', width: 300, Header: 'Name', accessor: 'name', show: true, required: true, filterMethod: (filter, rows) => {
                                if (filter.value === "") {
                                    return true;
                                }
                                return rows.name.toLowerCase().includes(filter.value.toLowerCase()) || rows.semester.toLowerCase().includes(filter.value.toLowerCase());
                            }},
                            {id: 'forms', width: 150, Header: 'Forms', accessor: 'forms_returned', show: true, required: true, Cell: props => typeof props.value === 'undefined' ? <center className='empty'>N/A</center> : <center>{props.value} / {props.original.forms_produced} <small style={{ color: '#aaa', fontSize: '0.8em' }}>({(props.value / props.original.forms_produced * 100).toFixed(1)}%)</small></center>}
                        ].concat(orderColumns(Object.keys(Object.values(res.sections)[0].ratings)).map((info) => ({
                            id: info,
                            width: 150,
                            Header: getColumnName(info),
                            accessor: info,
                            Cell: props => <center className={!props.value ? "empty" : ""}>{isNaN(props.value) ? "N/A" : props.value.toFixed(2)}</center>,
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
        const { course, instructor, type } = this.props;
        return (
          <div id="course-details" className="box">
          { ((type === "course" && instructor) || (type === "instructor" && course)) && !this.state.data ? <div>Loading...</div> : !this.state.data ?
              <div id="select-row">
              <div>
                  <h3 id="select-row-text">{ type === "instructor" ? "Select a course to see individual sections, comments, and more details." : "Select an instructor to see individual sections, comments, and more details."}</h3>
                  { type === "course" ? <object type="image/svg+xml" data="/static/image/prof.svg">
                    <img alt="Professor Icon" src="/static/image/prof.png" />
                  </object> : <object type="image/svg+xml" id="select-course-icon" data="/static/image/books-and-bag.svg">
                    <img alt="Class Icon" src="/static/image/books-and-bag.png" />
                  </object> } 
              </div>
            </div> :
            <div id="course-details-wrapper">
              <h3><Link style={{ color: '#b2b2b2', textDecoration: 'none' }} to={type === "course" ? `/instructor/${instructor}` : `/course/${course}`}>{type === "course" ? this.state.data.instructor.name : course}</Link></h3>
              <div className="clearfix">
                  <div className="btn-group">
                      <button onClick={() => { this.setState({ viewingRatings: true }); }} id="view_ratings" className={"btn btn-sm " + (this.state.viewingRatings ? "btn-sub-primary" : "btn-sub-secondary")}>Ratings</button>
                      <button onClick={() => { this.setState({ viewingRatings: false }); }} id="view_comments" className={"btn btn-sm " + (!this.state.viewingRatings ? "btn-sub-primary" : "btn-sub-secondary")}>Comments</button>
                  </div>
                  <ColumnSelector name="details" onSelect={(cols) => this.setState({ columns: cols })} columns={this.state.columns} buttonStyle="btn-sub" />
                  {this.state.viewingRatings && <div className="float-right"><label className="table-search"><input value={this.state.filterAll} onChange={(val) => this.setState({ filtered: [{id: "name", value: val.target.value}], filterAll: val.target.value })} type="search" className="form-control form-control-sm" /></label></div>}
              </div>
              {this.state.viewingRatings ? <div id="course-details-data">
                  <ScoreTable
                  sorted={[{id: 'semester', desc: false}]}
                  filtered={this.state.filtered}
                  data={ Object.values(this.state.data.sections).map((i) => ({...i.ratings, semester: i.semester, name: i.course_name, forms_produced: i.forms_produced, forms_returned: i.forms_returned})) }
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
