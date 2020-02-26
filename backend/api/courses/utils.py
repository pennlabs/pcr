import datetime

from .models import Semester


def current_semester():
    now = datetime.datetime.now()
    semester = 'A' if now.month < 5 else ('B' if now.month < 9 else 'C')
    return Semester(now.year, semester)


# FNAR 337 Advanced Orange (Jaime Mundo)
# Explore the majesty of the color Orange in its natural habitat,
# and ridicule other, uglier colors, such as Chartreuse (eww).

# MGMT 099 The Art of Delegating (Alexey Komissarouky)
# The Kemisserouh delegates teaching duties to you. Independent study.

class API404(Exception):
    def __init__(self, message=None, perhaps=None):
        self.message = message
        self.perhaps = perhaps
