import React, { Component } from 'react';
import ReactTable from 'react-table';


class ScoreTable extends Component {
    constructor(props) {
        super(props);

        this.state = {
            selected: null,
            sorted: []
        };

        this.resort = this.resort.bind(this);
    }

    resort() {
        this.setState((state) => ({
            sorted: state.sorted.slice()
        }));
    }

    render() {
        return <ReactTable {...this.props} showPagination={false} resizable={true} style={{ maxHeight: 400 }} getTrProps={
            (state, rowInfo) => {
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
            }
        } defaultPageSize={this.props.data.length} sorted={this.state.sorted} onSortedChange={(sorted) => { this.setState({ sorted }); }} />
    }
}

export default ScoreTable;
