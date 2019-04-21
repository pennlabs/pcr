import React, { Component } from 'react';
import ScoreTable from './ScoreTable';
import ColumnSelector from './ColumnSelector';
import { convertInstructorName } from './Tags';

import 'react-table/react-table.css';

class ScoreBox extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            columns: null,
            isAverage: true
        };
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick() {
        this.setState(state => ({
            isAverage: !state.isAverage
        }));
        this.refs.table.resort();
    }

    componentDidMount() {
        const results = this.props.data;

        const columns = {};
        const is_course = this.props.type === "course";
        const data = Object.keys(is_course ? results.instructors : results.courses).map((key) => {
            const val = is_course ? results.instructors[key] : results.courses[key];
            const output = {};
            Object.keys(val.average_reviews).forEach((col) => {
                output[col] = {
                    average: val.average_reviews[col].toFixed(2),
                    recent: val.recent_reviews[col].toFixed(2)
                };
                columns[col] = true;
            });
            output.key = is_course ? key : val.code;
            output.name = val.name;
            return output;
        });
        const cols = Object.keys(columns).map((key) => {
            var header = key.substring(1).split(/(?=[A-Z])/).join(" ").replace("T A", "TA").replace(/Recommend/g, "Rec.");
            return {
                id: key,
                Header: header,
                accessor: key,
                sortMethod: (a, b) => {
                    if (a && b) {
                        a = this.state.isAverage ? a.average : a.recent;
                        b = this.state.isAverage ? b.average : b.recent;
                        return a > b ? 1 : -1;
                    }
                    return a ? 1 : -1;
                },
                Cell: props => <center>
                                    { this.state.isAverage ? <span className='cell_average'>{props.value ? props.value.average : "N/A"}</span> :
                                    <span className='cell_recent'>{props.value ? props.value.recent : "N/A"}</span> }
                               </center>,
                width: 150,
                show: true
            };
        });
        cols.unshift({
            Header: is_course ? "Instructor" : "Course",
            accessor: "name",
            width: 300,
            show: true,
            required: true,
            Cell: props => <span>{is_course && <a href={"/instructor/" + props.original.key} className="mr-1" style={{color: 'rgb(102, 146, 161)'}}><i className="instructor-link far fa-user"></i></a>} {props.value}{props.original.star && <i className={'fa-star ml-1 ' + (props.original.star.open ? 'fa' : 'far')}></i>}</span>
        });
        this.setState(state => ({
            data: data,
            columns: cols
        }));
    }

    render() {
        // TODO: default sort by professors currently teaching and then professors who have taught most recently

        if (!this.state.data) {
            return <h1>Loading Data...</h1>;
        }

        if (this.props.live_data) {
            const instructors_this_semester = {};
            const data = {
                open: 0,
                all: 0
            };
            this.props.live_data.instructors.forEach((a) => {
                const key = convertInstructorName(a);
                Object.values(this.props.live_data.courses).forEach((cat) => {
                    const all_courses_by_instructor = cat.filter((a) => a.instructors.map((b) => convertInstructorName(b.name)).indexOf(key) !== -1).filter((a) => !a.is_cancelled);
                    data.open += all_courses_by_instructor.filter((a) => !a.is_closed).length;
                    data.all += all_courses_by_instructor.length;
                });
                instructors_this_semester[key] = data;
            });

            this.state.data.forEach(function(row) {
                const currentInfo = instructors_this_semester[convertInstructorName(row.name)];
                row['star'] = currentInfo;
            });
        }

        const is_course = this.props.type === "course";

        return (
            <div className="box clearfix">
                <div className="btn-group" onClick={this.handleClick}>
                    <button className={"btn btn-sm " + (this.state.isAverage ? 'btn-primary' : 'btn-secondary')}>Average</button>
                    <button className={"btn btn-sm " + (this.state.isAverage ? 'btn-secondary' : 'btn-primary')}>Most Recent</button>
                </div>
                <ColumnSelector name="score" columns={this.state.columns} onSelect={(cols) => this.setState({ columns: cols })} />
                <ScoreTable ref="table" data={this.state.data} columns={this.state.columns} onSelect={this.props.onSelect} noun={is_course ? "instructor" : "course"} />
            </div>
        );
    }
}

export default ScoreBox;
