import { useEffect } from 'react'
import { withRouter } from 'react-router-dom'

/**
 * Dummy component to make Google Analytics work well with React router.
 */
const Analytics = ({ location, history }) => {
  useEffect(() => {
    if (history.action === 'PUSH') {
      const { pathname, search } = location
      window.ga('set', 'page', pathname + search)
      window.ga('send', 'pageview')
    }
  }, [location])
  return null
}

export const GoogleAnalytics = withRouter(Analytics)
