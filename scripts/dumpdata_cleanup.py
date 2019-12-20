#!/usr/bin/env python3

import json
import sys
import argparse
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser(description='Cleanup and reduce PCR Django fixture data dump. Writes the new data dump json to stdout.')
    parser.add_argument('file', type=str, help='The input file to parse, generated from the ./manage.py dumpdata command.')
    parser.add_argument('--no-reference-cleanup', action='store_true', help='Do not remove objects with broken references.')

    args = parser.parse_args()

    # Load JSON data dump
    with open(args.file, 'r') as f:
        items = json.load(f)

    # Remove models
    remove = set([
        'contenttypes.contenttype',
        'apiconsumer.apiconsumer',
        'apiconsumer.apiuser',
        'admin.logentry',
        'sessions.session',
        'sites.site',
        'auth.user',
        'auth.permission'
    ])
    new_items = []
    for item in items:
        if item['model'] not in remove:
            new_items.append(item)
    items = new_items

    # Save the primary key of all objects
    models = defaultdict(set)

    for item in items:
        models[item['model']].add(item['pk'])

    if not args.no_reference_cleanup:
        # Remove objects with broken foreign key references
        fixes = [
            ('courses.alias', 'department', 'courses.department'),
            ('courses.alias', 'course', 'courses.course'),
            ('courses.course', 'primary_alias', 'courses.alias'),
            ('courses.section', 'course', 'courses.course'),
            ('courses.review', 'section', 'courses.section'),
            ('courses.review', 'instructor', 'courses.instructor'),
            ('courses.reviewbit', 'review', 'courses.review'),
        ]

        # Sanity check fix inputs
        for model, field, to in fixes:
            if model in models:
                assert to in models, to

        for num in [1, 2]:
            for model, field, to in fixes:
                new_items = []
                old_sum = 0
                new_sum = 0
                for item in items:
                    if item['model'] == model:
                        old_sum += 1
                        if item['fields'][field] in models[to]:
                            new_sum += 1
                            new_items.append(item)
                        else:
                            try:
                                models[model].remove(item['pk'])
                            except KeyError:
                                pass
                    else:
                        new_items.append(item)
                print('[Round {}] Applied rule {} -> kept {}/{} item(s)'.format(num, (model, field, to), new_sum, old_sum), file=sys.stderr)
                items = new_items

    print(json.dumps(items))


if __name__ == '__main__':
    main()
