import re

from django.http import JsonResponse
from django.db.models import Avg

from .models import Alias, Course, Section, Review, ReviewBit, Instructor


def display_course(request, course):
    dept, num = re.match(r"([A-Za-z]{3,4})[ \-]{1}(\d+)", course).groups()
    aliases = Alias.objects.filter(department__code__iexact=dept, coursenum=num)
    courses = Course.objects.filter(primary_alias__in=aliases)
    course = courses.order_by('-semester').first()
    semester = course.semester
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
        "name": course.name,
        "description": course.description.strip(),
        "average_ratings": {bit["field"]: round(bit["score"], 1) for bit in reviewbits_average},
        "recent_ratings": {bit["field"]: round(bit["score"], 1) for bit in reviewbits_recent},
        "instructors": instructors,
    })
