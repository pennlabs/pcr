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
            isAverage: true
        };
        this.handleClick = this.handleClick.bind(this);
        this.handleToggle = this.handleToggle.bind(this);
    }

    handleClick() {
        this.setState(state => ({
            isAverage: !state.isAverage,
            sorted: state.sorted.slice()
        }));
        console.log(this.state.columns);
    }

    handleToggle(i) {
        return() => {
            console.log(i);
            this.setState((state) => {
                state.columns[i].show = false;
                return state;
            })
            console.log(this.state.columns);
        };
    }


    componentDidMount() {
        fetch("http://localhost:8000/api/display/course/WRIT-002?token=public").then(res => res.json()).then((results) => {
            const columns = {};
            const data = Object.keys(results.instructors).map((key) => {
                const val = results.instructors[key];
                const output = {};
                Object.keys(val.average_reviews).forEach((col) => {
                    output[col] = {
                        average: val.average_reviews[col].toFixed(2),
                        recent: val.recent_reviews[col].toFixed(2)
                    };
                    columns[col] = true;
                });
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
                };
            });
            cols.unshift({
                Header: "Instructor",
                accessor: "name",
                width: 300
            });
            this.setState(state => ({
                data: data,
                columns: cols
            }));
        });
    }

    render() {
        if (!this.state.data) {
            return <h1>Loading Data...</h1>;
        }
        return (
            <div>
                <div>
                    {this.state.columns.map((item, i) => <div key={i} onClick={this.handleToggle(i)}>{item.Header}</div>)}
                </div>
                <button onClick={this.handleClick}>
                    {this.state.isAverage ? 'Average' : 'Most Recent'}
                </button>
                <ReactTable data={this.state.data} sorted={this.state.sorted} onSortedChange={sorted => {this.setState({ sorted });}} columns={this.state.columns} showPagination={false} resizable={false} defaultPageSize={this.state.data.length} style={{ maxHeight: "400px" }} />
            </div>
        );
    }
}

export default ScoreTable;