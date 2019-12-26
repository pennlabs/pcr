# Penn Course Review

[![Build Status](https://travis-ci.org/pennlabs/pcr.svg?branch=master)](https://travis-ci.org/pennlabs/pcr)

The source code for [Penn Course Review](https://penncoursereview.com/).

## Introduction

PennCourseReview is a student-run publication that provides numerical ratings
and written reviews for undergraduate courses taught at the University of
Pennsylvania.

## Setup

To set up your development environment:

```bash
pipenv install --dev

cd frontend
npm install
```

To run the API server, obtain the `fixtures.json` file from a club member and run:

```bash
pipenv shell
./manage.py migrate
./manage.py loaddata fixtures.json
./manage.py maketoken
./manage.py runserver
```

To run the frontend, run the following command in a separate terminal:
```bash
cd frontend
npm start
```

## Documentation

See the [API readme](API-README.md) for more details about the Penn Course Review API.
