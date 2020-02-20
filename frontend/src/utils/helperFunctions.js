export const capitalize = str =>
  str.replace(/(?:^|\s)\S/g, e => e.toUpperCase())

export function orderColumns(cols) {
  const colSet = new Set(cols)
  const fixedCols = [
    'latest_semester',
    'num_semesters',
    'rCourseQuality',
    'rInstructorQuality',
    'rDifficulty',
    'rAmountLearned',
  ].filter(a => colSet.has(a))
  const fixedColsSet = new Set(fixedCols)
  return fixedCols.concat(cols.filter(a => !fixedColsSet.has(a)).sort())
}

export function getColumnName(key) {
  return key
    .substring(1)
    .split(/(?=[A-Z])/)
    .join(' ')
    .replace('T A', 'TA')
    .replace(/Recommend/g, 'Rec.')
}

// Compares PCR semester codes.
export function compareSemesters(a, b) {
  const ay = parseInt(a.split(' ')[1])
  const by = parseInt(b.split(' ')[1])
  const as = a.split(' ')[0]
  const bs = b.split(' ')[0]

  if (ay !== by) {
    return by - ay
  }

  const mapping = { Fall: 'A', Summer: 'B', Spring: 'C' }

  return mapping[as].localeCompare(mapping[bs])
}

// Converts an instructor name into a unique key that should be the same for historical data and the Penn directory.
// TODO: Move this to a Redux store or React context
const nameCache = {}

export function convertInstructorName(name) {
  if (name in nameCache) {
    return nameCache[name]
  }
  const out = name
    .toUpperCase()
    .substr(0, 30)
    .replace(/[^a-zA-Z\s]/g, '')
    .replace(/ [A-Z]+ /g, ' ')
  nameCache[name] = out
  return out
}
