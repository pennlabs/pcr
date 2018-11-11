"""
A Django-specific command for importing course and review data from
ISC's data dumps.

This command (`./manage.py importfromisc`) should be run after ISC's
data dumps have been turned into SQL and loaded into a database.
It will NOT import the qualitative reviews from PCR, that must be done
separately (and after).
"""
__author__ = 'Kyle Hardgrave (kyleh@sas.upenn.edu)'

import time
import traceback

import MySQLdb as db
from django.core.management.base import BaseCommand
from django.conf import settings

from ....courses.models import (Alias, Course, CourseHistory, Department,
                                Instructor, Review, ReviewBit, Section, Semester)


class Command(BaseCommand):
    """A manage.py command to import review data from ISC's DBs.
    We import things in semester-wise chunks so that, if there's an error,
    you hopefully only have to redo one semester. Within each semester,
    we import in three stages:

    1. **Main stage**. The main table has _almost_ everything we need.
         We go through each row that represents a PRIMARY LISTING of a section
         and create (or find) everything from that.
    2. **Aliasing**. After we have all the primary listings, we make another
         pass through the main table and look at every row where the
         PRI_SECTION and SECTION_ID key don't match - i.e., a crosslisting.
         Here we only add the Alias and nothing else - we expect the
         course to exist already.
             Since we were provided with a separate database of crosslistings,
         we optionally make a pass over that as well (`alt_import_aliases`). This
         one tends to have a few cross-listings that weren't covered in the first.
         Even MORE fun, it has DOZENS of crosslistings for courses that don't
         appear to exist. We ignore these. YAY!
    3. **Descriptions**. Because descriptions are stored by course ID ONLY,
         and in a different table, we do these last. These are batch-added to
         any Course that doesn't already have a description.

    Alternatively, if the `--comments` flag is passed, we import the
    qualitative comments - and just those - from a dump of the old PCR.
    This should not be used ever again, but it's there.
    """
    args = '[all | <semester semester ...>]'
    help = 'Imports the given semesters from the ISC database dumps to Django'

    def add_arguments(self, parser):
        parser.add_argument('semester', nargs='*',
                            help=('A list of semesters that should be imported '
                                  '(ex: 2017A). You can either specify all or '
                                  'leave this blank to import all semesters.'))
        parser.add_argument('-a', '--otheraliases', action='store_true',
                            help=('Also check the ISC crosslist table for aliases, '
                                  'not just the normal summary table. Note that '
                                  'this usually doesn\'t end up adding more aliases '
                                  '(and <10 when it does). It also generates a bunch '
                                  '(>20 errors) in trying to crosslist courses '
                                  'that don\'t exist.'))
        parser.add_argument('-c', '--comments', action='store_true',
                            help=('Import the comments from the old-PCR DB dump, '
                                  'not the full course data form ISC. Note that this '
                                  'should only have to be used, like, once. '
                                  'Comments are not part of the import otherwise.'))
        parser.add_argument('-e', '--catcherrors', action='store_true',
                            help='Log errors instead of interrupting the import.')
        parser.add_argument('-d', '--db',
                            help=('An alternate database (uses the IMPORT_DATABASE '
                                  'in settings by default).'))
        parser.add_argument('-p', '--passwd',
                            help='Alternate database password.')
        parser.add_argument('-u', '--user',
                            help='Alternate database username.')

    # NOTE: if importing legacy data (past the past 3 semesters)
    # this should instead be set to TEST_PCR_SUMMARY_HIST_V
    ISC_SUMMARY_TABLE = 'TEST_PCR_SUMMARY_V'
    ISC_RATING_TABLE = 'TEST_PCR_RATING_V'
    ISC_CROSSLIST_TABLE = 'TEST_PCR_CROSSLIST_SUMMARY_V'
    ISC_DESC_TABLE = 'TEST_PCR_COURSE_DESC_V'

    OLDPCR_COURSES = 'coursereview_tblcourses'
    OLDPCR_DEPTS = 'coursereview_tbldepts'
    OLDPCR_LECTURERS = 'coursereview_tbllecturers'
    OLDPCR_REVIEWS = 'coursereview_tbllecturerreviews'

    EARLIEST_TERM = '2002A'

    depts = {}
    num_created = {
        'Alias': 0,
        'Course': 0,
        'CourseHistory': 0,
        'Department': 0,
        'Instructor': 0,
        'Review': 0,
        'ReviewBit': 0,
        'Section': 0,
    }
    num_errors = 0
    total_updated_reviews = 0

    def handle(self, *args, **opts):
        """Handle command line arguments."""
        try:
            self.verbosity = int(opts['verbosity']) if opts['verbosity'] else 1
            self.catch_errors = opts['catcherrors']
            self.just_comments = opts['comments']
            self.import_other_aliases = opts['otheraliases']

            # Set database
            db_name = opts['db'] if opts['db'] else settings.IMPORT_DATABASE_NAME
            db_user = opts['user'] if opts['user'] else settings.IMPORT_DATABASE_USER
            db_pw = opts['passwd'] if opts['passwd'] else settings.IMPORT_DATABASE_PWD
            self._log('Using database %s and user %s' % (db_name, db_user))
            self.db = db.connect(db=db_name, user=db_user, passwd=db_pw)

            # Set the semesters; this also validates the input
            if not opts['semester'] or opts['semester'] == 'all':
                self._log('Importing all available semesters.')
                if not self.just_comments:
                    # We use the semesters in the primary ISC table
                    terms = self.select(['term'], [self.ISC_SUMMARY_TABLE],
                                        conditions=['term > "%s"' %
                                                    self.EARLIEST_TERM],
                                        group_by=['term'], order_by=['term ASC'])
                    semesters = [Semester(term[0]) for term in terms]
                else:
                    # We use the semesters in the PCR comments table
                    terms = self.select(['year', 'semester'], [self.OLDPCR_REVIEWS],
                                        group_by=['year', 'semester'],
                                        order_by=['year ASC', 'semester ASC'])
                    semesters = [Semester(year, semester)
                                 for year, semester in terms]
            else:
                semesters = [Semester(sem_arg) for sem_arg in set(opts['semester'])]
                self._log('Importing the following semesters: {}'.format(semesters))

            # Do the magic
            for sem in semesters:
                self._log('Importing %s' % sem)
                if self.just_comments:
                    self.import_comments(sem)
                else:
                    self.import_reviews(sem)
                    self.import_aliases(sem)
                    if self.import_other_aliases:
                        self.alt_import_aliases(sem)
                self._log('-' * 79)
            if not self.just_comments:
                self.import_descriptions()  # Done in aggregate since not sem-specific

        except KeyboardInterrupt:
            self._err('Aborting...')
            self.db.close()

        # Some helpful info before we leave
        self.print_stats()

    def import_comments(self, sem):
        """Import the comments from the old Penn Course Review dumps and
        sync up with the rest of the data."""

        updated_reviews = 0

        # The select statement here is kept whole to keep the many joins clear.
        # SQL doesn't care about whitespace, so the formatting issues of a
        # multiline string are fine. Similarly, SQL indentation is for clarity,
        # not semantics.
        query_str = """
            SELECT
                depts.dept_code, courses.course_code, reviews.review,
                reviews.lecturer_id, lecturers.last_name, lecturers.first_name
            FROM %s AS reviews
                INNER JOIN %s AS courses ON reviews.course_id = courses.course_id
                INNER JOIN %s AS depts ON courses.dept_id = depts.dept_id
                INNER JOIN %s AS lecturers
                    ON reviews.lecturer_id = lecturers.lecturer_id
            WHERE reviews.year = %d AND reviews.semester = '%s'
            ORDER BY depts.dept_code ASC, courses.course_code ASC
            """ % (self.OLDPCR_REVIEWS, self.OLDPCR_COURSES, self.OLDPCR_DEPTS,
                   self.OLDPCR_LECTURERS, sem.year, sem.seasoncodeABC)

        review_rows = self.query(query_str)
        for (dept_code, course_code, comments,
             prof_id, prof_lname, prof_fname) in review_rows:
            self._log('-' * 20)
            self._log('Loading review for %s-%s @ %s (%s, %s [%d])' % (
                dept_code, course_code, sem.code(), prof_lname, prof_fname, prof_id))

            # Fix types
            course_code = int(course_code)
            prof_id = int(prof_id)
            comments = comments.decode(
                'cp1252', 'ignore').encode('utf-8', 'ignore')

            dept = Department.objects.get(code=dept_code)
            profs = Instructor.objects.filter(oldpcr_id=prof_id)
            sections = Section.objects.filter(instructors__in=profs,
                                              course__semester=sem,
                                              course__alias__department=dept,
                                              course__alias__coursenum=course_code)
            for sect in sections:
                self._log('Processing review for section %s.' % sect, 2)
                review = Review.objects.get(section=sect, instructor__in=profs)
                self._log('Updating comments.' % sect, 2)
                updated_reviews += 1
                review.comments = comments
                review.save()

        self._log('Updated %d reviews in %s.' % (updated_reviews, sem))
        self.total_updated_reviews += updated_reviews

    def import_descriptions(self):
        """Import all the Course descriptions."""
        courses_updated = 0

        fields = ['course_id', 'paragraph_number', 'course_description']
        tables = [self.ISC_DESC_TABLE]
        order_by = ['course_id ASC', 'paragraph_number ASC']
        descriptions = self.select(fields, tables, order_by=order_by)

        def commit_courses(course_id, courses, desc):
            self._log('-' * 20)
            self._log('Adding description for %s to %d courses.' % (
                course_id, courses.count()))
            for course in courses:
                self._log('-> %s: %s...' % (course, desc), 2)
                course.description = desc
                try:
                    course.save()
                except Exception:
                    self._handle_err('Error processing %s:' % course_id)

        # Because course descriptions are stored in separate rows by
        # PARAGRAPH NUMBER, and I don't have the SQL-fu to join them,
        # we have to do some weird logic with the paragraph number.
        full_desc = ''
        courses = None
        last_course_id = ''
        for course_id, paragraph_num, desc in descriptions:
            # Why is this a string? I don't know
            paragraph_num = int(paragraph_num)
            dept_code, course_code, _ = self.parse_sect_str(course_id)
            try:  # Ignore nonexistant departments
                dept = Department.objects.get(code=dept_code)
            except Department.DoesNotExist:
                continue

            if paragraph_num == 1:  # This is the beginning of a new sequence
                if full_desc:  # We have the full previous description; save
                    commit_courses(last_course_id, courses, full_desc)
                    courses_updated += 1
                # Start fresh
                full_desc = '%s\n\n' % desc
                last_course_id = course_id
                courses = Course.objects.filter(primary_alias__department=dept,
                                                primary_alias__coursenum=course_code,
                                                description='')
            else:
                # This is the second (or third or w/e) part of a description - go on
                full_desc += '%s\n\n' % desc

        # Add remaining courses
        commit_courses(last_course_id, courses, full_desc)
        courses_updated += 1

        self._log('Updated %d course descriptions.' % courses_updated)

    def import_reviews(self, sem):
        """Import the given semesters' courses and reviews.

        The main entry-point for importing everything. Note that this only
        imports primary listings, `import_aliases` must be called to handle
        crosslistings.

        Args:
            sem: A Semester object to import, like `Semester(2011, 'A')`.
                If `None`, imports all available semesters.
        """

        main_fields = [  # All fields are strings unless otherwise indicated
            'title', 'pri_section', 'subject_area_desc',
            'instructor_penn_id', 'instructor_fname', 'instructor_lname',
            'enrollment', 'responses', 'form_type',  # <- numbers
        ]
        review_fields = [  # The many rating vectors - all numbers, or null
            'rInstructorQuality', 'rCourseQuality', 'rDifficulty',
            'rCommAbility', 'rStimulateInterest', 'rInstructorAccess',
            'rReadingsValue', 'rAmountLearned', 'rWorkRequired',
            'rRecommendMajor', 'rRecommendNonMajor', 'rArticulateGoals',
            'rSkillEmphasis', 'rHomeworkValuable', 'rExamsConsistent',
            'rAbilitiesChallenged', 'rClassPace', 'rOralSkills',
            'rInstructorConcern', 'rInstructorRapport',
            'rInstructorAttitude', 'rInstructorEffective',
            'rGradeFairness', 'rNativeAbility', 'rTAQuality',
        ]
        tables = [self.ISC_SUMMARY_TABLE]
        # Prevents a few duplicates where the number of responses or from type
        # has changed.
        group_by = ['pri_section',    'instructor_penn_id']
        # We always take the first review with the highest number of responses.
        order_by = ['pri_section ASC',
                    'instructor_penn_id ASC', 'responses DESC']
        conditions = ['pri_section = section_id', 'term = "%s"' % sem.code()]
        reviews = self.select(main_fields + review_fields, tables,
                              conditions=conditions, order_by=order_by,
                              group_by=group_by)
        r = {}  # The dictionary holding all the scores on each iteration

        # Take care to keep this megatuple in sync with the queried fields
        # described above.
        for (title, pri_sect, subj_name,
             prof_id, prof_fname, prof_lname,
             size, responses, form_type,
             r['rInstructorQuality'], r['rCourseQuality'], r['rDifficulty'],
             r['rCommAbility'], r['rStimulateInterest'], r['rInstructorAccess'],
             r['rReadingsValue'], r['rAmountLearned'], r['rWorkRequired'],
             r['rRecommendMajor'], r['rRecommendNonMajor'], r['rArticulateGoals'],
             r['rSkillEmphasis'], r['rHomeworkValuable'], r['rExamsConsistent'],
             r['rAbilitiesChallenged'], r['rClassPace'], r['rOralSkills'],
             r['rInstructorConcern'], r['rInstructorRapport'],
             r['rInstructorAttitude'], r['rInstructorEffective'],
             r['rGradeFairness'], r['rNativeAbility'], r['rTAQuality']
             ) in reviews:

            full_row_str = '%s @ %s (%s, %s)' % (pri_sect, sem.code(),
                                                 prof_lname, prof_fname)
            self._log('-' * 20)
            self._log('Loading %s' % full_row_str)

            try:
                # Fix types
                subj_code, course_code, sect_code = self.parse_sect_str(
                    pri_sect)
                prof_id = int(prof_id)
                # A rare few courses have NULL titles
                title = title or ''

                # Departments.
                dept = self.get_or_create(Department, code=subj_code)
                if not dept.name:  # Only set dept.name if not already set
                    dept.name = subj_name
                    dept.save()

                # CourseHistories. We use the history of the _most recent_
                # course that has the same primary listing.
                try:
                    hist = CourseHistory.objects.filter(
                        course__primary_alias__department=dept,
                        course__primary_alias__coursenum=course_code
                    ).order_by('-course__semester')[0]
                    self._log('Reused CourseHistory: %s' % hist, 2)
                except IndexError:  # Returned empty QuerySet
                    hist = CourseHistory(notes='Created from PCR Course %s-%3d: %s' % (
                        subj_code, course_code, title))
                    hist.save()
                    self._log('Created new CourseHistory: %s' % hist, 2)
                    self.num_created['CourseHistory'] += 1

                # Course + Primary Alias.
                course = self.get_or_create(Course, semester=sem, history=hist)
                alias = self.get_or_create(
                    Alias, course=course, department=dept, coursenum=course_code,
                    semester=sem)
                course.primary_alias = alias  # Resave with non-null primary_alias
                if not course.name:  # Only set course.name if not already set
                    course.name = title
                course.save()

                # Instructor, Section, Review.
                # These are all fairly self-explanatory.
                prof = self.get_or_create(Instructor, oldpcr_id=prof_id)
                if prof.first_name != prof_fname:
                    prof.first_name = prof_fname
                    prof.save()
                if prof.last_name != prof_lname:
                    prof.last_name = prof_lname
                    prof.save()

                sect = self.get_or_create(
                    Section, course=course, name=title, sectionnum=sect_code)
                sect.instructors.add(prof)  # Many-to-many field

                # Reviews. Ignore review data from reviews with no responses,
                # as some have 0's (instead of NULL).
                if responses > 0:
                    review = self.get_or_create(
                        Review, section=sect, instructor=prof, forms_returned=responses,
                        forms_produced=size, form_type=form_type)

                    # ReviewBit. Log these in aggregate - too annoying otherwise.
                    bits_added = 0
                    bits_existing = 0
                    for field in review_fields:
                        if r[field] is not None:  # Many of the review vectors are NULL
                            bit, bit_created = ReviewBit.objects.get_or_create(
                                review=review, field=field, score=r[field])
                            if bit_created:
                                bits_added += 1
                            else:
                                bits_existing += 1
                    self._log('Created %d new ReviewBits. Reused %d.' % (
                        bits_added, bits_existing), 2)
                    self.num_created['ReviewBit'] += bits_added

            except Exception:
                self._handle_err('Error processing %s:' % full_row_str)

        self.print_stats()

    def import_aliases(self, sem):
        """Import the given semesters' crosslistings.

        After calling `import_primary`, this simply makes a second pass
        over the summary table and imports all the crosslistings.

        Args:
            sem: A Semester object to import, like `Semester(2011, 'A')`.
                If `None`, imports all available semesters.
        """
        fields = ['section_id', 'pri_section']
        tables = [self.ISC_SUMMARY_TABLE]
        order_by = ['pri_section ASC']
        conditions = ['pri_section != section_id', 'term = "%s"' % sem.code()]
        aliases = self.select(fields, tables, conditions=conditions,
                              order_by=order_by)

        for sect_id, pri_sect in aliases:
            full_row_str = '%s -> %s @ %s' % (pri_sect, sect_id, sem.code())
            self._log('-' * 20)
            self._log('Crosslisting %s' % (full_row_str))

            try:
                pri_dept_code, pri_coursenum, _ = self.parse_sect_str(pri_sect)
                xlist_dept_code, xlist_coursenum, _ = self.parse_sect_str(
                    sect_id)
                pri_dept = self.get_or_create(Department, code=pri_dept_code)
                xlist_dept = self.get_or_create(
                    Department, code=xlist_dept_code)

                course = Course.objects.get(
                    semester=sem, primary_alias__department=pri_dept,
                    primary_alias__coursenum=pri_coursenum)

                self.get_or_create(
                    Alias, course=course, department=xlist_dept,
                    coursenum=xlist_coursenum, semester=sem
                )

            except Exception:
                self._handle_err('Error cross-listing %s:' % full_row_str)

        self.print_stats()

    def alt_import_aliases(self, sem):
        """Import Aliases for a given semester, using the CROSSLIST_SUMMARY table.

        This does effectively the same thing as `import_aliases`, except
        with the table specific to crosslisting. AFAICT, there are only a
        small number of crosslistings that *only* exist in this table, e.g.,
        six in 2011A.

        Note: This table bizarrely includes crosslistings for a number of
        courses that *don't* appear in the summary table. We avoid these on
        principle (and count/log them at the end).

        There may be a faster way to use both tables using some JOIN magic,
        but for simplicity I've left this as its own function.

        Args:
            sem: A Semester object to import, like `Semester(2011, 'A')`.
                If `None`, imports all available semesters.
        """
        fields = ['section_id', 'xlist_section_id_1', 'xlist_section_id_2',
                  'xlist_section_id_3', 'xlist_section_id_4', 'xlist_section_id_4']
        tables = [self.ISC_CROSSLIST_TABLE]  # Note the difference
        order_by = ['section_id']
        # Ignore sections without any crosslistings:
        conditions = ['xlist_section_id_1 is not null',
                      'term = "%s"' % sem.code()]
        aliases = self.select(fields, tables, conditions=conditions,
                              order_by=order_by)

        xlist_ids = {}  # Store the (up to five) crosslistings from each row
        num_nonexist = 0
        for (sect_id, xlist_ids[1], xlist_ids[2], xlist_ids[3], xlist_ids[4],
             xlist_ids[5]) in aliases:
            self._log('-' * 20)
            self._log('Crosslistng %s @ %s' % (sect_id, sem.code()))

            try:
                # Fix types
                pri_dept_code, pri_coursenum, _ = self.parse_sect_str(sect_id)
                pri_dept = self.get_or_create(Department, code=pri_dept_code)

                try:  # Ignore courses that weren't in the main import
                    course = Course.objects.get(
                        semester=sem, primary_alias__department=pri_dept,
                        primary_alias__coursenum=pri_coursenum)
                except Course.DoesNotExist:
                    self._err(
                        'Tried to crosslist with a course that does not exist!')
                    num_nonexist += 1
                    continue

                for xlist_id in xlist_ids.itervalues():
                    if xlist_id is None:  # Don't waste time when we run out of xlists
                        break
                    self._log('--> Aliasing %s' % xlist_id)

                    xlist_dept_code, xlist_coursenum, _ = self.parse_sect_str(
                        xlist_id)
                    xlist_dept = self.get_or_create(
                        Department, code=xlist_dept_code)

                    self.get_or_create(
                        Alias, course=course, department=xlist_dept,
                        coursenum=xlist_coursenum, semester=sem
                    )

            except Exception:
                self._handle_err('Error cross-listing % @ %s:' %
                                 (sect_id, sem.code()))

        if num_nonexist:  # Report the number of nonexistant at the end.
            self._err('Tried to crosslist with %d nonexist courses.' %
                      num_nonexist)
        self.print_stats()

    # Helpers
    def _handle_err(self, msg):
        """Log unknown errors and print stack trace. That way a random DB error
        won't ruin a long import."""
        if self.catch_errors:
            self._err('-' * 50)
            self._err(msg)
            self._err(traceback.format_exc())
            self.num_errors += 1
        else:
            raise

    def print_stats(self):
        """Print the info on what we've done so far."""
        self._log('-' * 50)
        self._log('New objects: %s' % (
            ', '.join(['%d %s' % (num, model)
                       for model, num in self.num_created.items()])))
        self._log('Updated %d review comments.' % self.total_updated_reviews)
        self._log('Uncaught errors: %d' % self.num_errors)

    def get_or_create(self, model, **kwargs):
        """A wrapper for Django's Model.objects.get_or_create() that does
        some logging. In the case of Department, it hits the cache first
        and updates it if necessary.

        Args:
            model: The Django model, e.g., `Instructor`.
            kwargs: The same keyword args passed to the original.

        Returns:
            A Model instance.
        """
        is_dept = model == Department
        if is_dept:  # For departments, check the cache
            dept_code = kwargs['code']
            try:
                dept = self.depts[dept_code]
            except KeyError:
                pass
            else:
                self._log('Reused cached Department %s: %s' %
                          (dept.code, dept.name), 2)
                return dept

        name = model.__name__
        obj, created = model.objects.get_or_create(**kwargs)
        if created:
            self._log('Created new %s: %s' % (name, obj), 2)
            self.num_created[name] += 1
        else:
            self._log('Reused existing %s: %s' % (name, obj), 2)

        if is_dept:  # Update Department cache
            self.depts[obj.code] = obj

        return obj

    def parse_sect_str(self, section_str):
        """Turn a DB section or course string into a nice tuple.
        'CIS 120001' -> ('CIS', 125, 1). 'CIS 099' -> ('CIS', 99, None)

        In the DB, the strings are always 10 characters (or 7 for courses),
        and padded with spaces based on the length of the deparment code.
        """
        try:
            sect_code = int(section_str[7:10])
        except ValueError:
            sect_code = None
        try:
            course_code = int(section_str[4:7])
        except ValueError:
            course_code = None
        return (section_str[0:4].strip(), course_code, sect_code)

    def query(self, query_str, args=None):
        """A simple wrapper for our MySQL queries."""
        start = time.time()
        self._log('Executing query: "%s"' % query_str, 2)
        cursor = self.db.cursor()
        cursor.execute(query_str, args)
        results = cursor.fetchall()
        self._log('Took: %s' % (time.time() - start), 2)
        self._log('Founds %s results.' % len(results), 2)
        return results

    def select(self, fields, tables, conditions=None, group_by=None,
               order_by=None):
        """A wrapper for MySQL SELECT queries.

        Args:
            fields: List of database row names
            tables: List of database table names
            conditions: Map of field-value pairs to filter by
            group_by: List of fields to group (aggregate) by
            order_by: List of fields to order by
        """
        query = ["SELECT", ", ".join(fields), "FROM", ", ".join(tables)]

        if conditions:
            query.extend(["WHERE", " AND ".join(conditions)])

        if group_by:
            query.extend(["GROUP BY", ", ".join(group_by)])

        if order_by:
            query.extend(["ORDER BY", ", ".join(order_by)])

        return self.query(" ".join(query))

    def _log(self, msg, v=1):
        """Log messages to standard out, depending on the verbosity."""
        if self.verbosity >= v:
            self.stdout.write('%s\n' % msg)

    def _err(self, msg):
        """Log errors to stderr, regardless of verbosity."""
        self.stderr.write('ERR: %s\n' % msg)
