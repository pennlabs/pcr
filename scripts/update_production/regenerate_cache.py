# Script to regenerate the Penn Course Review site cache.
#
# NOTE: On the production server, this should be run using
#   /usr/bin/python2.6
# since it has twisted installed, but python2.7 does not.
#
# Before running this, make sure the symlink at
#   penncoursereview.com:~pcr/projects/pcrsite/staticgenerator_output/write
# points to a fresh cache directory. (Also, all cache directories and symlinks
# should be owned by the Apache user "www-data".) When finished, remove the
# previous read symlink and point a new read symlink to the new cache
# directory. Remove dead directories as necessary (it's usually a good idea to
# keep 1 old one around.)
#
# This should definitely be run on a Penn (i.e. not off-campus) internet
# connection (since STWing's connection is much faster on-campus). Running
# it directly on the PCR server may or may not be a good idea.
#
# Known bugs: Many. In particular, watch out for:
#  - running out of disk space
#  - going over the maximum number of folders in the API cache
#
# If it breaks in the middle, don't worry about it, just rerun it. It'll
# go through the pages it's already cached really quickly.
# Note that many of the errors you'll get are just due to server overload,
# so it's probably a good idea to run the script twice (the pages that were
# overloaded before will [hopefully] work this time, and [theoretically]
# the only pages that fail on the second run are the ones with real errors)

import os
import urllib2
import json
import string
import argparse
import logging

from twisted.internet import reactor
import twisted.internet.defer
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

logging.getLogger().setLevel(logging.INFO)

URL_PREFIX = 'https://penncoursereview.com/__cache__regen/'
AUTOCOMPLETE_PATH = 'autocomplete_data.json/'
N_CONCURRENT_ACCESSES = 15
SUCCESS_DISPLAY_LEN = 80


class PrinterClient(Protocol):
    def __init__(self, whenFinished, displayMax=80, displayFinished=True):
        self.whenFinished = whenFinished
        self.firstPart = True
        self.displayMax = displayMax
        self.displayFinished = displayFinished

    def dataReceived(self, bytes):
        if self.firstPart:
            self.firstPart = False
            logging.info(repr(bytes)[1:(1+self.displayMax)])

    def connectionLost(self, reason):
        if self.displayFinished:
            logging.warning('Finished:', reason.getErrorMessage())
        self.whenFinished.callback(None)


def handleResponse(r, url, num, lenurls):
    isError = r.code != 200
    logging.info("%c %d %6.2f%% (%6d) %50s  " % ('X' if isError else ' ', r.code, num*100.0/lenurls, num, url))
    if isError:
        logging.error("##### HTTP Error %d: %s" % (r.code, r.phrase))
        for k, v in r.headers.getAllRawHeaders():
            logging.error("%s: %s" % (k, '\n  '.join(v)))
    whenFinished = twisted.internet.defer.Deferred()
    r.deliverBody(PrinterClient(whenFinished, 400 if isError else SUCCESS_DISPLAY_LEN, isError))
    return whenFinished


def handleError(reason, url, num, lenurls):
    logging.error("X %6.2f%% (%6d) %50s" % (num*100.0/lenurls, num, url))
    logging.error("##### Script Error")
    reason.printTraceback()
    reactor.stop()


def getPage(url, num, lenurls):
    args = [url, num, lenurls]
    d = Agent(reactor).request('GET', URL_PREFIX + url, Headers({'User-Agent': ['twisted']}), None)
    d.addCallbacks(handleResponse, handleError, args, None, args, None)
    return d


parser = argparse.ArgumentParser(description='Regenerate the cache on PCR by visiting common pages.')
parser.add_argument('-n', '--dry-run', action='store_true', help='Do not actually generate cache, but print out urls that would be visited.')
args = parser.parse_args()

logging.info('Retrieving base json file...')
d = urllib2.urlopen(URL_PREFIX + AUTOCOMPLETE_PATH)
d_data = d.read()
logging.info('Retrieved base json file...')
j = json.loads(d_data)
logging.info('Finished parsing base json file...')
urls = ([os.path.join(AUTOCOMPLETE_PATH, c1 + c2 + ".json")
         for c1 in string.letters[:26] for c2 in string.letters[:26]] +
        [str(item['url']) for item_categ in j.values() for item in item_categ])
logging.info('Finished parsing prefix json files...')


semaphore = twisted.internet.defer.DeferredSemaphore(N_CONCURRENT_ACCESSES)
dl = list()

if args.dry_run:
    for url in urls:
        logging.info(">>> {}".format(url))
    logging.info("Total of {} urls.".format(len(urls)))
    exit(0)

logging.info("Loading %d URLS..." % len(urls))
for i, url in enumerate(urls):
    dl.append(semaphore.run(getPage, url, i, len(urls)))

logging.info("Starting URL processing...")
dl = twisted.internet.defer.DeferredList(dl)
dl.addCallbacks(lambda x: reactor.stop(), handleError)

reactor.run()
