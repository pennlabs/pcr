import re
import requests
import itertools

from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q, Avg
from django.views.decorators.cache import cache_page, never_cache
from django.shortcuts import redirect
from statistics import mean

from .models import Alias, Course, Section, Review, ReviewBit, Instructor, Department, CourseHistory
from ..apiconsumer.models import APIUser

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def titleize(name):
    """ Titleize a course name or instructor, taking into account exceptions such as II. """
    name = re.sub(r"I(x|v|i+)", lambda m: "I" + m.group(1).upper(), name.strip().title())
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


@never_cache
def display_token(request):
    if isinstance(request.consumer, APIUser):
        request.consumer.regenerate()
        if 'redirect' not in request.GET:
            return JsonResponse({
                "error": "No redirect url passed to server."
            })
        original_url = request.GET['redirect']
        redirect_url = urlparse(original_url)
        valid_scheme = redirect_url.scheme in ['http', 'https']
        valid_host = redirect_url.netloc.rsplit(":", 1)[0] in settings.ALLOWED_HOSTS
        if not valid_scheme or not valid_host:
            return JsonResponse({
                "error": "Invalid redirect url passed to server. ({})".format("invalid protocol" if not valid_scheme else "invalid origin")
            })

        domain = None
        if redirect_url.netloc.startswith("www."):
            domain = redirect_url.netloc.split(".", 1)[1]

        resp = redirect(original_url)
        resp.set_cookie('token', request.consumer.token, expires=request.consumer.expiration, domain=domain)
        return resp

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

    instructors = {
        inst["id"]: {
            "name": titleize("{} {}".format(inst["first_name"] or "", inst["last_name"] or "")),
            "average_reviews": {},
            "recent_reviews": {}
        } for inst in Instructor.objects.filter(Q(first_name__isnull=False) | Q(last_name__isnull=False), section__in=sections).values("id", "first_name", "last_name")
    }
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
    sections = Section.objects.filter(instructors=instructor).order_by("course__semester")
    reviews = Review.objects.filter(instructor=instructor)
    course_average_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__course__history").annotate(score=Avg('score'))
    course_recent_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__course__history", "review__section__course__semester").annotate(score=Avg('score')).order_by("review__section__course__semester")
    rating_keys = {bit["field"] for bit in course_average_ratings}

    output = {}

    for dept, num, name, iden in sections.values_list("course__primary_alias__department", "course__primary_alias__coursenum", "name", "course__history__id").distinct():
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

    for sec, name, sem in section_objects.values_list("id", "name", "course__semester"):
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


@cache_page(60 * 60)
def display_autocomplete(request):
    course_set = {}
    for dept, num, name in Section.objects.all().values_list("course__primary_alias__department__code", "course__primary_alias__coursenum", "name").distinct():
        code = "{} {:03d}".format(dept, num)
        if code in course_set:
            if name is not None:
                course_set[code]["desc"].add(name)
        else:
            course_set[code] = {
                "title": code,
                "desc": set([name]) if name is not None else set(),
                "url": "course/{}-{:03d}".format(dept, num)
            }

    for info in course_set.values():
        info["desc"] = sorted(info["desc"])

    depts = [{
        "title": code,
        "desc": name,
        "url": "department/{}".format(code)
    } for code, name in Department.objects.all().values_list("code", "name")]

    instructor_set = {}
    instructors_with_names = Instructor.objects.filter(Q(first_name__isnull=False) | Q(last_name__isnull=False))

    for iid, first, last, dept in instructors_with_names.values_list("id", "first_name", "last_name", "section__course__primary_alias__department__code").distinct():
        code = "{}-{}-{}".format(iid, first.replace(" ", "-") if first is not None else "", last.replace(" ", "-") if last is not None else "")
        if code in instructor_set:
            if dept is not None:
                instructor_set[code]["desc"].add(dept)
        else:
            instructor_set[code] = {
                "title": titleize("{} {}".format(first or "", last or "")),
                "desc": set([dept]) if dept is not None else set(),
                "url": "instructor/{}".format(code)
            }

    for info in instructor_set.values():
        info["desc"] = ", ".join(sorted(info["desc"]))

    return JsonResponse({
        "courses": list(course_set.values()),
        "departments": depts,
        "instructors": list(instructor_set.values())
    })


def display_live(request, course):
    title = course.upper().strip()
    try:
        dept, code = title.split("-")
    except ValueError:
        return JsonResponse({
            "error": "Incorrectly formatted course code '{}'.".format(title)
        })

    resp = requests.get("https://api.pennlabs.org/registrar/search?q={}".format(title))
    resp.raise_for_status()
    raw_data = resp.json()
    matching_courses = [course for course in raw_data["courses"] if course["course_department"].strip().upper() == dept and course["course_number"].strip().upper() == code and course["is_cancelled"] is not True]
    courses = {}

    for course in matching_courses:
        key = course["activity"]
        if key not in courses:
            courses[key] = []
        courses[key].append(course)

    instructors = list(set(itertools.chain(*[[y["name"] for y in x["instructors"]] for x in matching_courses if x["activity"] not in ["REC"]])))
    instructor_links = {}

    for name in instructors:
        first_name = name.split(" ", 1)[0]
        last_name = name.rsplit(" ", 1)[-1]
        objs = Instructor.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)
        if objs.count() == 1:
            instructor_links[name] = objs.first().get_absolute_url()

    data = {
        "courses": courses,
        "credits": max(round(float(x["credits"].split(" ")[0]), 2) for x in matching_courses) if matching_courses else 0,
        "instructors": instructors,
        "instructor_links": instructor_links,
        "term": matching_courses[0]["term_normalized"] if matching_courses else None
    }

    return JsonResponse(data)
