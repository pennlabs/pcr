import re

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.db.models import Q, Avg
from statistics import mean

from .models import Alias, Course, Section, Review, ReviewBit, Instructor, Department, CourseHistory
from ..apiconsumer.models import APIUser

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def titleize(name):
    """ Titleize a course name or instructor, taking into account exceptions such as II. """
    name = re.sub(r"I(i+)", lambda m: "I" + m.group(1).upper(), name.strip().title())
    name = re.sub(r"(\d)(St|Nd|Rd|Th)", lambda m: m.group(1) + m.group(2).lower(), name)
    name = re.sub(r"Mc([a-z])", lambda m: "Mc" + m.group(1).upper(), name)
    name = name.replace("'S", "'s")
    return name


def is_pcr_data(func):
    def wrapper(request, *args, **kwargs):
        if not request.consumer.access_pcr:
            return JsonResponse({
                "error": "The provided token does not have access to this data."
            })

        return func(request, *args, **kwargs)
    return wrapper


def display_token(request):
    if isinstance(request.consumer, APIUser):
        host_url = urlparse(request.GET['host'])
        if host_url.scheme not in ['http', 'https'] or host_url.netloc.rsplit(":", 1)[0] not in settings.ALLOWED_HOSTS:
            return JsonResponse({
                "error": "Invalid host url passed to server."
            })
        host_url = "{}://{}/".format(host_url.scheme, host_url.netloc)
        return HttpResponse("<html><head><style>body { background-color: #fafcff; }</style></head><body><script>window.parent.postMessage('{}', '{}');</script></body></html>".format(request.consumer.token, host_url))

    return JsonResponse({
        "error": "Cannot retrieve token with given parameters."
    })


@is_pcr_data
def display_course(request, course):
    info = re.match(r"([A-Za-z]{2,4})[ \-]{1}(\d+)", course)
    if info is None:
        return JsonResponse({
            "error": "Incorrectly formatted course code '{}'.".format(course)
        })
    dept, num = info.groups()
    aliases = Alias.objects.filter(department__code__iexact=dept, coursenum=num)
    courses = Course.objects.filter(alias__in=aliases)
    other_aliases = Alias.objects.filter(course__in=courses).values_list("department__code", "coursenum").distinct()
    course_latest_semester = courses.order_by('-semester').first()
    if course_latest_semester is None:
        return JsonResponse({
            "error": "Could not find course matching code '{}'.".format(course)
        })
    semester = course_latest_semester.semester
    sections = Section.objects.filter(course__in=courses)
    reviews = Review.objects.filter(section__in=sections)
    reviewbits_average = ReviewBit.objects.filter(review__in=reviews).values("field").annotate(score=Avg('score'))
    reviewbits_recent = ReviewBit.objects.filter(review__in=reviews, review__section__course__semester=semester).values("field").annotate(score=Avg('score'))

    instructors = {inst["id"]: {"name": titleize("{} {}".format(inst["first_name"] or "", inst["last_name"] or "")), "average_reviews": {}, "recent_reviews": {}} for inst in Instructor.objects.filter(Q(first_name__isnull=False) | Q(last_name__isnull=False), section__in=sections).values("id", "first_name", "last_name")}
    instructor_average_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__instructors").annotate(score=Avg('score'))
    instructor_recent_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__instructors", "review__section__course__semester").annotate(score=Avg('score')).order_by("review__section__course__semester")

    for rating in instructor_average_ratings:
        instructors[rating["review__section__instructors"]]["average_reviews"][rating["field"]] = round(rating["score"], 2)

    for rating in instructor_recent_ratings:
        instructors[rating["review__section__instructors"]]["recent_reviews"][rating["field"]] = round(rating["score"], 2)
        instructors[rating["review__section__instructors"]]["most_recent_semester"] = str(rating["review__section__course__semester"])

    instructors = {("{}-{}".format(k, re.sub(r"[^\w]", "-", v["name"]))): v for k, v in instructors.items()}

    return JsonResponse({
        "code": "{}-{:03d}".format(dept, int(num)),
        "aliases": ["{}-{:03d}".format(x, y) for x, y in other_aliases if not (x == dept and y == int(num))],
        "name": course_latest_semester.name,
        "description": course_latest_semester.description.strip(),
        "average_ratings": {bit["field"]: round(bit["score"], 1) for bit in reviewbits_average},
        "num_sections": sections.count(),
        "num_sections_recent": sections.filter(course__semester=semester).count(),
        "recent_ratings": {bit["field"]: round(bit["score"], 1) for bit in reviewbits_recent},
        "instructors": instructors,
    })


@is_pcr_data
def display_instructor(request, instructor):
    req_instructor = instructor
    info = re.match(r"(\d+)-+(\w+)-+(\w*)", req_instructor)
    if info is None:
        return JsonResponse({
            "error": "Incorrectly formatted instructor code '{}'.".format(req_instructor)
        })
    instructor_id, first, last = info.groups()
    instructor = Instructor.objects.filter(id=instructor_id).first()
    if instructor is None:
        return JsonResponse({
            "error": "Could not find instructor matching code '{}'.".format(req_instructor)
        })
    sections = Section.objects.filter(instructors=instructor)
    courses = Course.objects.filter(section__in=sections)
    histories = CourseHistory.objects.filter(course__in=courses)
    reviews = Review.objects.filter(instructor=instructor)
    course_average_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__course__history").annotate(score=Avg('score'))
    course_recent_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__course__history", "review__section__course__semester").annotate(score=Avg('score')).order_by("review__section__course__semester")
    rating_keys = {bit["field"] for bit in course_average_ratings}

    output = {}

    for dept, num, name, iden in histories.values_list("course__primary_alias__department", "course__primary_alias__coursenum", "course__name", "id").order_by("course__primary_alias__coursenum").distinct():
        code = "{}-{:03d}".format(dept, num)
        output[iden] = {
            "code": code,
            "name": titleize(name),
            "average_reviews": {},
            "recent_reviews": {}
        }

    for rating in course_average_ratings:
        output[rating["review__section__course__history"]]["average_reviews"][rating["field"]] = round(rating["score"], 2)

    for rating in course_recent_ratings:
        output[rating["review__section__course__history"]]["recent_reviews"][rating["field"]] = round(rating["score"], 2)

    return JsonResponse({
        "id": instructor.id,
        "name": titleize(instructor.name),
        "average_ratings": {key: round(mean([bit["score"] for bit in course_recent_ratings.filter(field=key).values("score")]), 1) for key in rating_keys},
        "recent_ratings": {bit["field"]: round(bit["score"], 1) for bit in course_recent_ratings},
        "num_sections": sections.count(),
        "num_sections_recent": len(output),
        "courses": output
    })


@is_pcr_data
def display_dept(request, dept):
    dept = dept.upper().strip()
    department = Department.objects.filter(code__iexact=dept).first()
    if department is None:
        return JsonResponse({
            "error": "Could not find department matching '{}'.".format(dept)
        })
    histories = CourseHistory.objects.filter(course__primary_alias__department=department)
    reviews = Review.objects.filter(section__course__primary_alias__department=department)

    course_average_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__course__history").annotate(score=Avg('score'))
    course_recent_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__course__history", "review__section__course__semester").annotate(score=Avg('score')).order_by("review__section__course__semester")

    output = {}

    for num, name, iden in histories.values_list("course__primary_alias__coursenum", "course__name", "id").order_by("course__primary_alias__coursenum").distinct():
        code = "{}-{:03d}".format(dept, num)
        output[iden] = {
            "code": code,
            "name": titleize(name),
            "average_reviews": {},
            "recent_reviews": {}
        }

    for rating in course_average_ratings:
        output[rating["review__section__course__history"]]["average_reviews"][rating["field"]] = round(rating["score"], 3)

    for rating in course_recent_ratings:
        output[rating["review__section__course__history"]]["recent_reviews"][rating["field"]] = round(rating["score"], 3)

    return JsonResponse({
        "code": dept,
        "name": department.name.title(),
        "courses": output
    })


@is_pcr_data
def display_history(request, course, instructor):
    req_instructor = instructor
    info = re.match(r"(\d+)-+(\w+)-+(\w*)", req_instructor)
    if info is None:
        return JsonResponse({
            "error": "Incorrectly formatted instructor code '{}'.".format(req_instructor)
        })
    instructor_id, first, last = info.groups()
    instructor = Instructor.objects.filter(id=instructor_id).first()
    if instructor is None:
        return JsonResponse({
            "error": "Could not find instructor matching code '{}'.".format(req_instructor)
        })
    info = re.match(r"([A-Za-z]{2,4})[ \-]{1}(\d+)", course)
    if info is None:
        return JsonResponse({
            "error": "Incorrectly formatted course code '{}'.".format(course)
        })
    dept, num = info.groups()
    aliases = Alias.objects.filter(department__code__iexact=dept, coursenum=num)
    courses = Course.objects.filter(alias__in=aliases)
    section_objects = Section.objects.filter(course__in=courses, instructors=instructor)
    if not section_objects.exists():
        return JsonResponse({
            "error": "Could not find course matching code '{}' with instructor '{}'.".format(course, req_instructor)
        })
    reviews = Review.objects.filter(section__in=section_objects)
    reviewbits = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__course__name", "review__section__course__semester").annotate(score=Avg('score'))

    sections = {}

    for sec, name, sem in section_objects.values_list("id", "course__name", "course__semester"):
        sections[sec] = {
            "course_name": titleize(name),
            "semester": str(sem),
            "ratings": {},
        }

    for sem, sec, field, score in reviewbits.values_list("review__section__course__semester", "review__section__id", "field", "score"):
        sections[sec]["ratings"][field] = round(score, 3)

    for sec, comment, returned, produced in reviews.values_list("section__id", "comments", "forms_returned", "forms_produced"):
        sections[sec]["forms_returned"] = returned
        sections[sec]["forms_produced"] = produced
        sections[sec]["comments"] = comment

    return JsonResponse({
        "instructor": {
            "id": instructor.id,
            "name": instructor.name.title()
        },
        "course_code": "{}-{:03d}".format(dept, int(num)),
        "sections": sections
    })


def display_autocomplete(request):
    courses = [{
        "category": "Courses",
        "title": "{} {:03d}".format(x, y),
        "desc": z,
        "url": "course/{}-{:03d}".format(x, y),
        "keywords": " ".join("{}{}{:03d}".format(x, a, y) for a in ['', '-', ' '])
    } for x, y, z in Alias.objects.all().values_list("department__code", "coursenum", "course__name").distinct()]

    course_set = {}
    for course in courses:
        course_set[course["title"]] = course
    courses = list(course_set.values())

    depts = [{
        "category": "Departments",
        "title": code,
        "desc": name,
        "url": "department/{}".format(code),
        "keywords": "{} {}".format(code, name.lower())
    } for code, name in Department.objects.all().values_list("code", "name")]

    instructor_set = {}

    for iid, first, last, dept in Instructor.objects.filter(Q(first_name__isnull=False) | Q(last_name__isnull=False)).values_list("id", "first_name", "last_name", "section__course__primary_alias__department__code").distinct():
        code = "{}-{}-{}".format(iid, first.replace(" ", "-") if first is not None else "", last.replace(" ", "-") if last is not None else "")
        if code in instructor_set:
            if dept is not None:
                instructor_set[code]["desc"].add(dept)
        else:
            instructor_set[code] = {
                "category": "Instructors",
                "title": titleize("{} {}".format(first or "", last or "")),
                "desc": set([dept]) if dept is not None else set(),
                "url": "instructor/{}".format(code),
                "keywords": "{} {}".format(first, last).lower()
            }

    for info in instructor_set.values():
        info["desc"] = ", ".join(sorted(info["desc"]))

    return JsonResponse({
        "courses": courses,
        "departments": depts,
        "instructors": list(instructor_set.values())
    })
