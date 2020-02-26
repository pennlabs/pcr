import string

from django.db import models


try:
    from secrets import choice
except ImportError:
    from random import choice


def generate_key():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '_'
    return ''.join(choice(chars) for x in range(30))


def generate_user_key():
    return 'user_{}'.format(generate_key())


class APIUser(object):
    """
    Fake model class used to represent a logged in user.
    User management is handled by platform authentication.
    """
    def __init__(self, username, token=None):
        self.username = username
        self.token = token

    @property
    def permission_level(self):
        return 2

    @property
    def valid(self):
        return True

    @property
    def access_pcr(self):
        return True

    @property
    def access_secret(self):
        return False

    def __str__(self):
        return '%s (user)' % (self.username)


class APIConsumer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=75, unique=True)
    description = models.TextField()
    token = models.CharField(max_length=200, unique=True, default=generate_key)
    permission_level = models.IntegerField(default=2)

    # 0 - no access, equivalent to no key
    # 1 - access to public data only
    # 2 - access to PCR data
    # 9001 - access to secret pcrsite stuff

    @property
    def valid(self):
        return self.permission_level > 0

    @property
    def access_pcr(self):
        return self.permission_level >= 2

    @property
    def access_secret(self):
        return self.permission_level > 9000

    def __str__(self):
        return '%s (level %d)' % (self.name, self.permission_level)
