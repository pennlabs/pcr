import React, { Component } from 'react';
import ReactTable from 'react-table';


import 'react-table/react-table.css';


class ScoreTable extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            columns: null
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
                        recent: val.average_reviews[col],
                        average: val.recent_reviews[col]
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
                    Cell: props => <center>
                                        { props.show_average ? <span className='cell_average'>{props.value ? props.value.average : "N/A"}</span> :
                                        <span className='cell_recent'>{props.value ? props.value.recent : "N/A"}</span> }
                                   </center>,
                    width: 100
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

        return <ReactTable data={this.state.data} show_average="abcghi" columns={this.state.columns} showPagination={false} resizable={false} defaultPageSize={this.state.data.length} style={{ "max-height": "400px" }} />;
    }
}

export default ScoreTable;
