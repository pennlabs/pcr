import React from 'react'
import { MAIL_TO } from '../../constants/routes'

export default ({ name, contact, notes }) => (
  <div className="instructor">
    <div className="title">{name}</div>
    {contact && (
      <div>
        <p className="desc">
          Email:{' '}
          <a href={MAIL_TO(contact.email)}> {contact.email.toLowerCase()}</a>
        </p>
      </div>
    )}
    {notes.map(note => (
      <div key={note} className="note">
        <i className="fa fa-thumbtack" /> {note}
      </div>
    ))}
  </div>
)
