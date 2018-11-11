import json

from collections import defaultdict
from django.http import HttpResponse
from django.shortcuts import redirect, reverse

from .utils import current_semester, API404
from ..json_helpers import JSON
from .models import (Course, Department, Review, Alias, Building, CourseHistory,
                     Section, Instructor, SemesterDepartment, semesterFromID,
                     semesterFromCode, )
from .links import RSRCS

DOCS_URL = 'http://pennlabs.org/console/docs.html'
DOCS_HTML = "<a href='%s'>%s</a>" % (DOCS_URL, DOCS_URL)


def course_histories(request):
    if not request.consumer.access_secret:
        # This method is for the PCR site only.
        raise API404("This is not the database dump you are looking for.")

    # 1. get and aggregate all course alias data
    alias_fields = ['coursenum', 'department__code',
                    'course__history', 'course__name']
    query_results = Alias.objects.select_related(
        *alias_fields).values(*alias_fields)

    # Note: Some courses have no aliases (probably an import script bug).
    # This function will not see those courses (we don't really want to anyway),
    # so we have hist_to_name default to "" (if it defaulted to None, then
    # name_override would not happen and it would fetch their real names and that
    # would be slow)
    hist_to_aliases = defaultdict(set)
    hist_to_name = defaultdict(lambda: "")
    for e in query_results:
        hist_to_aliases[e['course__history']].add(
            (e['department__code'], e['coursenum']))
        hist_to_name[e['course__history']] = (e['course__name'])

    # don't include course histories that are only offered this semester
    old_course_history_ids = [x[0] for x in Course.objects
                              .filter(semester__lt=current_semester())
                              .select_related('history')
                              .values_list('history')
                              .distinct()]

    hists = CourseHistory.objects.filter(id__in=old_course_history_ids)
    course_histories = [h.toShortJSON(name_override=hist_to_name[h.id],
                                      aliases_override=hist_to_aliases[h.id])
                        for h in hists]

    # Union-find approach to removing duplicates, code from
    # Stack Overflow: http://stackoverflow.com/a/42183579
    dict_histories = merge_union(course_histories)

    return JSON({RSRCS: dict_histories})

# Return ancestor of given node


def ancestor(parent, node):
    if parent[node] != node:
        # Do path compression
        parent[node] = ancestor(parent, parent[node])

    return parent[node]


def merge(parent, rank, x, y):
    # Merge sets that x & y belong to
    x = ancestor(parent, x)
    y = ancestor(parent, y)

    if x == y:
        return

    # Union by rank, merge smaller set to larger one
    if rank[y] > rank[x]:
        x, y = y, x

    parent[y] = x
    rank[x] += rank[y]


def merge_union(setlist):
    # For every word in sets list what sets contain it
    words = defaultdict(list)

    for i, s in enumerate(setlist):
        for w in s['aliases']:
            words[w].append(i)
    # Merge sets that share the word
    parent = list(range(len(setlist)))
    rank = [1] * len(setlist)
    for sets in words.values():
        it = iter(sets)
        merge_to = next(it)
        for x in it:
            merge(parent, rank, merge_to, x)
    # Construct result by union the sets within a component
    result = defaultdict(dict)
    for merge_from, merge_to in enumerate(parent):
        if merge_to not in result:
            result[merge_to] = setlist[merge_from]
        else:
            result[merge_to]['aliases'] = list(set(result[merge_to]['aliases']) |
                                               set(setlist[merge_from]['aliases']))
    return list(result.values())


def semesters(request):
    semester_list = (semesterFromID(d['semester']) for d in
                     Course.objects.values('semester').order_by('semester').distinct())
    return JSON({RSRCS: [s.toShortJSON() for s in semester_list]})


def semester_main(request, semester_code):
    return JSON(semesterFromCode(semester_code).toJSON())


def semester_dept(request, semester_code, dept_code):
    dept_code = dept_code.upper()
    d = Department.objects.get(code=dept_code)
    dept = SemesterDepartment(semesterFromCode(semester_code), d)
    return JSON(dept.toJSON())


def instructors(request):
    if not request.consumer.access_pcr:
        # This method is only available to those with review data access.
        raise API404("This is not the database dump you are looking for.")

    # get departments for every instructor
    # 1.  Professor id --> set of courses they teach
    prof_to_courses_fields = ['instructor_id', 'section__course_id']
    # thing in the current semester (IE, profs only teaching this semester aren't useful)
    prof_to_courses_query = Review.objects.select_related(*prof_to_courses_fields) \
        .values(*prof_to_courses_fields)
    prof_to_courses = defaultdict(set)
    for e in prof_to_courses_query:
        prof_to_courses[e['instructor_id']].add(e['section__course_id'])

    # 2.  Course id --> set of departments its in
    course_to_depts_fields = ['department__code', 'course_id']
    course_to_depts_query = Alias.objects.select_related(*course_to_depts_fields) \
        .values(*course_to_depts_fields)
    course_to_depts = defaultdict(set)
    for e in course_to_depts_query:
        course_to_depts[e['course_id']].add(e['department__code'])

    def instructor_to_depts(i):
        return list(set(dept for course in prof_to_courses[i.id] for dept in course_to_depts[course]))

    def make_instructor_json(i):
        json = i.toShortJSON()
        json["depts"] = instructor_to_depts(i)
        return json

    # 3. get and aggregate all course alias data no 'this semester only' prof, please
    return JSON({RSRCS: [
        make_instructor_json(i)
        for i in Instructor.objects.all() if i.id in prof_to_courses
    ]})


def instructor_main(request, instructor_id):
    db_id = int(instructor_id.split("-")[0])
    c = Instructor.objects.get(id=db_id)
    return JSON(c.toJSON(extra=['sections', 'reviews']))


def instructor_sections(request, instructor_id):
    db_id = int(instructor_id.split("-")[0])
    sections = Instructor.objects.get(id=db_id).section_set.all()

    return JSON({RSRCS: [s.toJSON() for s in sections]})


def instructor_reviews(request, instructor_id):
    db_id = int(instructor_id.split("-")[0])
    sections = Instructor.objects.get(id=db_id).section_set.all()
    reviews = sum([list(s.review_set.all()) for s in sections], [])

    return JSON({RSRCS: [r.toJSON() for r in reviews]})


def coursehistory_main(request, histid):
    hist = CourseHistory.objects.get(id=int(histid))
    return JSON(hist.toJSON())


def coursehistory_reviews(request, histid):
    reviews = Review.objects.filter(section__course__history__id=int(histid))
    return JSON({RSRCS: [r.toJSON() for r in reviews]})


def course_main(request, courseid):
    course = Course.objects.get(id=int(courseid))
    return JSON(course.toJSON())


def course_reviews(request, courseid):
    sections = Course.objects.get(id=int(courseid)).section_set.all()
    reviews = sum([list(s.review_set.all()) for s in sections], [])
    return JSON({RSRCS: [r.toJSON() for r in reviews]})


def course_sections(request, courseid):
    # Return full JSON.
    api_sections = list(Course.objects.get(id=int(courseid)).section_set.all())
    return JSON({RSRCS: [s.toJSON() for s in api_sections]})


def course_history(request, path, courseid):
    course = Course.objects.get(id=int(courseid))
    return redirect(reverse("history", histid=course.history_id) + "?token=" + request.GET.get("token", ""))


def section_main(request, courseid, sectionnum):
    courseid = int(courseid)
    sectionnum = int(sectionnum)
    try:
        section = Section.objects.get(sectionnum=sectionnum, course=courseid)
        return JSON(section.toJSON())
    except Section.DoesNotExist:
        raise API404("Section %03d of course %d not found" %
                     (sectionnum, courseid))


def section_reviews(request, courseid, sectionnum):
    courseid = int(courseid)
    sectionnum = int(sectionnum)
    try:
        section = Section.objects.get(sectionnum=sectionnum, course=courseid)
        return JSON({RSRCS: [r.toJSON() for r in section.review_set.all()]})
    except Section.DoesNotExist:
        raise API404("Section %03d of course %d not found" %
                     (sectionnum, courseid))


def review_main(request, courseid, sectionnum, instructor_id):
    try:
        db_instructor_id = int(instructor_id.split("-")[0])
        db_review = Review.objects.get(section__sectionnum=sectionnum,
                                       section__course=courseid,
                                       instructor__id=db_instructor_id)
        review = db_review
        return JSON(review.toJSON())
    except Review.DoesNotExist:
        raise API404("Review for %s for section %03d of course %d not found" %
                     (instructor_id, sectionnum, courseid))


def alias_course(request, coursealias, path):
    try:
        semester_code, dept_code, coursenum_str = coursealias.upper().split('-')
        semester = semesterFromCode(semester_code)
        coursenum = int(coursenum_str)
    except:
        raise API404("Course alias %s not in correct format: YYYYS-DEPT-100." %
                     coursealias)

    courseid = Alias.objects.get(semester=semester,
                                 department=dept_code,
                                 coursenum=coursenum).course_id
    return redirect(reverse("course", kwargs={"courseid": courseid}) + path + "?token=" + request.GET.get("token", ""))


def alias_section(request, sectionalias):
    try:
        semester_code, dept_code, coursenum_str, sectionnum_str = (
            sectionalias.upper().split('-'))
        semester = semesterFromCode(semester_code)
        coursenum = int(coursenum_str)
        sectionnum = int(sectionnum_str)
    except:
        raise API404("Section alias %s not in correct format: YYYYS-DEPT-100-001."
                     % sectionalias)

    courseid = Alias.objects.get(semester=semester,
                                 department=dept_code,
                                 coursenum=coursenum).course_id
    return redirect(reverse("section", courseid=courseid, sectionnum=sectionnum) + "?token=" + request.GET.get("token", ""))


def alias_coursehistory(request, historyalias, path):
    try:
        dept_code, coursenum_str = historyalias.upper().split('-')
        coursenum = int(coursenum_str)
    except:
        raise API404("Course alias %s not in correct format: DEPT-100." %
                     historyalias)

    latest_alias = Alias.objects.filter(
        department=dept_code, coursenum=coursenum).order_by('-semester')[0]

    return redirect(reverse("history", kwargs={"histid": latest_alias.course.history_id}) + path + "?token=" + request.GET.get("token", ""))


def alias_misc(request, alias):
    content = json.dumps({"error": "Unmatched query '%s'" % alias,
                          "valid": False,
                          "version": "0.3"},
                         sort_keys=True,
                         indent=3)
    return HttpResponse(status=404,
                        content=content,
                        content_type="application/json")


def depts(request):
    depts = Department.objects.order_by('code').all()
    return JSON({RSRCS: [d.toShortJSON() for d in depts]})


def dept_main(request, dept_code):
    dept_code = dept_code.upper()
    d = Department.objects.get(code=dept_code)
    return JSON(d.toJSON())


def dept_reviews(request, dept_code):
    reviews = Review.objects.filter(
        section__course__alias__department__code=dept_code)
    return JSON({RSRCS: [r.toJSON() for r in reviews]})


def buildings(request):
    # TODO
    return JSON({RSRCS: [Building(code="LEVH", name="Levine Hall").toJSON()]})


def building_main(request, code):
    code = code.upper()
    if code != "LEVH":
        raise API404("Building %s not found" % code)

    return JSON(Building(code="LEVH", name="Levine Hall").toJSON())


def index(request):
    return JSON("Welcome to the Penn Labs PCR API. For docs, see %s."
                % DOCS_HTML)
