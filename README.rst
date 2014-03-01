
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

Install
================================================================================

To install ``pcr``, simply::

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Next, copy ``local_settings.py_default`` to ``local_settings.py`` and define
``TOKEN`` and ``DEV_ROOT``, plus anything else you may need.

At this point, if you are editing on the server things should just work.

If you are editing locally, you can run the server as follows::

    python manage.py runserver --settings=local_settings

Documentation
================================================================================

Documentation is available at http://penncoursereview.readthedocs.org/en/latest/
