#!/usr/bin/env python

'''Scrapes the registrar for information about all of the courses and dumps
them into /registrar.'''

import re
import time
import logging
import urllib2, re, codecs, os, shutil

from bs4 import BeautifulSoup
from xml.dom.minidom import parseString

DELETE_OLD_STUFF_MODE = False

# timetable or roster depending on time of year
urlType = "roster"

# download the roster category listing
rosterUrl = "http://www.upenn.edu/registrar/{}/".format(urlType)
response = urllib2.urlopen(rosterUrl)
html = response.read()

soup = BeautifulSoup(html, "html.parser")

# list of tuples with (url, category)
subjects = []
categoryPattern = re.compile("^\w+.html$")

for table in soup.findAll("table"):
    for link in soup.findAll("a"):
        href = link.get("href")
        if href.startswith("#"):
            continue
        if not categoryPattern.match(href):
            continue
        subjects.append((href, link.findParent("tr").findAll("td")[0].text.strip()))

if DELETE_OLD_STUFF_MODE:
    shutil.rmtree('./registrardata')

try:
    os.mkdir('registrardata')
except Exception:
    pass

os.chdir('./registrardata')

for urlpart, subject in subjects:
    url = rosterUrl + urlpart
    file_name = subject + ".txt"
    # if file already exists, just skip this one for now
    if not os.path.isfile(file_name):
        try:
            soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
        except urllib2.HTTPError:
            logging.warning("Failed to parse %s", url)
            continue
        outfile = open(file_name, 'w')
        outfile.write(subject.encode('utf-8') + '\n')
        outfile.write(soup.pre.text)
        outfile.close()
        logging.info("Added %s from %s", file_name, url)
        # should not be necessary anymore, the whole operation
        # is finished in less than a minute without any problems
        # time.sleep(3)  # don't get all angry at me for scraping yo
    else:
        logging.warning("%s already exists, skipping...", file_name)
