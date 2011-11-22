import json

from django.http import HttpResponse

from pcrsite.lib.api import api


def json_response(result_dict):
  return HttpResponse(content=json.dumps(result_dict))


def autocomplete_data(request):
  #1. Hit API up for course-history data, push into nop's desired format
  def alias_to_code(alias, sep="-"):
    code, num = alias.split('-')
    return "%s%s%03d" % (code, sep, int(num))
  courses_from_api = api('coursehistories')['values']
  courses = [{"category": "Courses",
              "title": alias_to_code(alias, ' '),
              "desc": course['name'],
              "url": "course/" + alias_to_code(alias),
              "keywords": " ".join([alias_to_code(alias.lower(), sep) \
                            for sep in ['', '-', ' ']] \
                        + [course['name'].lower()])
             } for course in courses_from_api 
               for alias in course['aliases']]

  #2. Hit API up for instructor data, push into nop's desired format
  instructors_from_api = api('instructors')['values']  
  instructors=[{"category": "Instructors",
                "title": instructor['name'],
                "desc": ", ".join(instructor['departments']),
                "url": "instructor/" + instructor['id'],
                "keywords": instructor['name'].lower()
               } for instructor in instructors_from_api 
                 if 'departments' in instructor]

  #3. Respond in JSON
  return json_response({"courses":courses, "instructors":instructors})
