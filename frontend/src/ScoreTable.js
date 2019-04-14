import React, { Component } from 'react';
import ReactTable from 'react-table';

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
                    if (this.state.isAverage) {
                      return a.average > b.average ? 1 : -1;
                    }
                    return a.recent > b.recent ? 1 : -1;
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
            Cell: props => <span>{props.value}{props.original.star && <i className={'fa-star ml-1 ' + (props.original.star.open ? 'fa' : 'far')}></i>}</span>
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
                const key = a.toUpperCase().replace(/[^a-zA-Z\s]/g, '');
                Object.values(this.props.live_data.courses).forEach((cat) => {
                    const all_courses_by_instructor = cat.filter((a) => a.instructors.map((b) => b.name.toUpperCase().replace(/[^a-zA-Z\s]/g, '')).indexOf(key) !== -1).filter((a) => !a.is_cancelled);
                    data.open += all_courses_by_instructor.filter((a) => !a.is_closed).length;
                    data.all += all_courses_by_instructor.length;
                });
                instructors_this_semester[key] = data;
            });

            this.state.data.forEach(function(row) {
                const currentInfo = instructors_this_semester[row.name.toUpperCase().replace(/[^a-zA-Z\s]/g, '')];
                row['star'] = currentInfo;
            });
        }

        return (
            <div className="box clearfix">
                <div>
                    {this.state.columns.map((item, i) => <span key={i} onClick={this.handleToggle(i)} style={{ marginRight: 10, fontWeight: item.show ? "bold": "normal" }}>{item.Header}</span>)}
                </div>
                <button onClick={this.handleClick}>
                    {this.state.isAverage ? 'Average' : 'Most Recent'}
                </button>
                <ReactTable data={this.state.data} sorted={this.state.sorted} onSortedChange={sorted => {this.setState({ sorted });}} columns={this.state.columns} showPagination={false} resizable={false} defaultPageSize={this.state.data.length} style={{ maxHeight: "400px" }} getTrProps={(state, rowInfo) => {
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
