
# PennCourseReview API

Provides the PennCourseReview API.

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
