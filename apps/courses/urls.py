from django.conf.urls import url

# import each of the handlers
from . import views
from .utils import cross_domain_ajax, API404


def dispatch_404(message=None, perhaps=None):
    def view(request):
        raise API404(message)
    return view


urlpatterns = [
    # Index
    url(r"^$", views.index),

    # Instructors
    url(r"^instructors/?$", views.instructors),
    url(r"^instructors/(?P<instructor_id>[^/]+)/?$", views.instructor_main, name="instructor"),
    url(r"^instructors/(?P<instructor_id>[^/]+)/sections/?$", views.instructor_sections),
    url(r"^instructors/(?P<instructor_id>[^/]+)/reviews$/?", views.instructor_reviews),

    # Course Histories
    url(r"^coursehistories/?$", views.course_histories),
    url(r"^coursehistories/(?P<histid>\d+)/?$", views.coursehistory_main, name="history"),
    url(r"^coursehistories/(?P<histid>\d+)/reviews/?$", views.coursehistory_reviews),
    url(r"^coursehistories/(?P<historyalias>[^/]+)(?P<path>.*)", views.alias_coursehistory),

    # Departments
    url(r"^depts/?$", views.depts),
    url(r"^depts/(?P<dept_code>[^/]+)/?$", views.dept_main, name="department"),
    url(r"^depts/(?P<dept_code>[^/]+)/reviews/?$", views.dept_reviews),

    # Semesters
    url(r"^semesters/?$", views.semesters),
    url(r"^semesters/(?P<semester_code>[^/]+)/?$", views.semester_main, name="semester"),
    url(r"^semesters/(?P<semester_code>[^/]+)/(?P<dept_code>[^/]+)/?$", views.semester_dept, name="semdept"),

    # Buildings
    url(r"^building/?$", views.buildings),
    url(r"^building/(?P<code>[^/]+)/?$", views.building_main, name="building"),

    # Courses
    url(r"^courses/?$", dispatch_404("sorry, no global course list")),
    url(r"^courses/(?P<courseid>\d+)/?$", views.course_main, name="course"),
    url(r"^courses/(?P<courseid>\d+)/reviews/?$", views.course_reviews),
    url(r"^courses/(?P<courseid>\d+)/sections/?$", views.course_sections),
    url(r"^courses/(?P<courseid>\d+)/sections/(?P<sectionnum>[^/]+)/?$", views.section_main, name="section"),
    url(r"^courses/(?P<courseid>\d+)/sections/(?P<sectionnum>[^/]+)/reviews/?$", views.section_reviews),
    url(r"^courses/(?P<courseid>\d+)/sections/(?P<sectionnum>[^/]+)/reviews/(?P<instructor_id>[^/]+)/?$", views.review_main, name="review"),
    url(r"^courses/(?P<coursealias>[^/]+)(?P<path>.*)$", views.alias_course),

    # Sections
    url(r"^sections$", dispatch_404("sorry, no global sections list")),
    url(r"^sections/(?P<sectionalias>[^/]+)$", views.alias_section),

    # Misc
    url(r"^(?P<alias>.*)$", views.alias_misc)
]


def handle_errors(func):
    def wrap(request, *args, **kwargs):
        try:
            if not request.consumer.access_pcr and "review" in request.path:
                raise API404("This API token does not have access to review data.")
            response = func(request, *args, **kwargs)
        except API404 as e:
            obj = {
                'help': "See %s for API documentation." % views.DOCS_HTML,
                'error': 'Error 404. The resource could not be found: ' + request.path
            }
            if e.perhaps:
                obj['perhaps_you_meant'] = e.perhaps  # and perhaps not
            if e.message:
                obj['message'] = e.message
            return views.JSON(obj, valid=False, httpstatus=404)
        return response
    return wrap


for pattern in urlpatterns:
    pattern.callback = handle_errors(cross_domain_ajax(pattern.callback))
