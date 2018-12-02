import itertools
import requests

from django.shortcuts import render
from django.http import JsonResponse
from .models import Instructor, CourseHistory, Department
from collections import OrderedDict


def instructor(request, id):
    instructor = Instructor(id)
    context = {
        'item': instructor,
        'reviews': instructor.reviews,
        'title': instructor.name,
        'show_name': True,
        'type': 'instructor',
    }
    return render(request, 'pcr_detail/detail.html', context)


# groups instructors to reviews by recency in semester
def sorted_instructors_by_sem(reviews):
    sorted_reviews = sorted(reviews, key=lambda review: review.section.course.semester)
    instructor_to_most_recent_sem = {}
    for review in sorted_reviews:
        instructor_to_most_recent_sem[review.instructor] = review.section.course.semester
    sorted_instructors = sorted(instructor_to_most_recent_sem.items(), key=lambda x: x[1], reverse=True)
    grouped_obj = OrderedDict()
    for i in sorted_instructors:
        associated_reviews = []
        for review in sorted_reviews:
            if review.instructor.name == i[0].name:
                associated_reviews.append(review)
        grouped_obj[i[0]] = associated_reviews
    return grouped_obj


def course(request, title):
    title = title.upper()
    coursehistory = CourseHistory(title)
    reviews = set(
        review for course in coursehistory.courses for section in course.sections for review in section.reviews)
    grouped_reviews = sorted_instructors_by_sem(reviews)
    context = {
        'item': coursehistory,
        'reviews': reviews,
        'show_name': len(set([r.section.name for r in reviews])) != 1,
        'title': title,
        'type': 'course',
        'instructor_list': grouped_reviews
    }
    return render(request, 'pcr_detail/detail.html', context)


def department(request, name):
    department = Department(name)
    context = {
        'item': department,
        'reviews': set(review for coursehistory in department.coursehistories
                       for course in coursehistory.courses
                       for section in course.sections
                       for review in section.reviews),
        'title': name,
        'show_name': True,
        'type': 'department',
    }
    return render(request, 'pcr_detail/detail.html', context)


def live(request, title):
    title = title.upper().strip()
    dept, code = title.split("-")
    resp = requests.get("http://api.pennlabs.org/registrar/search?q={}".format(title))
    resp.raise_for_status()
    raw_data = resp.json()
    matching_courses = [course for course in raw_data["courses"] if course["course_department"].strip().upper() == dept and course["course_number"].strip().upper() == code]
    courses = {}

    for course in matching_courses:
        key = course["activity"]
        if key not in courses:
            courses[key] = []
        courses[key].append(course)

    data = {
        "courses": courses,
        "credits": max(round(float(x["credits"].split(" ")[0]), 2) for x in matching_courses) if matching_courses else 0,
        "instructors": list(set(itertools.chain(*[[y["name"] for y in x["instructors"]] for x in matching_courses]))),
        "term": matching_courses[0]["term_normalized"] if matching_courses else None
    }
    return JsonResponse(data, json_dumps_params={"indent": 4})
