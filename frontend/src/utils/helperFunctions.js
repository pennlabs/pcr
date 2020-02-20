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
