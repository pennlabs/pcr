import re

from django.http import JsonResponse
from django.db.models import Avg

from .models import Alias, Course, Section, Review, ReviewBit


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

    return JsonResponse({
        "code": "{} {}".format(dept, num),
        "name": course.name,
        "description": course.description.strip(),
        "average_ratings": {bit["field"]: round(bit["score"], 1) for bit in reviewbits_average},
        "recent_ratings": {bit["field"]: round(bit["score"], 1) for bit in reviewbits_recent}
    })
