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
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt

cd frontend
npm install
```

To run the API server:

Ensure that the `DATABASE_URL` environment variable is set to the correct value.

```bash
source venv/bin/activate
./manage.py runserver
```

To run the frontend, run:
```bash
cd frontend
npm start
```

## Documentation

See the [API readme](API-README.md) for more details about the Penn Course Review API.
