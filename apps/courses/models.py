import re

from django.db import models
from django.shortcuts import reverse

from .links import (RSRCS, DEPARTMENT_TOKEN, REVIEW_TOKEN,
                    COURSEHISTORY_TOKEN, COURSE_TOKEN, SECTION_TOKEN,
                    INSTRUCTOR_TOKEN)

# Note: each class has get_absolute_url - this is for "url" when queried


class Semester:
    """ A semester, with a calendar year and a season.
    Season codes: (a,b,c) -> (Spring, Summer, Fall)
      Note that:
      (Year Y, semester s) (with s=0,1,2 -> a,b,c) is semester
        3(Y-1740) + s       = 780 + 3(Y-2000) + s
      Semester 2010a is 810. Current (2010c) is 812.
    """

    def __init__(self, year=None, semester=None):
        """ Create a semester from a year and a season code.
          Valid inputs (all case-insensitive): Semester(2010, 'c') ==
            Semester('2010', 'c') == Semester('2010c') """
        if year is None:
            year, semester = 1740, "a"  # the epoch
        if semester is None:
            year, semester = year[:-1], year[-1]
        semesternum = "abc".find(semester.lower())
        if semesternum == -1:
            raise ValueError("Invalid semester code: " + semester)

        self.year = int(year)  # calendar year
        self.semesternum = semesternum  # (0,1,2) -> (Spring, Summer, Fall)

    @property
    def id(self):
        """ Returns the numerical ID for this semester.
        (Year Y, semester s) (with s=0,1,2 -> a,b,c) is semester
          3(Y-1740) + s       = 780 + 3(Y-2000) + s
        Semester 2010a is 810. Current (2010c) is 812. """
        return 3 * (self.year - 1740) + self.semesternum

    @property
    def seasoncodeABC(self):
        """ Returns the season code. """
        return "ABC"[self.semesternum]

    def code(self):
        """ Returns code YYYYa (calendar year + season code) """
        return "%4d%s" % (self.year, self.seasoncodeABC)

    def __repr__(self):
        return "Semester(%d,\"%s\")" % (self.year, self.seasoncodeABC)

    def __str__(self):
        return "%s %d" % (["Spring", "Summer", "Fall"][self.semesternum], self.year)

    def get_absolute_url(self):
        return reverse("semester", kwargs={"semester_code": self.code()})

    def __cmp__(self, other):
        if other:
            return cmp(self.id, other.id)
        else:
            return 1  # arbitrarily, if other is given as ''

    def toShortJSON(self):
        return {
            'id': self.code(),
            'name': str(self),
            'year': self.year,
            'seasoncode': self.seasoncodeABC,
            'path': self.get_absolute_url()
        }

    def toJSON(self):
        # import here, to avoid circular import
        from models import Department, SemesterDepartment

        result = self.toShortJSON()

        depts = Department.objects.filter(alias__semester=self).order_by(
            'code').distinct()
        result[DEPARTMENT_TOKEN] = [SemesterDepartment(self, d).toShortJSON()
                                    for d in depts]
        return result


def semesterFromID(id):
    """ Given a numerical semester ID, return a semester. """
    if isinstance(id, Semester):
        return id
    return Semester(1740 + id / 3, "abc"[id % 3])


def semesterFromCode(yyyys):
    if len(yyyys) != 5:
        raise Exception("too many or too few characters")
    year = int(yyyys[:4])
    season = yyyys[4].lower()
    return Semester(year=year, semester=season)


class SemesterField(models.Field):
    description = "A semester during which a course may be offered"

    def __init__(self, *args, **kwargs):
        super(SemesterField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "SemesterField"

    def db_type(self, connection):
        return 'smallint'

    def to_python(self, value):
        if isinstance(value, Semester):
            return value
        if value == "":
            return Semester()
        if "HACKS!":  # commence hack:
            try:
                seasons = ["Spring", "Summer", "Fall"]
                tmp_season, tmp_year = value.split(" ")
                if tmp_season in seasons:
                    return Semester(tmp_year, "abc"[seasons.index(tmp_season)])
            except:
                pass
        try:
            id = int(value)
        except ValueError as e:
            raise e
        else:
            return semesterFromID(id)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        if isinstance(value, Semester):
            return value.id
        if isinstance(value, int):
            return value
        raise TypeError("Invalid type passed to SemesterField!")


class Department(models.Model):
    """A department/subject"""
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.code

    @property
    def tokens(self):
        """List of single-word strings used to guide search.

        >>> d = Department.objects.create(code="ECON", name="Economics")
        >>> d.tokens
        ['economics', 'econ']
        >>> d.delete()

        >>> d = Department.objects.create(code="CIS",
        ...                               name="Computer and Information Science")
        >>> d.tokens
        ['computer', 'and', 'information', 'science', 'cis']
        >>> d.delete()
        """
        tokens = self.name.lower().split()
        tokens.append(self.code.lower())
        return tokens

    @property
    def datum(self):
        """Response format for search queries.

        >>> d = Department.objects.create(code="ECON", name="Economics")
        >>> d.datum == {'tokens': ['economics', 'econ'],
        ...             'path': '/depts/econ',
        ...             'id': 'ECON',
        ...             'value': 'Economics'}
        True
        >>> d.delete()
        """
        return {'value': self.name,
                'tokens': self.tokens,
                'path': self.get_absolute_url(),
                'id': self.code,
                }

    def get_absolute_url(self):
        # don't know actual semester
        return reverse("department", kwargs={"dept_code": self.code})

    def toShortJSON(self):
        return {
            'id': self.code,
            'name': self.name,
            'path': self.get_absolute_url(),
        }

    def toJSON(self):
        result = self.toShortJSON()

        hists = CourseHistory.objects.filter(
            course__alias__department=self).distinct()
        result[COURSEHISTORY_TOKEN] = [h.toShortJSON() for h in hists]

        # Post 1.0/nice to have, reviews for semester-department.
        result[REVIEW_TOKEN] = {
            'path': "%s/%s" % (self.get_absolute_url(), REVIEW_TOKEN)}

        return result


class CourseHistory(models.Model):
    """A course, as it has existed for many semesters. Various courses
       (several Courses each of CIS 160, CIS 260, CSE 260...) will all
       point to the same CourseHistory if they're all continuations
       of the same course."""
    notes = models.TextField()

    def __unicode__(self):
        return u"CourseHistory ID %d (%s)" % (self.id, self.notes)

    @property
    def aliases(self):
        """all names that this thing is known by"""
        # TODO: shadowing (IE, CIS 260 is not used by another course, don't alias
        # me that way.
        return Alias.objects.filter(course__history=self).only('coursenum', 'department__name')

    def get_absolute_url(self):
        return reverse("history", kwargs={"histid": self.id})

    # name_override: string, or None
    # aliases_override: list of (dept, num) tuple pairs, or None
    # courses_override: list of Course objects, or None

    def toShortJSON(self, name_override=None, aliases_override=None):
        # need to explictly check for None; user may override with empty string/list
        if name_override is None:
            name = self.course_set.all()[:1].get().name
        else:
            name = name_override
        aliases = set(
            alias.course_code for alias in self.aliases) if aliases_override is None else aliases_override
        return {
            'id': self.id,
            'name': name,
            'path': self.get_absolute_url(),
            'aliases': ["%s-%03d" % (code[0], code[1]) for code in aliases]
        }

    def toJSON(self, name_override=None, aliases_override=None, courses_override=None):
        courses = list(self.course_set.all()
                       ) if courses_override is None else courses_override
        response = self.toShortJSON(
            name_override=name_override, aliases_override=aliases_override)
        response[COURSE_TOKEN] = [c.toShortJSON() for c in courses]
        response[REVIEW_TOKEN] = {
            'path': '%s/%s' % (self.get_absolute_url(), REVIEW_TOKEN)}
        return response


class Course(models.Model):
    """A course that can be taken during a particular semester
       (e.g. CIS-120 @2010c). A course may have multiple
       crosslistings, i.e. COGS 001 and CIS 140 are the same
       course.

       The following should be distinct courses (TODO are they?):
       WRIT-039-301 and WRIT-039-303 (they have same course number,
        but different titles)
    """
    semester = SemesterField()  # models.IntegerField() # ID to create a Semester

    # The name of the course
    # e.g. FINANCIAL ACCOUNTING
    name = models.CharField(max_length=200)

    credits = models.FloatField(null=True)
    description = models.TextField()
    history = models.ForeignKey(CourseHistory, null=True)
    oldpcr_id = models.IntegerField(null=True)

    # This is the course's primary cross-listing. In fact, cross-listings are
    # handled at the section level on ISC's side, but we abstract to the course
    # level for simplicity. (This may change.) Should not be null, but must be
    # nullable since it will point back to the Course and one must be
    # inserted first.
    primary_alias = models.ForeignKey(
        'Alias', related_name='courses', null=True)

    def __unicode__(self):
        return "%s %s" % (self.id, self.name)

    @property
    def tokens(self):
        """List of single-word strings used to guide search.

        >>> d = Department.objects.create(code="econ")
        >>> c = Course.objects.create(name="INTRO TO MICRO")
        >>> alias = Alias.objects.create(department=d, course=c, coursenum=001)
        >>> c.primary_alias = alias
        >>> c.tokens == ['econ001', 'econ-001', 'econ', '001', 'intro', 'to', 'micro']
        True
        >>> alias.delete()
        >>> c.delete()
        >>> d.delete()
        """
        tokens = []
        for alias in self.getAliases():
            tokens.append(alias.lower().replace("-", ""))
            tokens.append(alias.lower())
            tokens.extend(alias.lower().split("-"))
        tokens.extend(self.name.lower().split())
        return tokens

    def get_absolute_url(self):
        return reverse("course", kwargs={"courseid": self.id})

    @property
    def code(self):
        return '%s-%03d' % (self.primary_alias.department_id,
                            self.primary_alias.coursenum)

    def getAliases(self):
        return ["%s-%03d" % (x.department_id, x.coursenum)
                for x in self.alias_set.all()]

    def toShortJSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'primary_alias': self.code,
            'aliases': self.getAliases(),
            'path': self.get_absolute_url(),
            'semester': self.semester.code()
        }

    def toJSON(self):
        result = self.toShortJSON()
        path = self.get_absolute_url()
        result.update({
            'credits': self.credits,
            'description': self.description,
            SECTION_TOKEN: {
                'path': '%s/%s' % (path, SECTION_TOKEN),
                RSRCS: [x.toShortJSON() for x in self.section_set.all()],
            },
            REVIEW_TOKEN: {
                'path': '%s/%s' % (path, REVIEW_TOKEN),
            },
            COURSEHISTORY_TOKEN: {'path': reverse("history", kwargs={"histid": self.history_id})},
        })

        return result

    @property
    def datum(self):
        """Response format for search queries.
        >>> d = Department.objects.create(code="econ")
        >>> desc = "Topics in microeconomics."
        >>> c = Course.objects.create(name="INTRO TO MICRO", description=desc)
        >>> alias = Alias.objects.create(department=d, course=c, coursenum=001)
        >>> c.primary_alias = alias
        >>> c.datum == {'tokens': ['econ001', 'econ-001', 'econ', '001', 'intro', 'to', 'micro'],
        ...             'path': '/courses/1',
        ...             'name': 'INTRO TO MICRO',
        ...             'value': 'econ-001',
        ...             'aliases': ['econ-001'],
        ...             'semester': '1740A',
        ...             'description': 'Topics in microeconomics.'}
        True
        >>> alias.delete()
        >>> c.delete()
        >>> d.delete()
        """
        return {
            'value': self.code,
            'name': self.name,
            'tokens': self.tokens,
            'path': self.get_absolute_url(),
            'description': self.description,
            'semester': self.semester.code(),
            'aliases': self.getAliases(),
        }


class Instructor(models.Model):
    """ A course instructor or TA (or "STAFF")"""
    # Leave names able to accept nulls- some professor names have been redacted
    first_name = models.CharField(db_index=True, max_length=80, null=True)
    last_name = models.CharField(db_index=True, max_length=80, null=True)
    # TODO: don't have these yet
    pennkey = models.CharField(max_length=80, null=True)
    email = models.EmailField(max_length=80, null=True)
    # TODO photo?
    website = models.URLField(max_length=200, null=True)
    oldpcr_id = models.IntegerField(null=True)

    @property
    def name(self):
        return (self.first_name or "") + " " + (self.last_name or "")

    @property
    def temp_id(self):
        return re.sub(r"[^\w]", "-", "%d %s" % (self.id, self.name))
        # for pennapps demo only

    @property
    def tokens(self):
        """List single-word strings that can aid in finding this object.

        >>> i = Instructor.objects.create(first_name="Uriel", last_name="Spiegel")
        >>> i.tokens
        ['uriel', 'spiegel']
        >>> i.delete()
        """
        name = self.name or ""
        return name.lower().split()

    def get_absolute_url(self):
        return reverse("instructor", kwargs={"instructor_id": self.temp_id})

    def __unicode__(self):
        return self.name

    @property
    def datum(self):
        """Response format for search queries.

        >>> i = Instructor.objects.create(first_name="Uriel", last_name="Spiegel")
        >>> i.datum == {'tokens': ['uriel', 'spiegel'],
        ...             'path': '/instructors/1-Uriel-Spiegel',
        ...             'value': 'Uriel Spiegel'}
        True
        >>> i.delete()
        """
        return {
            'value': self.name,
            'tokens': self.tokens,
            'path': self.get_absolute_url(),
        }

    def toShortJSON(self):
        return {
            'id': self.temp_id,
            'name': self.name,
            'path': self.get_absolute_url(),
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

    def toJSON(self, extra=[]):
        result = self.toShortJSON()
        result[SECTION_TOKEN] = {
            'path': "%s/%s" % (self.get_absolute_url(), SECTION_TOKEN)}
        if 'sections' in extra:
            result[SECTION_TOKEN][RSRCS] = [x.toShortJSON()
                                            for x in self.section_set.all()]
        result[REVIEW_TOKEN] = {
            'path': "%s/%s" % (self.get_absolute_url(), REVIEW_TOKEN)}
        if 'reviews' in extra:
            result[REVIEW_TOKEN][RSRCS] = [x.toShortJSON()
                                           for x in self.review_set.all()]
        return result


class Alias(models.Model):
    """A (department, number) name for a Course.

    A Course will have as many Aliases as it has crosslistings.
    """

    course = models.ForeignKey(Course)
    department = models.ForeignKey(Department)
    coursenum = models.IntegerField()
    semester = SemesterField()  # redundant; should equal course.semester
    # when importing from registrar , we don't have pcr_id's
    oldpcr_id = models.IntegerField(null=True)

    def __unicode__(self):
        return "%s: %s-%03d (%s)" % (self.course_id,
                                     self.department,
                                     self.coursenum,
                                     self.semester.code()
                                     )

    @property
    def course_code(self):
        """returns something akin to the tuple ('CIS', 120)"""
        return (self.department_id, self.coursenum)


class Section(models.Model):
    """ A section of a Course
    Inherits crosslisting properties from course
    (e.g. if COGS-001 and CIS-140 are Aliases for course 511, then
    COGS-001-401 and CIS-140-401 are "aliases" for section 511-401
    TODO: is this structure guaranteed by the registar?

    TODO: document how group works
    """
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=200)
    sectionnum = models.IntegerField()
    instructors = models.ManyToManyField(Instructor)
    group = models.IntegerField(null=True)
    sectiontype = models.CharField(max_length=3, null=True)
    """ Section type values:
  CLN clinic
  DIS dissertation
  IND independent study
  LAB lab
  LEC lecture
  MST masters thesis
  REC recitation
  SEM seminar
  SRT senior thesis
  STU studio
  """
    # need to allow nulls for when importing from registrat
    oldpcr_id = models.IntegerField(null=True)

    def __unicode__(self):
        return "%s-%03d " % (self.course, self.sectionnum)

    def get_absolute_url(self):
        return reverse("section", kwargs={"courseid": self.course_id, "sectionnum": self.sectionnum})

    class Meta:
        """ To hold uniqueness constraint """
        unique_together = (("course", "sectionnum"),)

    # TODO: Deprecate
    def getAliases(self):
        return self.aliases

    @property
    def aliases(self):
        return ["%s-%03d" % (alias, self.sectionnum)
                for alias in self.course.getAliases()]

    @property
    def api_id(self):
        return "%s-%03d" % (self.course_id, self.sectionnum)

    def toShortJSON(self):
        pri_alias = self.course.primary_alias
        return {
            'id': self.api_id,
            'aliases': self.getAliases(),
            'primary_alias': '%s-%03d-%03d' % (
                pri_alias.department_id, pri_alias.coursenum, self.sectionnum),
            'name': self.name,
            'sectionnum': "%03d" % self.sectionnum,
            'path': self.get_absolute_url(),
        }

    def toJSON(self):
        path = self.get_absolute_url()
        result = self.toShortJSON()
        result.update({
            'group': self.group,
            INSTRUCTOR_TOKEN: [i.toShortJSON() for i in self.instructors.all()],
            'meetingtimes': [x.toJSON() for x in self.meetingtime_set.all()],
            COURSE_TOKEN: self.course.toShortJSON(),
            REVIEW_TOKEN: {
                'path': '%s/%s' % (path, REVIEW_TOKEN),
                RSRCS: [x.toShortJSON() for x in self.review_set.all()]
            },
        })
        return result


class Review(models.Model):
    """ The aggregate review data for a class. """
    section = models.ForeignKey(Section)
    instructor = models.ForeignKey(Instructor)
    forms_returned = models.IntegerField()
    forms_produced = models.IntegerField()
    form_type = models.IntegerField()
    comments = models.TextField()

    class Meta:
        """ To hold uniqueness constraint """
        unique_together = (("section", "instructor"),)

    def __unicode__(self):
        return "Review for %s" % str(self.section)

    def get_absolute_url(self):
        pennkey = self.instructor.temp_id if self.instructor else "99999-JAIME-MUNDO"
        return reverse("review", kwargs={"courseid": self.section.course_id, "sectionnum": self.section.sectionnum, "instructor_id": pennkey})

    def toShortJSON(self):
        return {
            'id': '%s-%s' % (self.section.api_id, self.instructor.temp_id),
            'section': self.section.toShortJSON(),
            'instructor': self.instructor.toShortJSON() if self.instructor_id else None,
            'path': reverse("review", kwargs={"courseid": self.section.course_id, "sectionnum": self.section.sectionnum,
                            "instructor_id": self.instructor.temp_id if self.instructor_id else "99999-JAIME-MUNDO"})
        }

    def toJSON(self):
        result = self.toShortJSON()
        bits = self.reviewbit_set.all()
        result.update({
            'num_reviewers': self.forms_returned,
            'num_students': self.forms_produced,
            'ratings': dict((bit.field, "%1.2f" % bit.score) for bit in bits),
            'comments': self.comments,
        })

        return result


class ReviewBit(models.Model):
    """ A component of a review. """
    review = models.ForeignKey(Review)
    field = models.CharField(max_length=30)
    score = models.FloatField()

    class Meta:
        """ To hold uniqueness constraint """
        unique_together = (("review", "field"),)

    def __unicode__(self):
        return "%s - %s: %s" % (str(self.review), self.field, self.score)


class Building(models.Model):
    """ A building at Penn. """
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=80)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("building", kwargs={"code": self.code})

    def toJSON(self):
        return {
            'id': self.code,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'path': self.get_absolute_url()
        }


class Room(models.Model):
    """ A room in a Building. It optionally may be named. """
    building = models.ForeignKey(Building)
    roomnum = models.CharField(max_length=5)
    name = models.CharField(max_length=80)
    # name is empty string if room doesn't have special name
    # (e.g. Wu and Chen Auditorium), don't bother putting in "LEVH 101"

    class Meta:
        """ To hold uniqueness constraint """
        unique_together = (("building", "roomnum"),)

    def __unicode__(self):
        if self.name != "":
            return self.name
        else:
            return "%s %s" % (self.building, self.roomnum)
        # TODO: change to spaces to hyphens, for consistency w/ courses?


class MeetingTime(models.Model):
    """ A day/time/location that a Section meets. """
    section = models.ForeignKey(Section)
    type = models.CharField(max_length=3)
    day = models.CharField(max_length=1)
    # the time hh:mm is formatted as decimal hhmm, i.e. h*100 + m
    start = models.IntegerField()
    end = models.IntegerField()
    room = models.ForeignKey(Room)

    def __unicode__(self):
        return "%s %s - %s @ %s" % (self.day, self.start, self.end, self.room)

    def toJSON(self):
        return {
            'start': self.start,  # String (e.g. "13:30")
            'end': self.end,  # String (e.g. "15:00")
            'day': self.day,  # String (e.g. "R" for thursday)
            'type': self.type,  # String (e.g. "LEC")
            # TODO FOR AFTER 1.0
            #    'room': {'building': room_building, # building_json output
            #             'id': '%s %s' % (room_building['id'], room_number),
            #             'name': room_name, # String, or None if has no name.
            #             'number': room_number, # String (e.g. "321")
            #             }
        }


class SemesterDepartment:
    """ A (semester, department) pair. Not a model, but treated like one
    for JSON generation purposes. """

    def __init__(self, semester, department):
        self.semester = semester
        self.department = department

    def __unicode__(self):
        return unicode((self.semester, self.department))

    def get_absolute_url(self):
        return reverse("semdept", kwargs={"semester_code": self.semester.code(), "dept_code": self.department.code})

    def toShortJSON(self):
        return {
            'id': self.department.code,  # no department_id here
            'name': self.department.name,
            'path': self.get_absolute_url(),
        }

    def toJSON(self):
        result = self.toShortJSON()

        courses = Course.objects.filter(alias__department=self.department,
                                        semester=self.semester)

        result[COURSE_TOKEN] = [c.toShortJSON() for c in courses]

        return result
