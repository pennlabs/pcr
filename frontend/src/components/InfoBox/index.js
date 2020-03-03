import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import reactStringReplace from 'react-string-replace'

import Ratings from './InfoRatings'
import { CourseDescription, CourseHeader } from './CourseInfo'
import { apiContact } from '../../utils/api'

/**
 * Information box on the left most side, containing scores and descriptions
 * of course or professor.
 */

const InfoBox = ({
  type,
  data: {
    average_ratings: average = {},
    recent_ratings: recent = {},
    code = '',
    aliases,
    description,
    instructors,
    name,
    notes,
    num_sections: numSections,
    num_sections_recent: numSectionsRecent,
  },
  data,
  liveData,
  selectedCourses,
}) => {
  const [contact, setContact] = useState(null)
  const [inCourseCart, setInCourseCart] = useState(
    Boolean(localStorage.getItem(code))
  )

  useEffect(() => {
    if (type === 'instructor') apiContact(name).then(setContact)
  }, [name, type])

  const handleAdd = key => {
    let instructor = 'Average Professor'
    if (key !== 'average') {
      ;({
        name: instructor,
        average_reviews: average,
        recent_reviews: recent,
      } = instructors[key])
    }
    const info = Object.keys(average).map(category => ({
      category,
      average: average[category],
      recent: recent[category],
    }))
    const item = JSON.stringify({
      version: 1,
      course: code,
      instructor,
      info,
    })
    localStorage.setItem(code, item)
    if (window.onCartUpdated) window.onCartUpdated()
    setInCourseCart(true)
  }
  const handleRemove = () => {
    localStorage.removeItem(code)
    setInCourseCart(false)
    if (window.onCartUpdated) window.onCartUpdated()
  }

  const {
    rInstructorQuality: avgInstructorQuality,
    rCourseQuality: avgCourseQuality,
    rDifficulty: avgDifficulty,
  } = average
  const {
    rInstructorQuality: recentInstructorQuality,
    rCourseQuality: recentCourseQuality,
    rDifficulty: recentDifficulty,
  } = recent

  if (!data) {
    return <h1>Loading data...</h1>
  }

  return (
    <div className="box">
      <div id="banner-info" data-type="course">
        {type === 'course' && (
          <div className="course">
            <div className="title">
              {code.replace('-', ' ')}

              <span className="float-right">
                {inCourseCart ? (
                  <span
                    onClick={handleRemove}
                    className="courseCart btn btn-action"
                    title="Remove from Cart"
                  >
                    <i className="fa fa-fw fa-trash-alt" />
                  </span>
                ) : (
                  <Popover
                    button={
                      <span
                        className="courseCart btn btn-action"
                        title="Add to Cart"
                      >
                        <i className="fa fa-fw fa-cart-plus" />
                      </span>
                    }
                  >
                    <div className="popover-title">Add to Cart</div>
                    <div
                      className="popover-content"
                      style={{ maxHeight: 400, overflowY: 'auto' }}
                    >
                      <div id="divList">
                        <ul className="professorList">
                          <li>
                            <button onClick={() => handleAdd('average')}>
                              Average Professor
                            </button>
                          </li>
                          {Object.keys(instructors)
                            .sort((a, b) =>
                              instructors[a].name.localeCompare(
                                instructors[b].name
                              )
                            )
                            .map(key => (
                              <li key={key}>
                                <button onClick={() => handleAdd(key)}>
                                  {instructors[key].name}
                                </button>
                              </li>
                            ))}
                        </ul>
                      </div>
                    </div>
                  </Popover>
                )}{' '}
                <a
                  target="_blank"
                  rel="noopener noreferrer"
                  title="Get Alerted"
                  href={`https://penncoursealert.com/?course=${code}&source=pcr`}
                  className="btn btn-action"
                >
                  <i className="fas fa-fw fa-bell" />
                </a>
              </span>
            </div>
            {Boolean(aliases.length) && (
              <div className="crosslist">
                Also:{' '}
                {aliases.map((cls, i) => [
                  i > 0 && ', ',
                  <Link key={cls} to={`/course/${cls}`}>
                    {cls}
                  </Link>,
                ])}
              </div>
            )}
            <p className="subtitle">{name}</p>
            {notes.map(note => (
              <div key={note} className="note">
                <i className="fa fa-thumbtack" /> {note}
              </div>
            ))}
            {type === 'course' && liveData && (
              <Tags
                {...liveData}
                data={data}
                existingInstructors={Object.values(instructors).map(
                  a => a.name
                )}
              />
            )}
          </div>
        )}

        {type === 'instructor' && (
          <div className="instructor">
            <div className="title">{name}</div>
            {contact && (
              <div>
                <p className="desc">
                  Email:{' '}
                  <a href={`mailto:${contact.email}`}>
                    {contact.email.toLowerCase()}
                  </a>
                </p>
              </div>
            )}
            {notes.map(note => (
              <div key={note} className="note">
                <i className="fa fa-thumbtack" /> {note}
              </div>
            ))}
          </div>
        )}

        {type === 'department' && (
          <div className="department">
            <div className="title">{name}</div>
            <p className="subtitle">{code}</p>
          </div>
        )}
      </div>

      {type !== 'department' && (
        <div id="banner-score">
          <Ratings
            value="Average"
            instructor={avgInstructorQuality}
            course={avgCourseQuality}
            difficulty={avgDifficulty}
            num_sections={numSections}
          />

          <Ratings
            value="Recent"
            instructor={recentInstructorQuality}
            course={recentCourseQuality}
            difficulty={recentDifficulty}
            num_sections={numSectionsRecent}
          />
        </div>
      )}

      {type === 'department' && <DepartmentInfo courses={selectedCourses} />}

      {type === 'course' && (
        <p className="desc">
          {reactStringReplace(description, /([A-Z]{2,4}[ -]\d{3})/g, (m, i) => (
            <Link to={`/course/${m.replace(' ', '-')}`} key={m + i}>
              {m}
            </Link>
          ))}
        </p>
      )}
    </div>
  )
}

export default InfoBox
