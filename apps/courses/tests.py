"""
Tests for the API views.

These are run by `./manage.py test`.
"""
import json
import requests

from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from api.apiconsumer.models import APIConsumer
from models import (Alias, Course, CourseHistory, Department, Instructor,
                    Section, Review, ReviewBit)


class ViewTest(TestCase):
    """A test of the API views (i.e., the JSON served by the API).

    Attributes:
      consumer: An APIConsumer object, for querying the API.
      client: A Django test client, for making basic HTTP calls.
    """

    def setUp(self):
        """Set up the necessary objects for testing.

        If overrided in a subclass, be sure to call
        `super(ChildTest, self).setUp()` to create the consumer and client.
        """
        self.consumer = APIConsumer.objects.create(
            name="test",
            email="test@test.com",
            description="",
            token="root",
            permission_level=9001
        )
        self.client = Client()

    def get_result(self, path):
        """Load a page on the API and return the result.

        Fails on inability to parse json or invalid content.
        """
        response = self.client.get(path, {'token': self.consumer.token})
        try:
            content = json.loads(response.content)
        except ValueError as e:
            self.fail("%s (s=\"%s\")" % (e, response.content))
        self.assertTrue(content['valid'], content)
        return content['result']


class DataTest(ViewTest):
    """Test the basic integrity of the API structure."""

    def setUp(self):
        super(DataTest, self).setUp()

        cis = Department.objects.create(
            code='CIS', name='Computer Science')
        ese = Department.objects.create(
            code='ESE', name='Electrical Engineering')
        cis110 = CourseHistory.objects.create(notes="None.")
        self.histid = cis110.id
        cis110_1 = Course.objects.create(
            semester=810,
            name="CIS 110",
            credits=1.0,
            description="intro to CS.",
            history=cis110
        )
        self.courseid = cis110_1.id
        instructor1 = Instructor.objects.create(
            first_name="John", last_name="Doe")
        section1 = Section.objects.create(
            course=cis110_1, name="Intro to CS",
            sectionnum='001', sectiontype='LEC')
        self.sectionid = section1.sectionnum
        alias1 = Alias.objects.create(
            course=cis110_1, department=cis, coursenum=1, semester=810)
        alias2 = Alias.objects.create(
            course=cis110_1, department=ese, coursenum=1, semester=810)
        cis110_1.primary_alias = alias1
        cis110_1.save()
        review1 = Review.objects.create(
            section=section1, instructor=instructor1,
            forms_returned=10, forms_produced=20, form_type=1,
            comments="Students enjoyed the course.")
        reviewbit1 = ReviewBit.objects.create(
            review=review1, field="Instructor Quality", score=3.0)
        reviewbit2 = ReviewBit.objects.create(
            review=review1, field="Difficulty", score=1.0)
        reviewbit3 = ReviewBit.objects.create(
            review=review1, field="Course Quality", score=2.0)

    def validate_results(self, path):
        """Check that there are, in fact, results."""
        result = self.get_result(path)
        self.assertTrue(len(result['values']) > 0, result)

    def test_presence_of_depts(self):
        self.validate_results('/depts')

    def test_dept_should_have(self):
        result = self.get_result('/depts/CIS')
        self.assertTrue("coursehistories" in result)
        self.assertTrue("id" in result)
        self.assertTrue("name" in result)
        self.assertTrue("path" in result)
        self.assertTrue("reviews" in result)

    def test_coursehistory_should_have(self):
        result = self.get_result('/coursehistories/{}'.format(self.histid))
        self.assertTrue("aliases" in result)
        self.assertTrue("courses" in result)
        self.assertTrue("id" in result)
        self.assertTrue("name" in result)
        self.assertTrue("path" in result)
        self.assertTrue("reviews" in result)

    def test_presence_of_instructors(self):
        self.validate_results('/instructors')

    def test_instructor_should_have(self):
        instructor = Instructor.objects.all()[0]
        result = self.get_result(instructor.get_absolute_url())
        self.assertTrue("id" in result)
        self.assertTrue("name" in result)
        self.assertTrue("path" in result)
        self.assertTrue("reviews" in result)

    def test_course_should_have(self):
        result = self.get_result('/courses/{}'.format(self.histid))
        self.assertTrue("aliases" in result)
        self.assertTrue("coursehistories" in result)
        self.assertTrue("credits" in result)
        self.assertTrue("description" in result)
        self.assertTrue("id" in result)
        self.assertTrue("name" in result)
        self.assertTrue("path" in result)
        self.assertTrue("reviews" in result)
        self.assertTrue("sections" in result)
        self.assertTrue("semester" in result)

    def test_presence_of_course_reviews(self):
        self.validate_results('/courses/{}/reviews'.format(self.courseid))

    def test_presence_of_sections(self):
        self.validate_results('/courses/{}/sections'.format(self.courseid))

    def test_section_should_have(self):
        result = self.get_result('/courses/{}/sections/{}/'.format(self.courseid, self.sectionid))
        self.assertTrue("aliases" in result)
        self.assertTrue("courses" in result)
        self.assertTrue("group" in result)
        self.assertTrue("id" in result)
        self.assertTrue("instructors" in result)
        self.assertTrue("meetingtimes" in result)
        self.assertTrue("name" in result)
        self.assertTrue("path" in result)
        self.assertTrue("reviews" in result)
        self.assertTrue("sectionnum" in result)

    def test_presence_of_section_reviews(self):
        self.validate_results('/courses/{}/sections/{}/reviews'.format(self.courseid, self.sectionid))

    def test_review_should_have(self):
        result = self.get_result('/courses/{}/sections/{}/reviews'.format(self.courseid, self.sectionid))
        review = result['values'][0]

        self.assertTrue("comments" in review)
        self.assertTrue("id" in review)
        self.assertTrue("instructor" in review)
        self.assertTrue("num_reviewers" in review)
        self.assertTrue("num_students" in review)
        self.assertTrue("path" in review)
        self.assertTrue("ratings" in review)
        self.assertTrue("section" in review)

        comments = review['comments']
        instructor = review['instructor']
        ratings = review['ratings']
        num_reviewers = review['num_reviewers']
        num_students = review['num_students']
        section = review['section']

        self.assertTrue(comments != "null", msg=comments)
        self.assertTrue(len(comments) > 0, msg=comments)
        self.assertTrue(instructor['name'] == "John Doe", msg=instructor)
        self.assertTrue(len(ratings) > 0, msg=result)
        self.assertTrue(int(num_reviewers) > 0)
        self.assertTrue(int(num_students) > 0)
        self.assertTrue(section['sectionnum'] == '001')

    def test_presence_of_semesters(self):
        self.validate_results('/semesters')

    def test_forward_slash_depts(self):
        self.validate_results('/depts/')

    def test_forward_slash_instructors(self):
        self.validate_results('/instructors/')

    def test_forward_slash_coursehistories(self):
        self.validate_results('/coursehistories/')

    def test_forward_slash_semesters(self):
        self.validate_results('/semesters/')


class LiveViewTest(TestCase):
    """A test of the live API views.

    Because Django creates an empty database for testing, we use an
    actual HTTP request instead of Django's django.test.client.Client
    so that we can see actual data.

    Attributes:
      root_path: The root path where this API is serving.
      token: The access token used for testing. Should have permissions
        set to 9001 and be defined in settings.
    """

    def setUp(self):
        # TODO(kyleh): Factor this out
        self.root_path = 'http://api.penncoursereview.com/v1'
        self.token = settings.TEST_API_TOKEN

    def get_result(self, path):
        """Load a page of the live API and return the result."""
        full_path = self.root_path + path
        response = requests.get(full_path, params={'token': self.token})
        content = response.json()
        self.assertEquals(
            response.status_code, requests.codes.ok,
            'Server response error to %s: %s' % (full_path, response.status_code))
        self.assertTrue(content is not None, 'Response not parsable JSON')
        self.assertTrue(content['valid'], 'Response is not valid')
        return content['result']

    def get_course_path(self, semester, course_code):
        """Get a course's absolute path.

        Args:
          semester: The semester to search in the form '2011A' = Spring 2011
          course_code: The target course in the form 'CIS-125'
        """
        # TODO(kyleh): We assume that there is only one course with the
        # course_code in the given semester. May not be a safe assumption.
        search_path = '/semesters/%s/%s' % (semester.lower(),
                                            course_code.split('-')[0])
        return [course['path']
                for course in self.get_result(search_path)['courses']
                if course_code in course['aliases']][0]


class CrossListingTest(LiveViewTest):
    """Test that courses are being properly crosslisted.

    In many places, a course that shoud be counted once is being listed
    as several different courses. We test that this is not happening.
    """

    def setUp(self):
        super(CrossListingTest, self).setUp()

    def check_crosslist(self, semester, primary_listing, aliases):
        """Test for proper cross-listing behavior.

        Args:
          semester: A semester in the form '2011A' = Spring 2011
          primary_listing: The primary listing of the course in the form 'CIS-125'
          aliases: A list of aliases in the form 'DEPT-123'
        """
        # TODO(kyleh): When we add a primary listing field to the API,
        # update this test accordingly.
        main_path = self.get_course_path(semester, primary_listing)
        main_data = self.get_result(main_path)
        for alias in aliases:
            alias_path = self.get_course_path(semester, alias)
            self.assertEquals(
                main_path, alias_path,
                'Path for %s (%s) and alias %s (%s) differ.' % (
                    primary_listing, main_path, alias, alias_path
                )
            )
            self.assertTrue(
                alias in main_data['aliases'],
                '%s does not contain %s as an alias.' % (
                    primary_listing, alias)
            )

    def test_phil228_ppe228(self):
        """Test that PHIL-228 is a cross-listing of PPE-228 in 2009A."""
        self.check_crosslist('2009A', 'PHIL-228', ['PPE-228'])

    def test_cis125_eas125(self):
        """Test that EAS125 is a cross-listing of CIS-125 in 2011A."""
        self.check_crosslist('2011A', 'CIS-125', ['EAS-125'])

    def test_jarosinski(self):
        """Test the many cross-listings of Jarosinski's COML-501 in 2009C."""
        self.check_crosslist('2009C', 'COML-501',
                             ['CLST-511', 'ROML-512', 'GRMN-534', 'SLAV-500',
                              'ENGL-573'])


class CourseHistoryTest(LiveViewTest):
    """Test that courses are being properly aggregated into histories.

    This is somewhat hard to be 100% on as it's not an entirely clear-
    cut issue. But we at least have some examples.
    """

    def setUp(self):
        super(CourseHistoryTest, self).setUp()

    def test_cis160_cis260_cse260(self):
        """Test that CIS-160, CIS-260, and CSE-260 are in the same history."""
