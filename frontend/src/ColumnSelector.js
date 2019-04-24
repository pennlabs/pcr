import React, { Component } from 'react';
import Popover from './Popover';


class ColumnSelector extends Component {
    constructor(props) {
        super(props);

        this.handleToggle = this.handleToggle.bind(this);
        this.setAllColumns = this.setAllColumns.bind(this);
        this.changeColumns = this.changeColumns.bind(this);

        var defaultColumns = localStorage.getItem("meta-" + this.props.name);
        if (defaultColumns) {
            defaultColumns = JSON.parse(defaultColumns);
        }
        else {
            defaultColumns = {rInstructorQuality: true, rCourseQuality: true, rDifficulty: true, rAmountLearned: true};
        }
        this.defaultColumns = defaultColumns;
        this.changeColumns(this.props.columns.map((a) => ({...a, show: a.required || !!defaultColumns[a.id]})));
    }

    changeColumns(cols) {
        var newColumns = cols.reduce((map, obj) => {
            map[obj.id] = obj.show;
            return map;
        }, {});
        this.defaultColumns = Object.assign(this.defaultColumns, newColumns);
        localStorage.setItem("meta-" + this.props.name, JSON.stringify(this.defaultColumns));
        this.props.onSelect(cols);
    }

    handleToggle(i) {
        return () => {
            let columnsCopy = Array.from(this.props.columns);
            columnsCopy[i] = {...columnsCopy[i], show: !columnsCopy[i].show};
            this.changeColumns(columnsCopy);
        };
    }

    setAllColumns(val) {
        return () => {
            let columnsCopy = this.props.columns.map((a) => ({...a, show: a.required || val}));
            this.changeColumns(columnsCopy);
        };
    }

    render() {
        var x = 0;

        return <Popover style={{ width: 340 }} button={<button className={"btn btn-sm ml-2 " + (this.props.buttonStyle || "btn") + "-primary"}><i className="fa fa-plus"></i></button>}>
            <span onClick={this.setAllColumns(true)} className={"btn mb-2 mr-2 btn-sm " + (this.props.buttonStyle || "btn") + "-secondary"} style={{ width: 150, textAlign: 'center' }}>Select all</span>
            <span onClick={this.setAllColumns(false)} className={"btn mb-2 btn-sm " + (this.props.buttonStyle || "btn") + "-secondary"} style={{ width: 150, textAlign: 'center' }}>Clear</span>
            <hr style={{ borderBottom: '1px solid #ccc' }} />
            {this.props.columns.map((item, i) => {
                if (item.required) {
                    return false;
                }
                x += 1;
                return <span key={i} onClick={this.handleToggle(i)} style={{ width: 150, textAlign: 'center' }} className={"btn mt-2 btn-sm " + (x % 2 === 1 ? "mr-2 " : "") + (this.props.buttonStyle || "btn") + (item.show ? '-primary' : '-secondary')}>{item.Header}</span>;
            })}
        </Popover>;
    }
}


export default ColumnSelector;
