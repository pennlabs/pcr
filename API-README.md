# PennCourseReview API

API for Penn Course Review Data.

Used by the PennCourseReview frontend and others.

# Architecture

The PCR API is composed of two parts. The scripts which pull the course data
from the registrar and the legacy PCR database, and the site which powers the
API itself.

## api

The api itself consists of five apps-- apiconsumer, course_descriptions,
courses, static_content, and testconsole.

### apiconsumer

Sets permission levels for developers who wish to use our API. This is mainly in
place because the data should only be accessible to Penn students and faculty.

### course_descriptions

Parses the course register. (Probably should be moved to /scripts)

### courses

Powers the actual API.

### static_content

Responsible for powering the static pages on the PCR site. It's basically a very
simple version of a CMS and exists solely so that admins only have to manage one
admin site.

### testconsole

testconsole is a simple javascript interface for the api.

## scripts

Responsible for scraping new data from the registrar and grabbing old data from
the legacy PCR site.

### Instructions to update the PCR API database

1. Change your directory to Penn-Course-API/scripts
2. Run "python download.py"
    * This scrapes the registrar, cleans up the data, and dumps it into /registrardata.
3. Run "python uploadcourses.py YEAR SEMESTER registrardata/*.txt"
   * uploadcourses.py [YEAR] [SEMESTER] [*FILES] parses the data scraped from download.py and uses it to update the PCR API database.
   * SEMESTER accepts either 'a', 'b', or 'c'
   * (ie, run "python uploadcourses.py 2009 a registrardata/econ.txt")
   * Since the registrar data changes every year, YEAR should be the current year, and SEMESTER the current semester.
4. Run "python import_from_pcr.py YEAR SEMESTER"
   * import_from_pcr.py [YEAR] [SEMESTER] reads from an external database-- assumed to have the original PCR records --and creates or updates course and review data in the new PCR API database.
   * (This can take a while.)

## Deployment

1. Connect to the production server.
2. Go to the directory containing `pcr-api` and run `source venv/bin/activate`.
3. Perform a `git pull`, `pip install -r requirements.txt`, and `./manage.py migrate`.
4. Set any necessary environment variables in `api/django.wsgi`.
5. Run `sudo apachectl -k graceful` to restart the server.

### Environment Variables
* `API_DEBUG` - Set this to `true` to enable Django debug mode.
* `API_DISPLAY_NAME` - Prepended before every api endpoint url, default is `/`.
* `API_SECRET_KEY` - The secret key for the Django application.
* `API_IMPORT_DATABASE_NAME` - The database to import from when using the import script.
* `API_IMPORT_DATABASE_USER` - The username for the database to import from when using the import script.
* `API_IMPORT_DATABASE_PWD` - The password for the database to import from when using the import script.
* `API_TEST_TOKEN` - The token used for live tests when running unit tests.
* `DATABASE_URL` - The location of the database.
* `SENTRY_DSN` - Set this to the Sentry DSN to enable error reporting.

# Setup

(Linux) Make sure you have the `libmysqlclient-dev` library installed:

```
sudo apt-get install libmysqlclient-dev
```

Install requirements with:

```
pip install -r requirements.txt
```

## MySQL Setup

The PennCourseReview API relies on MySQL for a database.

To install and setup MySQL on a Mac, use [Homebrew][1]:

```
brew remove mysql
brew cleanup
brew install mysql
mysql_install_db --verbose --user=whoami --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp
mysql.server start
```

## Configuration

Configuration variables are stored in environment variables. A list of these is shown below:

- `DEBUG` - Turns on and off debugging. The default is false.
- `API_DB_NAME` - The name of the database. Default is api.
- `API_DB_USER` - The user used to connect to the database. Default is root.
- `API_DB_PWD` - The password used to connect to the database. Default is none.
- `DISPLAY_NAME` - Prefixed before API requests (ex: `/v1/`). Default `/`.
- `SECRET_KEY` - Random string, should be kept secret in production.
- `TEST_API_TOKEN` - Used when running `python manage.py test`.

For local development, you may need to create a database.

1. Open the mysql shell with `mysql --user=root mysql`.
2. Create the database `CREATE DATABASE <DATABASE_NAME>;` where `<DATABASE_NAME>` is the value of `API_DB_NAME`.

Finally, setup the database with `python manage.py migrate`.

## Static files

Run `python manage.py collectstatic -l`

# Usage

To run the server:

```
python ./manage.py runserver
```

You may want to create a token to access data. Run `python ./manage.py maketoken` to create a token called "public".

Finally hit `http://localhost:8000/?token=public` to check that everything worked.

[1]: http://brew.sh/

# Testing

To test the server:

```
python ./manage.py test apiconsumer courses
```

At the time of writing, there are no failures in the test suite, but coverage is
relatively minimal.
