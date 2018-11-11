
.. _PennCourseReview: https://penncoursereview.com/

================================================================================
PennCourseReview
================================================================================

Front-end component to PennCourseReview_. Renders the data from the PCR API in a
user-friendly manner.

Introduction
================================================================================

PennCourseReview is a student-run publication that provides numerical ratings
and written reviews for undergraduate courses taught at the University of
Pennsylvania.

Setup
================================================================================

To set up your development environment:

1. Define ``PCR_API_TOKEN``, ``PROXY_TOKEN``, and ``SECRET_KEY``, plus anything
   else you may need in ``settings.py``. You can preferably also define this as
   an environment variable (``$PCR_API_TOKEN``). The default tokens do not work
   in production. Optionally, set the ``DEBUG`` environment variable, default is
   true for development.

2. Start the server locally, via::

    make server

Documentation
================================================================================

Documentation is available at http://penncoursereview.readthedocs.org/en/latest/
