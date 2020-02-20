import React, { useEffect, useState } from 'react'
import ReactTable from 'react-table'

const ScoreTable = props => {
  const { noun, multi, data = [], onSelect } = props
  const [selected, setSelected] = useState(multi ? {} : null)
  const [sorted, setSorted] = useState(props.sorted)

  useEffect(() => {
    const selected = multi ? {} : null
    setSelected(selected)
    onSelect && onSelect(selected)
  }, [data])

  const getTrProps = (_, rowInfo) => {
    const { index, original, row } = rowInfo
    const noRow = multi ? index in selected : index === selected
    return rowInfo && row
      ? {
          onClick: () => {
            if (multi) {
              if (noRow) {
                delete selected[index]
              } else {
                selected[index] = rowInfo
              }
              onSelect && onSelect(selected)
              setSelected({ ...selected })
            } else {
              onSelect && onSelect(noRow ? null : original.key)
              setSelected(noRow ? null : index)
            }
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
