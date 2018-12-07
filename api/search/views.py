"""
The modules implement the PennCourseReview search endpoint.
"""
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_GET

from ..json_helpers import JSON
from ..courses.models import Alias, Department, Instructor

# Field name for the query value
QUERY_FIELD = 'q'
# Field name for the result type value
RESULT_TYPE_FIELD = 'result_type'
# Field name for the count field value
COUNT_FIELD = 'count'
# Field name for the page field value
PAGE_FIELD = 'page'


class ResultType(object):
    MIXED = 'mixed'
    COURSES = 'courses'
    INSTRUCTORS = 'instructors'
    DEPARTMENTS = 'departments'


RESULT_TYPES = [ResultType.MIXED, ResultType.COURSES, ResultType.INSTRUCTORS,
                ResultType.DEPARTMENTS]


# The type of results to fetch
DEFAULT_RESULT_TYPE = ResultType.MIXED
# The default number of results to return per page
DEFAULT_COUNT = 15
# The default page to fetch
DEFAULT_PAGE = 0


@require_GET
def search(request):
    """Handle a request to the search endpoint.
    Return :class:HttpResponse object.

    :param request: a Django request
    """
    try:
        if QUERY_FIELD not in request.GET:
            raise ValueError("expected `q`, got %s" % request.GET.keys())
        q = request.GET[QUERY_FIELD]

        result_type = request.GET.get(RESULT_TYPE_FIELD, DEFAULT_RESULT_TYPE)
        if result_type not in RESULT_TYPES:
            raise ValueError("invalid result type: '%s'" % result_type)

        count = _nat(request.GET.get(COUNT_FIELD, DEFAULT_COUNT))
        page = _nat(request.GET.get(PAGE_FIELD, DEFAULT_PAGE))
    except ValueError as e:
        return HttpResponseBadRequest(e)

    return JSON(_get_datasets(q, result_type, count, page))


def _get_datasets(q, result_type, count, page):
    """Fetch multiple datasets that are relevant to `q`.

    :param q: A search query
    :param result_type: Either 'mixed', 'courses', 'instructors', or
                        'departments'. Controls what types of results are
                        returned.
    :param count: The number of results to return per page
    :param page: The page to fetch
    """
    datasets = {}
    offset = page * count

    if result_type in (ResultType.MIXED, ResultType.COURSES):
        datasets['courses'] = _retrieve_courses(q, offset + count)
    if result_type in (ResultType.MIXED, ResultType.INSTRUCTORS):
        datasets['instructors'] = _retrieve_instructors(q, offset + count)
    if result_type in (ResultType.MIXED, ResultType.DEPARTMENTS):
        datasets['departments'] = _retrieve_departments(q, offset + count)

    for k, dataset in datasets.items():
        datasets[k] = [obj.datum for obj in dataset[offset:]]
    return datasets


def _retrieve_courses(q, count):
    """Retrieve a list of `count` unique Courses that are relevant to `q`.

    :param q: A search query
    :param count: The number of results to return
    """
    # Generate a list of `count` courses, whose name, department name, or
    # department code matches `q` or a token in `q`,
    # first listing courses whose coursenum matches a token in `q`,
    # then listing courses whose department code or department name matches
    # a token in q,
    # then listing courses whose name matches `q`.

    tokens = set(q.split() + q.split("-"))

    # split queries at the first number to handle cases like "cis110" or
    # "econ001"
    try:
        i = _index_digit(q)
    except ValueError:
        pass
    else:
        tokens.add(q[:i])
        tokens.add(q[i:])

    q1 = Q(course__name__icontains=q)
    q2 = Q(department__code__in=tokens)
    q3 = Q(department__name__in=tokens)
    nums = []
    for token in tokens:
        try:
            num = int(token)
        except ValueError:
            pass
        else:
            nums.append(num)
    q4 = Q(coursenum__in=nums)
    a1 = (Alias.objects.filter(q1 | q2 | q3)
          .order_by("coursenum")
          .order_by("-semester"))
    r0 = [a.course for a in a1.filter(q4)[:count]]
    r1 = [a.course for a in a1.exclude(q4).filter(q2 | q3)[:count - len(r0)]]
    r2 = [a.course
          for a in a1.exclude(q2 | q3 | q4)[:count - len(r0) - len(r1)]]
    return r0 + r1 + r2


def _retrieve_instructors(q, count):
    """Retrieve a list of `count` unique Instructors that are relevant to `q`.

    :param q: A search query
    :param count: The number of results to return
    """
    # Generate a list of `count` instructors,

    # This function generates a list of <= count instructors, first listing instructors
    # whose first AND last names match q, and second listing instructors whose
    # first OR last names matches a term in q.

    r = list()
    words = q.split()

    q_all = Q()

    for word in words:
        q_all |= Q(last_name__istartswith=word) | Q(
            first_name__istartswith=word)

    r_all = Instructor.objects.filter(q_all)

    if len(words) == 2:
        q0 = Q(last_name__istartswith=words[1]) & Q(
            first_name__istartswith=words[0])
        q1 = Q(last_name__istartswith=words[0]) & Q(
            first_name__istartswith=words[1])

        r += list(r_all.filter(q0)[:count])
        r += list(r_all.filter(q1)[:count - len(r)])

        r_all = r_all.exclude(q0 | q1)

    # We assume the query does not contain identical words, which we expect to generate duplicates
    for i, word in enumerate(words):
        q1 = Q(last_name__istartswith=word)
        q2 = Q(first_name__istartswith=word)

        # Given that the query is 'Adam Grant' we consider results with "Adam" in the first name
        # more relevant than results with "Adam" in the last name, and vice-versa for "Grant"
        if i == 0:
            r += list(r_all.filter(q2)[:count - len(r)])
            r += list(r_all.filter(q1)[:count - len(r)])
        else:
            r += list(r_all.filter(q1)[:count - len(r)])
            r += list(r_all.filter(q2)[:count - len(r)])

        if len(r) == count:
            break
    return r


def _retrieve_departments(q, count):
    """Retrieve a list of `count` unique Departments that are relevant to `q`.

    :param q: A search query
    :param count: The number of results to return
    """
    # Do not prioritize departments. There are so few it's not meaningful.
    q1 = Q(name__istartswith=q) | Q(code__istartswith=q)
    r0 = Department.objects.filter(q1)[:count]
    return r0


def _nat(n):
    """Convert a string to a natural number.

    :param n: a string to convert
    """
    n = int(n)
    if n < 0:
        raise ValueError("could not convert string to natural: '%s'" % n)
    return n


def _index_digit(s):
    """Find the index of the first digit in `s`.

    :param s: a string to scan

    Raises a ValueError if no digit is found.
    """
    for i, c in enumerate(s):
        if c.isdigit():
            return i
    raise ValueError("digit not found")
