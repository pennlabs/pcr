import React, { Component } from 'react'
import ReactTable from 'react-table'

/**
 * A wrapper for the react table with common table functionality and styling.
 */
class ScoreTable extends Component {
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
            if (rowInfo && rowInfo.row) {
              return {
                onClick: () => {
                  this.setState(state => {
                    const noRow = this.props.multi
                      ? rowInfo.index in state.selected
                      : rowInfo.index === state.selected
                    if (this.props.multi) {
                      if (noRow) {
                        delete state.selected[rowInfo.index]
                      } else {
                        state.selected[rowInfo.index] = rowInfo
                      }
                      if (this.props.onSelect) {
                        this.props.onSelect(state.selected)
                      }
                      return { selected: { ...state.selected } }
                    }

                    if (this.props.onSelect) {
                      this.props.onSelect(noRow ? null : rowInfo.original.key)
                    }
                    return { selected: noRow ? null : rowInfo.index }
                  })
                },
                className: (this.props.multi
                  ? rowInfo.index in this.state.selected
                  : rowInfo.index === this.state.selected)
                  ? 'selected'
                  : undefined,
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
          Showing
          {this.props.data.length}{' '}
          {(this.props.noun || 'row') +
            (this.props.data.length !== 1 ? 's' : '')}
        </span>
      </div>
    )
  }
}

export default ScoreTable
