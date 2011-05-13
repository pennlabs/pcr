"""
NOTE: this is a development-specific file that lets us set various variables
(such as branch name, etc) so that we can share changes in the more general
django.wsgi and settings.py files without fear. This should be configured per-
sandbox. This and nothing else.
Author: AMK, Dec 27, 2010"""
import os

DISPLAY_NAME = "pcrsite-ceasarb" # IE, pennapps.com/display_name
DEV_ROOT = "/home/ceasarb/ceasarb_dev" # root of all apps you're working on
PCRSITE_APP_ROOT = os.path.join(DEV_ROOT, "pcrsite")
