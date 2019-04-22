import React, { Component } from 'react';
import ReactTable from 'react-table';


class ScoreTable extends Component {
    constructor(props) {
        super(props);

        this.state = {
            selected: null,
            sorted: this.props.sorted
        };

        this.resort = this.resort.bind(this);
    }

    componentDidUpdate(prevProps) {
        if (prevProps.data !== this.props.data) {
            this.setState({ selected: null });
            if (this.props.onSelect) {
                this.props.onSelect(null);
            }
        }
    }

    resort() {
        this.setState((state) => ({
            sorted: state.sorted.slice()
        }));
    }

    render() {
        return (<div className="mt-2">
            <ReactTable className="mb-2" {...this.props} showPagination={false} resizable={false} style={{ maxHeight: 400 }} getTrProps={
                (state, rowInfo) => {
                    if (rowInfo && rowInfo.row) {
                        return {
                            onClick: (e) => {
                                this.setState((state) => {
                                    const noRow = rowInfo.index === state.selected;
                                    if (this.props.onSelect) {
                                        this.props.onSelect(noRow ? null : rowInfo.original.key);
                                    }
                                    return {selected: noRow ? null : rowInfo.index};
                                });
                            },
                            className: rowInfo.index === this.state.selected ? 'selected' : undefined
                        };
                    }
                    return {};
                }
            } minRows={0} defaultPageSize={this.props.data.length} sorted={this.state.sorted} onSortedChange={(sorted) => { this.setState({ sorted }); }} />
            <span id="course-table_info">Showing {this.props.data.length} {(this.props.noun || "row") + (this.props.data.length !== 1 ? "s" : "")}</span>
        </div>);
    }
}

export default ScoreTable;
