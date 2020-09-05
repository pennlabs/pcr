import React from 'react'
import { Link } from 'react-router-dom'
import { getLogoutUrl } from '../utils/api'
import { FEEDBACK_AIRTABLE, STWING_WEBSITE, WEBSITE } from '../constants/routes'

/**
 * The footer of every page.
 */
const Footer = ({ style }) => (
  <div style={style} id="footer">
    <div id="footer-inner">
      <Link to="/about">About</Link> | <Link to="/faq">FAQs</Link> |{' '}
      <a
        target="_blank"
        rel="noopener noreferrer"
        href={FEEDBACK_AIRTABLE}
      >
        Feedback
      </a>{' '}
      | <a href={getLogoutUrl()}>Logout</a>
      <p id="copyright">
        Made with <i style={{ color: '#F56F71' }} className="fa fa-heart" /> by{' '}
        <a href={WEBSITE}>
          <strong>Penn Labs</strong>
        </a>{' '}
        | Hosted by{' '}
        <a href={STWING_WEBSITE}>
          <strong>STWing</strong>
        </a>
      </p>
    </div>
  </div>
)

export default Footer
