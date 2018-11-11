import os
import json
from courses.models import *  # need to run thru django


def main():
    dir = "course_descriptions/data/"
    for file in os.listdir(dir):
        print file
        if not file.endswith(".txt"):
            continue
        dept = file.split(".")[0]
        data = json.loads("".join(open(dir + file).readlines()))
        for course in data:
            if not course:
                continue
            f = Alias.objects.filter(department__code=dept). \
                filter(coursenum=course["num"]).all()
            if len(f) > 2:
                print course["num"], f
            elif len(f) > 0:
                f[0].course.description = course["description"]
                f[0].course.save()


main()
