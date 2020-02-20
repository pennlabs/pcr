import React, { Component } from 'react'
import ReactTable from 'react-table'

/**
 * A wrapper for the react table with common table functionality and styling.
 */
export class ScoreTable extends Component {
  constructor(props) {
    super(props)

    this.state = {
      selected: this.props.multi ? {} : null,
      sorted: this.props.sorted,
    }

    this.resort = this.resort.bind(this)
  }

  componentDidUpdate(prevProps) {
    if (prevProps.data !== this.props.data) {
      // TODO: Switch to functional component and use useEffect(() => {...}, [])
      // eslint-disable-next-line react/no-did-update-set-state
      this.setState({ selected: this.props.multi ? {} : null })
      if (this.props.onSelect) {
        this.props.onSelect(this.props.multi ? {} : null)
      }
    }
  }

  resort() {
    this.setState(state => ({
      sorted: state.sorted.slice(),
    }))
  }

  render() {
    return (
      <div>
        <ReactTable
          className="mb-2"
          {...this.props}
          showPagination={false}
          resizable={false}
          style={{ maxHeight: 400 }}
          getTrProps={(_, rowInfo) => {
            const { selected } = this.state
            const { multi, onSelect } = this.props
            const { index, original, row } = rowInfo
            const noRow = multi ? index in selected : index === selected
            if (rowInfo && row) {
              return {
                onClick: () => {
                  if (multi) {
                    if (noRow) {
                      delete selected[index]
                    } else {
                      selected[index] = rowInfo
                    }
                    onSelect && onSelect(selected)
                    return this.setState({ selected: { ...selected } })
                  }
                  onSelect && onSelect(noRow ? null : original.key)
                  return this.setState({ selected: noRow ? null : index })
                },
                className: noRow ? 'selected' : '',
              }
            }
            return {}
          }}
          minRows={0}
          pageSize={this.props.data.length}
          sorted={this.state.sorted}
          onSortedChange={sorted => {
            this.setState({ sorted })
          }}
        />
        <span id="course-table_info">
          Showing {this.props.data.length}{' '}
          {(this.props.noun || 'row') +
            (this.props.data.length !== 1 ? 's' : '')}
        </span>
      </div>
    )
  }
}
