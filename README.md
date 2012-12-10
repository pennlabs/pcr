![Course Review Pipeline](http://i.imgur.com/82SzO.jpg)

PCR is divided into two components. The PCR API and the PCR Site.

# PCR API

The PCR API is composed of two parts. The scripts which pull the course data from the registrar and the legacy PCR database, and the site which powers the API itself.

## api
The api itself consists of five apps-- apiconsumer, course_descriptions, courses, static_content, and testconsole.

### apiconsumer
Sets permission levels for developers who wish to use our API. This is mainly in place because the data should only be accessible to Penn students and faculty.

### course_descriptions
Parses the course register. (Probably should be moved to /scripts)

### courses
Powers the actual API.

### static_content
Responsible for powering the static pages on the PCR site. It's basically a very simple version of a CMS and exists solely so that admins only have to manage one admin site.

### testconsole
testconsole is a simple javascript interface for the api.

## scripts
Responsible for scraping new data from the registrar and grabbing old data from the legacy PCR site.

### PCR Daemon User
Username: pcr-daemon
Password: laurenspringer

### Instructions to update the PCR API database

1. Change your directory to Penn-Course-API/scripts
2. Run "python download.py"
    * This scrapes the registrar, cleans up the data, and dumps it into /registrardata.
3. Run "python uploadcourses.py YEAR SEMESTER registrardata/*.txt"
    * uploadcourses.py [YEAR] [SEMESTER] [*FILES] parses the data scraped from download.py and uses it to update the PCR API database.
    * SEMESTER accepts either 'a', 'b', or 'c'
    * (ie, run "python uploadcourses.py 2009 a registrardata/econ.txt")
    * Since the registrardata changes every year, YEAR should be the current year, and SEMESTER the current semester.
4. Run "python import_from_pcr.py YEAR SEMESTER"
    * import_from_pcr.py [YEAR] [SEMESTER] reads from an external database-- assumed to have the original PCR records --and creates or updates course and review data in the new PCR API database.
    * (This can take a while.)

# PCR Site
The PCR site consists of three apps: pcr_detail, searchbar, and static.

## apps/pcr_detail
pcr_detail is responsible for serving model detail pages (ie, the instructor page, the coursehistory page, and the department page). Each page consists of three widgets:

* An "infobox" (Top-left). The infobox is responsible for showing information about the model itself. Since infoboxes change dramatically based on the model, there are different templates for each model.
* A scorecard (Top-right). The scorecard is responsible for showing the average and recent values of the reviews.
* A "scoretable" (Bottom). The scoretable is responsible for displaying the raw reviews in an accessible manner. The scoretable is composed by grouping on a key object (either a course or an instructor) and then displaying a relevant "sectiontable" which displays the raw data and possibly has a comment.
* A "choose_cols_box" (Visible when you click "Choose Columns"). The choose_cols_box is responsible for formatting the attributes into two columns.

This app also contains models.py which contains wrappers for each of the API objects.

## apps/searchbar
searchbar is responsible for the backend code that powers the searchbar.

## apps/static
static is responsible for serving the FAQ and About page. Both of these pages actually have their content stored in the API (so that admins only have to manage one site).

## lib/api

Each of these apps make use of the api function found in lib/api/api.py. The api function pulls domain and token data from local_settings to make requests to the PCR API.

