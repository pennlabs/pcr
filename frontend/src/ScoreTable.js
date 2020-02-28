import React, { useEffect, useState } from 'react'
import ReactTable from 'react-table'

const ScoreTable = props => {
  const {
    alternating = false,
    noun,
    multi,
    data = [],
    onSelect = () => {},
  } = props
  const [selected, setSelected] = useState(multi ? {} : null)
  const [sorted, setSorted] = useState(props.sorted)

  useEffect(() => {
    const selected = multi ? {} : null
    setSelected(selected)
    onSelect && onSelect(selected)
  }, [data, multi, onSelect])

  const getTrProps = (_, rowInfo) => {
    const { index, original, row } = rowInfo
    const noRow = multi ? index in selected : index === selected
    return rowInfo && row
      ? {
          style: alternating
            ? { backgroundColor: row._viewIndex % 2 ? '#F5F8F8' : 'white' }
            : {},
          onClick: () => {
            if (!multi) {
              const { key } = original
              onSelect(noRow ? null : key)
              setSelected(noRow ? null : index)
              return
            }
            if (noRow) {
              delete selected[index]
            } else {
              selected[index] = rowInfo
            }
            onSelect(selected)
            setSelected({ ...selected })
          },
          className: noRow ? 'selected' : '',
        }
      : {}
  }

  return (
    <div>
      <ReactTable
        className="mb-2"
        {...props}
        showPagination={false}
        resizable={false}
        style={{ maxHeight: 400 }}
        getTrProps={getTrProps}
        minRows={0}
        pageSize={data.length}
        sorted={sorted}
        onSortedChange={setSorted}
      />
      <span id="course-table_info">
        Showing {data.length} {(noun || 'row') + (data.length !== 1 ? 's' : '')}
      </span>
    </div>
  )
}

export default ScoreTable
