from lib.api import api


# we use this to provide data in the case that a course doesn't have lectures
# if a course doesn't, it will attempt to show seminar data, else lab data, else recitation data
# TODO: use this
TYPE_RANK = ('LEC', 'SEM', 'LAB', 'REC')


# python 2/3 compatibility
def cmp(x, y):
    return (x > y) - (x < y)


class ComparableMixin(object):
    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0


class Review(ComparableMixin, object):
    def __init__(self, rid):
        tokens = rid.split("-")
        # NOTE: Since a professor's name is hyphen separated we have to be careful
        course_id, section_id, instructor_id = tokens[0], tokens[1], "-".join(
            tokens[2:])
        try:
            raw_self = api('courses', course_id, 'sections',
                           section_id, 'reviews', instructor_id)
        except ValueError as e:
            raise e
        else:
            self.id = raw_self['id']
            self.comments = raw_self['comments']
            self.num_students = raw_self['num_students']
            self.num_reviewers = raw_self['num_reviewers']
            self.ratings = dict((k, float(v))
                                for k, v in raw_self['ratings'].items())
            self.__instructor_id = raw_self['instructor']['id']
            self.__section_id = raw_self['section']['id']

    @property
    def instructor(self):
        return Instructor(self.__instructor_id)

    @property
    def section(self):
        return Section(self.__section_id)

    def __cmp__(self, other):
        return cmp(self.id, other.id)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "Review(%s)" % self.id


class Instructor(ComparableMixin, object):
    def __init__(self, iid):
        try:
            raw_self = api('instructors', iid)
        except ValueError as e:
            raise e
        else:
            self.id = raw_self['id']
            self.name = raw_self['name']
            self.__section_ids = set(
                section['id'] for section in raw_self['sections']['values'])
            self.__review_ids = set(review['id']
                                    for review in raw_self['reviews']['values'])

    @property
    def last_name(self):
        return self.name.split()[-1]

    @property
    def sections(self):
        return set(Section(section_id) for section_id in self.__section_ids)

    @property
    def reviews(self):
        return set(Review(review_id) for review_id in self.__review_ids)

    def taught(self, course):
        """Check if an instructor taught a course."""
        for section in self.sections:
            if section.course == course:
                return True
        return False

    def __cmp__(self, other):
        return cmp(self.id, other.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "Instructor(%s)" % self.name


class Section(ComparableMixin, object):
    def __init__(self, sid):
        course_id, section_id = sid.split("-")
        try:
            raw_self = api('courses', course_id, 'sections', section_id)
        except ValueError as e:
            raise e
        else:
            self.id = raw_self['id']
            self.name = raw_self['name']
            self.sectionnum = raw_self['sectionnum']
            # TODO: Request change
            self.__course_id = raw_self['courses']['id']
            self.__instructor_ids = set(
                instructor['id'] for instructor in raw_self['instructors'])
            self.__review_ids = set(review['id']
                                    for review in raw_self['reviews']['values'])

    @property
    def course(self):
        return Course(self.__course_id)

    @property
    def instructors(self):
        return set(Instructor(instructor_id) for instructor_id in self.__instructor_ids)

    @property
    def reviews(self):
        return set(Review(review_id) for review_id in self.__review_ids)

    def __cmp__(self, other):
        return cmp(self.id, other.id)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "Section(%s)" % self.id


class Course(ComparableMixin, object):
    def __init__(self, cid):
        try:
            raw_self = api('courses', cid)
        except ValueError as e:
            raise e
        else:
            self.id = raw_self['id']
            self.aliases = set(alias for alias in raw_self['aliases'])
            self.primary_alias = raw_self['primary_alias']
            self.description = raw_self['description']
            self.semester = raw_self['semester']
            self.__coursehistory_id = raw_self['coursehistories']['path'].split(
                "/")[-1]
            self.__section_ids = set(
                section['id'] for section in raw_self['sections']['values'])

    @property
    def coursehistory(self):
        return CourseHistory(self.__coursehistory_id)

    @property
    def sections(self):
        return set(Section(section_id) for section_id in self.__section_ids)

    @property
    def url(self):
        return "courses/%s" % self.id

    def __cmp__(self, other):
        return cmp(self.id, other.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return 'Course(%s)' % self.id


class CourseHistory(ComparableMixin, object):
    def __init__(self, chid):
        # constructor id can either be one if its aliases, or numeric id
        try:
            raw_self = api('coursehistories', chid)
        except ValueError as e:
            raise e
        else:
            self.id = raw_self['id']
            self.aliases = set(raw_self['aliases'])
            self.name = raw_self['name']  # ie PROG LANG AND TECH II
            self.__course_ids = set(course['id']
                                    for course in raw_self['courses'])

    @property
    def courses(self):
        return set(Course(course_id) for course_id in self.__course_ids)

    @property
    def most_recent(self):
        for course in sorted(self.courses, key=lambda c: c.semester, reverse=True):
            return course

    def alias(self, instructor=None):
        """
        Get the primary alias of the course history in relation to an
        instructor. If instructor is None, get the most recent primary
        alias.
        """
        if instructor is None:
            return self.most_recent.primary_alias
        else:
            # Find the most recent course taught by an instructor
            for course in sorted(self.courses, key=lambda c: c.semester, reverse=True):
                if instructor.taught(course):
                    return course.primary_alias
            raise ValueError("instructor never taught course")

    @property
    def description(self):
        # NOTE: we cannot use most recent here because courses are not
        # guaranteed to have a description.
        for course in sorted(self.courses, key=lambda c: c.semester, reverse=True):
            if course.description:
                return course.description
        return None

    def __eq__(self, other):
        return self.id == other.id

    def __cmp__(self, other):
        return cmp(self.id, other.id)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return 'CourseHistory(%s)' % self.id


class Department(object):
    def __init__(self, name):
        try:
            raw_self = api('depts', name)
        except ValueError as e:
            raise e
        else:
            self.raw_self = raw_self
            self.id = raw_self['id']
            self.name = raw_self['name']

    @property
    def coursehistories(self):
        return set(CourseHistory(ch['id']) for ch in self.raw_self['coursehistories'])
