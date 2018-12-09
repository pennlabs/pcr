import itertools
import requests

from django.shortcuts import render, reverse
from django.http import JsonResponse, Http404
from .models import Instructor, CourseHistory, Department
from api.courses.models import Instructor as ApiInstructor
from collections import OrderedDict


def instructor(request, id):
    try:
        instructor = Instructor(id)
    except ValueError:
        raise Http404("Instructor {} does not exist!".format(id))
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
    try:
        coursehistory = CourseHistory(title)
    except ValueError:
        raise Http404("Course {} does not exist!".format(title))
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
    try:
        department = Department(name)
    except ValueError:
        raise Http404("Department {} does not exist!".format(name))
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

    instructors = list(set(itertools.chain(*[[y["name"] for y in x["instructors"]] for x in matching_courses])))
    instructor_links = {}

    for name in instructors:
        first_name = name.split(" ", 1)[0]
        last_name = name.rsplit(" ", 1)[-1]
        objs = ApiInstructor.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)
        if objs.count() == 1:
            instructor_links[name] = objs.first().get_absolute_url()

    data = {
        "courses": courses,
        "credits": max(round(float(x["credits"].split(" ")[0]), 2) for x in matching_courses) if matching_courses else 0,
        "instructors": instructors,
        "instructor_links": instructor_links,
        "term": matching_courses[0]["term_normalized"] if matching_courses else None
    }
    return JsonResponse(data, json_dumps_params={"indent": 4})
