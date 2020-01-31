import React, { Component } from 'react'
import Popover from './Popover'

/**
 * Used to select the columns that appear in a table.
 */
class ColumnSelector extends Component {
  constructor(props) {
    super(props)
    const { columns, type, name } = props
    let defaultColumns = localStorage.getItem(`meta-${name}`)
    if (defaultColumns) {
      defaultColumns = JSON.parse(defaultColumns)
    } else {
      const instructorFields = type === 'instructor'
        ? {
          latest_semester: true,
          num_semesters: true,
        }
        : {}

      defaultColumns = {
        ...instructorFields,
        rInstructorQuality: true,
        rCourseQuality: true,
        rDifficulty: true,
        rAmountLearned: true,
      }
    }
    this.defaultColumns = defaultColumns

    this.setAllColumns = this.setAllColumns.bind(this)
    this.changeColumns = this.changeColumns.bind(this)

    this.changeColumns(columns.map((a) => ({ ...a, show: a.required || !!defaultColumns[a.id] })))
  }

  changeColumns(cols) {
    const newColumns = cols.reduce((map, obj) => {
      map[obj.id] = obj.show
      return map
    }, {})
    this.defaultColumns = Object.assign(this.defaultColumns, newColumns)
    localStorage.setItem(`meta-${this.props.name}`, JSON.stringify(this.defaultColumns))
    this.props.onSelect(cols)
  }

  handleToggle(i) {
    return () => {
      const columnsCopy = Array.from(this.props.columns)
      columnsCopy[i] = { ...columnsCopy[i], show: !columnsCopy[i].show }
      this.changeColumns(columnsCopy)
    }
  }

  setAllColumns(val) {
    return () => {
      const columnsCopy = this.props.columns.map((a) => ({ ...a, show: a.required || val }))
      this.changeColumns(columnsCopy)
    }
  }

  render() {
    let x = 0

    return (
      <Popover style={{ width: 340 }} button={<button aria-label='Choose Columns' className={`btn btn-sm ml-2 ${this.props.buttonStyle || 'btn'}-primary`}><i className='fa fa-plus' /></button>}>
        <span onClick={this.setAllColumns(true)} className={`btn mb-2 mr-2 btn-sm ${this.props.buttonStyle || 'btn'}-secondary`} style={{ width: 150, textAlign: 'center' }}>Select all</span>
        <span onClick={this.setAllColumns(false)} className={`btn mb-2 btn-sm ${this.props.buttonStyle || 'btn'}-secondary`} style={{ width: 150, textAlign: 'center' }}>Clear</span>
        <hr />
        {this.props.columns.map((item, i) => {
          if (item.required) {
            return false
          }
          x += 1
          return <span key={i} onClick={this.handleToggle(i)} style={{ width: 150, textAlign: 'center' }} className={`btn mt-2 btn-sm ${x % 2 === 1 ? 'mr-2 ' : ''}${this.props.buttonStyle || 'btn'}${item.show ? '-primary' : '-secondary'}`}>{item.Header}</span>
        })}
      </Popover>
    )
  }
}

export default ColumnSelector
