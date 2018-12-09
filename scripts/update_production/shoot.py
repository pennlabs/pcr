#!/usr/bin/env python3

# A script like regenerate_cache.py, except it doesn't require twisted and works with Python 3.
# Run regenerate_cache.py with the --dry-run flag to get urls, and then use this to hit everything.

import sys
import string
import requests

from concurrent.futures import ThreadPoolExecutor

def run(url):
    resp = requests.get(url)
    resp.raise_for_status()
    print("{} {}".format(resp.status_code, url))

with ThreadPoolExecutor(max_workers=15) as executor:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            for line in f:
                executor.submit(run, line.strip())
    else:
        print("Usage: {} <url file>".format(sys.argv[0]))
        exit(1)
