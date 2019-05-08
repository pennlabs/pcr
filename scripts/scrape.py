#!/usr/bin/env python3

# Currently unused script to scrape course requirement/degree information from various sources and save to a JSON file.

import requests
import json
import re
import os
import collections
import datetime

from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup


def get_single_degree(obj):
    href, text = obj

    absolute_link = "https://catalog.upenn.edu" + href
    soup2 = BeautifulSoup(requests.get(absolute_link).content, "lxml")
    courses_raw = [course.text.replace("\u00a0", " ") for course in soup2.find("table", {"class": "sc_courselist"}).findAll("a", {"class": "bubblelink code"})]
    courses = []
    dept_prefixes = []
    for course in courses_raw:
        course_parts = [x.strip() for x in course.split("/")]
        for course_part in course_parts:
            if re.match(r"^[A-Z]{2,4} \d{3}$", course_part):
                courses.append(course_part)
                code = course_part.split(" ")[1]
                for prefix in dept_prefixes:
                    courses.append("{} {}".format(prefix, code))
                dept_prefixes = []
            elif re.match(r"^[A-Z]{2,4}", course_part):
                dept_prefixes.append(course_part)
            elif re.match(r"^\d{3}", course_part):
                courses.append("{} {}".format(courses[-1].split(" ")[0], course_part))
            else:
                raise ValueError("Unknown course code format '{}'!".format(course_parts))
    data = (text, {
        "link": absolute_link,
        "courses": courses
    })

    print("Obtained '{}' - {} courses".format(text, len(courses)))
    return data


def get_degree_information():
    print("Retrieving degree information...")
    soup = BeautifulSoup(requests.get("https://catalog.upenn.edu/undergraduate/programs/").content, "lxml")
    links = soup.find("div", {"class": "az_sitemap"}).findAll("a")
    with ThreadPoolExecutor(max_workers=6) as p:
        output = p.map(get_single_degree, [(x.get("href"), x.text) for x in links if x.get("href") and not x.get("href").startswith("#")])
    courses = collections.defaultdict(list)
    for degree, info in output:
        for course in info["courses"]:
            courses[course].append({
                "degree": degree,
                "link": info["link"]
            })
    return {x: {"degrees": y} for x, y in courses.items()}


def get_ccp_information():
    print("Retrieving Wharton CCP information...")
    data = []
    for course in requests.get("https://apps.wharton.upenn.edu/reports/index.cfm?action=reports.renderDatatablesJSON&id=UGRGenEdsNew").json()["data"]:
        data.append({
            "course": "{} {}".format(course[0], course[1]),
            "name": course[2].strip(),
            "gened": course[3],
            "ccp": "Yes" in course[4],
            "cdus": "CDUS" in course[4],
            "ccp_link": "https://undergrad-inside.wharton.upenn.edu/course-search-2017/"
        })
    return {x["course"]: x for x in data}


def get_sector_information():
    print("Retrieving College sector information...")
    courses = {}
    for sector in ["S", "H", "A", "O", "L", "P", "N"]:
        link = "https://apps.sas.upenn.edu/genreq/results.php?req[]={}&cls=10".format(sector)
        resp = requests.get(link)
        soup = BeautifulSoup(resp.content, "lxml")
        sector_name = soup.find("span", {"class": "bold"}).text.strip()
        for entry in soup.find("table", {"class": "cell2010"}).findAll("tr", {"class": ""}):
            cols = [x.text for x in entry.findAll("td")]
            code = cols[2]
            if not re.match(r"[A-Z]{2,4}\d{3}", code):
                continue
            courses[re.sub(r"([A-Z]{2,4})(\d{3})", r"\1 \2", code)] = {
                "sector_requirement": sector_name,
                "college_link": link
            }
    return courses


sources = [("catalog.json", get_degree_information), ("ccp.json", get_ccp_information), ("sector.json", get_sector_information)]

for fname, f in sources:
    if not os.path.exists(fname):
        data = f()
        with open(fname, "w") as f:
            f.write(json.dumps(data, indent=4))


print("Aggregating information...")

courses = collections.defaultdict(dict)
last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

for fname, _ in sources:
    with open(fname, "r") as f:
        for course, details in json.loads(f.read()).items():
            courses[course].update(details)

for course in courses.values():
    course["last_updated"] = last_updated

with open("data.json", "w") as f:
    f.write(json.dumps(courses, indent=4))
