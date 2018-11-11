__author__ = 'Kyle Hardgrave (kyleh@sas.upenn.edu)'

from optparse import make_option
import time

import MySQLdb as db
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from courses.models import (Alias, Course, CourseHistory, Department,
                            Instructor, Review, ReviewBit, Section, Semester)


class Command(BaseCommand):

    option_list = (
        make_option('-d', '--dryrun', action='store_true',
                    help=('Show what _would_ have happened.')),
    ) + BaseCommand.option_list

    dry_run = False
    db = None

    def log(self, msg):
        self.stdout.write('%s\n' % msg)

    def handle(self, *args, **opts):
        """Handle command line arguments."""
        self.db = db.connect(db='kyleh_pcrapi', user=settings.IMPORT_DATABASE_USER,
                             passwd=settings.IMPORT_DATABASE_PWD)
        self.dry_run = opts['dryrun']
        duplicate_ids = self.query(('SELECT oldpcr_id FROM courses_instructor '
                                    'GROUP BY oldpcr_id HAVING count(id) > 1'))
        profs_kept = 0
        profs_removed = 0
        sects_modified = 0
        reviews_modified = 0
        for dup_id in duplicate_ids:
            dup_id = dup_id[0]
            profs = Instructor.objects.filter(oldpcr_id=dup_id).order_by('id')
            orig_prof = profs[0]
            profs_kept += 1
            self.log('--------------------')
            self.log('Merging %d duplicates into %s' % (len(profs), orig_prof))
            for dup_prof in profs[1:]:
                profs_removed += 1
                self.log('Removing duplicate professor %s' % dup_prof)

                sects = Section.objects.filter(instructors=dup_prof)
                for sect in sects:
                    self.log('Reassigning section %s' % sect)
                    if not self.dry_run:
                        sect.instructors.remove(dup_prof)
                        sect.instructors.add(orig_prof)
                    sects_modified += 1

                reviews = Review.objects.filter(instructor=dup_prof)
                for review in reviews:
                    self.log('Reassigning review %s' % review)
                    review.instructor = orig_prof
                    reviews_modified += 1
                    if not self.dry_run:
                        review.save()

                orig_prof.first_name = dup_prof.first_name
                orig_prof.last_name = dup_prof.last_name
                if not self.dry_run:
                    dup_prof.delete()
            if not self.dry_run:
                orig_prof.save()

        self.log('------------------------------------------------------------')
        self.log(('Merged %d duplicate instructors into %d original ones. '
                  'Modified %d sections and %d reviews.' % (
                      profs_removed, profs_kept, sects_modified, reviews_modified)))

    def select(self, fields, tables, conditions=None, group_by=None,
               order_by=None):
        """A wrapper for MySQL SELECT queries.

        Args:
            fields: List of database row names
            tables: List of database table names
            conditions: Map of field-value pairs to filter by
            group_by: List of fields to group (aggregate) by
            order_by: List of fields to order by
        """
        query = ["SELECT", ", ".join(fields), "FROM", ", ".join(tables)]

        if conditions:
            query.extend(["WHERE", " AND ".join(conditions)])

        if group_by:
            query.extend(["GROUP BY", ", ".join(group_by)])

        if order_by:
            query.extend(["ORDER BY", ", ".join(order_by)])

        return self.query(" ".join(query))

    def query(self, query_str, args=None):
        """A simple wrapper for our MySQL queries."""
        start = time.time()
        self.log('Executing query: "%s"' % query_str)
        cursor = self.db.cursor()
        cursor.execute(query_str, args)
        results = cursor.fetchall()
        self.log('Took: %s' % (time.time() - start))
        self.log('Founds %s results.' % len(results))
        return results
