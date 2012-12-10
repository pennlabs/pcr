import json

from django.http import HttpResponse

from pcrsite.lib.api import api


def json_response(result_dict):
  return HttpResponse(content=json.dumps(result_dict))

def autocomplete_data(request, start=None):
  #1. Hit API up for course-history data, push into nop's desired format
  def alias_to_code(alias, sep="-"):
    code, num = alias.split('-')
    return "%s%s%03d" % (code, sep, int(num))
  courses_from_api = api('coursehistories')['values']
  courses = []
  for course in courses_from_api:
    for alias in course['aliases']:
      course_keywords = " ".join([alias_to_code(alias.lower(), sep)
                                  for sep in ['', '-', ' ']]
                                 + [course['name'].lower()])
      course_title = alias_to_code(alias, ' ')
      if start in course_title or start in course_keywords:
        courses.append({"category": "Courses",
                "title": course_title,
                "desc": course['name'],
                "url": "course/" + alias_to_code(alias),
                "keywords": course_keywords
                })
              
  #2. Hit API up for instructor data, push into nop's desired format
  instructors_from_api = api('instructors')['values']  
  instructors=[{"category": "Instructors",
                "title": instructor['name'],
                "desc": ", ".join(instructor['depts']),
                "url": "instructor/" + instructor['id'],
                "keywords": instructor['name'].lower()
               } for instructor in instructors_from_api 
                 if 'depts' in instructor and (start in instructor['name']
                   or start in instructor['name'].lower())]

  #3. Hit API up for department data, push into nop's desired format
  departments_from_api = api('depts')['values']  
  departments=[{"category": "Departments",
                "title": department['id'],
                "desc": "".join(department['name']),
                "url": "department/" + department['id'],
                "keywords": department['name']
               } for department in departments_from_api
                 if start in department['id'].lower() 
                   or start in department['name'].lower()]

  #4. Respond in JSON
  return json_response({"courses":courses, "instructors":instructors, 
    "departments":departments})
