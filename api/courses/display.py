import re

from django.http import JsonResponse
from django.db.models import Avg
from statistics import mean

from .models import Alias, Course, Section, Review, ReviewBit, Instructor, Department, CourseHistory


def display_course(request, course):
    info = re.match(r"([A-Za-z]{3,4})[ \-]{1}(\d+)", course)
    if info is None:
        return JsonResponse({
            "error": "Incorrectly formatted course code '{}'.".format(course)
        })
    dept, num = info.groups()
    aliases = Alias.objects.filter(department__code__iexact=dept, coursenum=num)
    courses = Course.objects.filter(primary_alias__in=aliases)
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

    instructors = {inst["id"]: {"name": (inst["first_name"] + " " + inst["last_name"]).strip(), "average_reviews": {}, "recent_reviews": {}} for inst in Instructor.objects.filter(section__in=sections).values("id", "first_name", "last_name")}
    instructor_average_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__instructors").annotate(score=Avg('score'))
    instructor_recent_ratings = ReviewBit.objects.filter(review__in=reviews).order_by("review__section__course__semester").values("field", "review__section__instructors", "score")

    for rating in instructor_average_ratings:
        instructors[rating["review__section__instructors"]]["average_reviews"][rating["field"]] = round(rating["score"], 2)

    for rating in instructor_recent_ratings:
        instructors[rating["review__section__instructors"]]["recent_reviews"][rating["field"]] = round(rating["score"], 2)

    instructors = {("{}-{}".format(k, re.sub(r"[^\w]", "-", v["name"]))): v for k, v in instructors.items()}

    return JsonResponse({
        "code": "{} {}".format(dept, num),
        "name": course_latest_semester.name,
        "description": course_latest_semester.description.strip(),
        "average_ratings": {bit["field"]: round(bit["score"], 1) for bit in reviewbits_average},
        "num_sections": sections.count(),
        "recent_ratings": {bit["field"]: round(bit["score"], 1) for bit in reviewbits_recent},
        "instructors": instructors,
    })


def display_instructor(request, instructor):
    req_instructor = instructor
    info = re.match(r"(\d+)-+(\w+)-+(\w+)", req_instructor)
    if info is None:
        return JsonResponse({
            "error": "Incorrectly formatted instructor code '{}'.".format(req_instructor)
        })
    instructor_id, first, last = info.groups()
    instructor = Instructor.objects.filter(id=instructor_id, first_name=first, last_name=last).first()
    if instructor is None:
        return JsonResponse({
            "error": "Could not find instructor matching code '{}'.".format(req_instructor)
        })
    sections = Section.objects.filter(instructors=instructor)
    courses = Course.objects.filter(section__in=sections)
    histories = CourseHistory.objects.filter(course__in=courses)
    reviews = Review.objects.filter(instructor=instructor)
    course_average_ratings = ReviewBit.objects.filter(review__in=reviews).values("field", "review__section__course__history").annotate(score=Avg('score'))
    course_recent_ratings = ReviewBit.objects.filter(review__in=reviews).order_by("review__section__course__semester").values("field", "review__section__course__history", "score")
    rating_keys = {bit["field"] for bit in course_average_ratings}

    output = {}

    for dept, num, name, iden in histories.values_list("course__primary_alias__department", "course__primary_alias__coursenum", "course__name", "id").order_by("course__primary_alias__coursenum").distinct():
        code = "{}-{:03d}".format(dept, num)
        output[iden] = {
            "code": code,
            "name": name.title(),
            "average_reviews": {},
            "recent_reviews": {}
        }

    for rating in course_average_ratings:
        output[rating["review__section__course__history"]]["average_reviews"][rating["field"]] = round(rating["score"], 3)

    for rating in course_recent_ratings:
        output[rating["review__section__course__history"]]["recent_reviews"][rating["field"]] = round(rating["score"], 3)

    return JsonResponse({
        "id": instructor.id,
        "name": instructor.name.title(),
        "average_ratings": {key: round(mean([bit["score"] for bit in course_recent_ratings.filter(field=key).values("score")]), 1) for key in rating_keys},
        "recent_ratings": {bit["field"]: round(bit["score"], 1) for bit in course_recent_ratings},
        "num_sections": sections.count(),
        "courses": output
    })


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
    course_recent_ratings = ReviewBit.objects.filter(review__in=reviews).order_by("review__section__course__semester").values("field", "review__section__course__history", "score")

    output = {}

    for num, name, iden in histories.values_list("course__primary_alias__coursenum", "course__name", "id").order_by("course__primary_alias__coursenum").distinct():
        code = "{}-{:03d}".format(dept, num)
        output[iden] = {
            "code": code,
            "name": name.title(),
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


def display_time(request, course, instructor):
    return JsonResponse({})
