import React, { Component } from 'react';
import ReactTable from 'react-table';
import Popover from './Popover';
import { convertInstructorName } from './Tags';

import 'react-table/react-table.css';

class ScoreTable extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            columns: null,
            sorted: [],
            isAverage: true,
            selected: null
        };
        this.handleClick = this.handleClick.bind(this);
        this.handleToggle = this.handleToggle.bind(this);
        this.setAllColumns = this.setAllColumns.bind(this);
    }

    handleClick() {
        this.setState(state => ({
            isAverage: !state.isAverage,
            sorted: state.sorted.slice()
        }));
    }

    handleToggle(i) {
        return() => {
            let columnsCopy = Array.from(this.state.columns);
            columnsCopy[i] = {...columnsCopy[i], show: !columnsCopy[i].show};
            this.setState((state) => ({
                ...state,
                columns: columnsCopy
            }))
        };
    }

    setAllColumns(val) {
        return () => {
            let columnsCopy = this.state.columns.map((a) => ({...a, show: val}));
            this.setState((state) => ({
                ...state,
                columns: columnsCopy
            }));
        };
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
            Cell: props => <span>{is_course && <a href={"/instructor/" + props.original.key} className="mr-1" style={{color: 'rgb(102, 146, 161)'}}><i className="instructor-link far fa-user"></i></a>} {props.value}{props.original.star && <i className={'fa-star ml-1 ' + (props.original.star.open ? 'fa' : 'far')}></i>}</span>
        });
        this.setState(state => ({
            data: data,
            columns: cols
        }));
    }

    render() {
        // TODO: default sort by professors currently teaching and then professors who have taught most recently
        // TODO: style column selector and buttons

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

        return (
            <div className="box clearfix">
                <div className="btn-group" onClick={this.handleClick}>
                    <button className={"btn btn-sm " + (this.state.isAverage ? 'btn-primary' : 'btn-secondary')}>Average</button>
                    <button className={"btn btn-sm " + (this.state.isAverage ? 'btn-secondary' : 'btn-primary')}>Most Recent</button>
                </div>
                <Popover button={<button className="btn btn-primary btn-sm ml-2"><i className="fa fa-plus"></i></button>}>
                    <span onClick={this.setAllColumns(true)} className="btn mb-2 btn-sm btn-secondary" style={{ width: '100%', textAlign: 'center' }}>Select all</span>
                    <span onClick={this.setAllColumns(false)} className="btn mb-2 btn-sm btn-secondary" style={{ width: '100%', textAlign: 'center' }}>Clear</span>
                    <hr style={{ borderBottom: '1px solid #ccc' }} />
                    {this.state.columns.map((item, i) => <span key={i} onClick={this.handleToggle(i)} style={{ width: '100%', textAlign: 'center' }} className={"btn mt-2 btn-sm " + (item.show ? 'btn-primary' : 'btn-secondary')}>{item.Header}</span>)}
                </Popover>
                <ReactTable className="mt-2" data={this.state.data} sorted={this.state.sorted} onSortedChange={sorted => {this.setState({ sorted });}} columns={this.state.columns} showPagination={false} resizable={false} defaultPageSize={this.state.data.length} style={{ maxHeight: "400px" }} getTrProps={(state, rowInfo) => {
                    if (rowInfo && rowInfo.row) {
                        return {
                            onClick: (e) => {
                                this.setState({
                                    selected: rowInfo.index
                                });
                                if (this.props.onSelect) {
                                    this.props.onSelect(rowInfo.original.key);
                                }
                            },
                            style: rowInfo.index === this.state.selected ? {
                                background: 'rgb(221, 235, 236)'
                            } : undefined
                        };
                    }
                    return {};
                }} />
            </div>
        );
    }
}

export default ScoreTable;
