from django.db import models


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
          3(Y-1740) + s = 780 + 3(Y-2000) + s
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

    @staticmethod
    def semesterFromID(val):
        """ Given a numerical semester ID, return a semester. """
        if isinstance(val, Semester):
            return val
        return Semester(1740 + val / 3, "abc"[val % 3])

    @staticmethod
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
        if value is None:
            return value
        if value == "":
            return Semester()
        if isinstance(value, int):
            return Semester.semesterFromID(value)
        if "HACKS!":  # commence hack:
            try:
                seasons = ["Spring", "Summer", "Fall"]
                tmp_season, tmp_year = value.split(" ")
                if tmp_season in seasons:
                    return Semester(tmp_year, "abc"[seasons.index(tmp_season)])
            except KeyError:
                pass
        try:
            return Semester.semesterFromID(int(value))
        except ValueError as e:
            raise e

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

    def __str__(self):
        return self.code


class CourseHistory(models.Model):
    """A course, as it has existed for many semesters. Various courses
       (several Courses each of CIS 160, CIS 260, CSE 260...) will all
       point to the same CourseHistory if they're all continuations
       of the same course."""
    notes = models.TextField()

    def __str__(self):
        return u"CourseHistory ID %d (%s)" % (self.id, self.notes)

    @property
    def aliases(self):
        """all names that this thing is known by"""
        # TODO: shadowing (IE, CIS 260 is not used by another course, don't alias
        # me that way.
        return Alias.objects.filter(course__history=self).only('coursenum', 'department__name')

    # name_override: string, or None
    # aliases_override: list of (dept, num) tuple pairs, or None
    # courses_override: list of Course objects, or None


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

    description = models.TextField()
    history = models.ForeignKey(CourseHistory, null=True, on_delete=models.CASCADE)

    # This is the course's primary cross-listing. In fact, cross-listings are
    # handled at the section level on ISC's side, but we abstract to the course
    # level for simplicity. (This may change.) Should not be null, but must be
    # nullable since it will point back to the Course and one must be
    # inserted first.
    primary_alias = models.ForeignKey(
        'Alias', related_name='courses', null=True, on_delete=models.PROTECT)

    def __str__(self):
        return "%s %s" % (self.id, self.name)

    @property
    def code(self):
        return '%s-%03d' % (self.primary_alias.department_id,
                            self.primary_alias.coursenum)


class Instructor(models.Model):
    # A course instructor or TA (or "STAFF")
    # Leave names able to accept nulls- some professor names have been redacted
    first_name = models.CharField(db_index=True, max_length=80, null=True)
    last_name = models.CharField(db_index=True, max_length=80, null=True)
    # TODO: don't have these yet
    pennkey = models.CharField(max_length=80, null=True)
    email = models.EmailField(max_length=80, null=True)
    # TODO photo?
    website = models.URLField(max_length=200, null=True)

    @property
    def name(self):
        return "{} {}".format(self.first_name or "", self.last_name or "").strip()

    @property
    def code(self):
        return "{}-{}-{}".format(self.id, self.first_name.upper() or "", self.last_name.upper() or "")

    @property
    def departments(self):
        return Department.objects.filter(aliases__course__sections__instructors=self)

    def __str__(self):
        return self.name


class Alias(models.Model):
    """A (department, number) name for a Course.
    A Course will have as many Aliases as it has crosslistings.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="aliases")
    coursenum = models.IntegerField()

    def __str__(self):
        return "%s: %s-%03d" % (self.course_id,
                                     self.department,
                                     self.coursenum
                                     )

    @property
    def course_code(self):
        """returns something akin to the tuple ('CIS', 120)"""
        return ("{}-{}".format(self.department_id, self.coursenum))


class Section(models.Model):
    """ A section of a Course
    Inherits crosslisting properties from course
    (e.g. if COGS-001 and CIS-140 are Aliases for course 511, then
    COGS-001-401 and CIS-140-401 are "aliases" for section 511-401
    TODO: is this structure guaranteed by the registar?

    TODO: document how group works
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=200)
    sectionnum = models.IntegerField()
    instructors = models.ManyToManyField(Instructor, related_name="sections")
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
    # and a few others, online course, NSO proseminar, SCUE preceptorial

    def __str__(self):
        return "%s-%03d " % (self.course, self.sectionnum)

    class Meta:
        """ To hold uniqueness constraint """
        unique_together = (("course", "sectionnum"),)


class Review(models.Model):
    """ The aggregate review data for a class. """
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="reviews")
    forms_returned = models.IntegerField()
    forms_produced = models.IntegerField()
    form_type = models.IntegerField()
    comments = models.TextField()

    class Meta:
        """ To hold uniqueness constraint """
        unique_together = (("section", "instructor"),)

    def __str__(self):
        return "Review for %s" % str(self.section)


class ReviewBit(models.Model):
    """ A component of a review. """
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    field = models.CharField(max_length=30)
    score = models.FloatField()

    class Meta:
        """ To hold uniqueness constraint """
        unique_together = (("review", "field"),)

    def __str__(self):
        return "%s - %s: %s" % (str(self.review), self.field, self.score)
