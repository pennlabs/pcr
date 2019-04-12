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
            output.key = key;
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
            show: true
        });
        this.setState(state => ({
            data: data,
            columns: cols
        }));
    }

    render() {
        if (!this.state.data) {
            return <h1>Loading Data...</h1>;
        }
        return (
            <div>
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
                            style: {
                                background: rowInfo.index === this.state.selected ? 'rgb(221, 235, 236)' : 'white'
                            }
                        };
                    }
                    return {};
                }} />
            </div>
        );
    }
}

export default ScoreTable;
