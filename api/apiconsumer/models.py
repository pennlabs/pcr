import datetime
import string

from django.db import models
from django.utils import timezone


try:
    from secrets import choice
except ImportError:
    from random import choice


def generate_key():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '_'
    return ''.join(choice(chars) for x in range(30))


def generate_user_key():
    return 'user_{}'.format(generate_key())


def generate_api_consumer(token):
    name = 'Labs API ' + token
    email = 'admin+' + token + '@pennlabs.org'
    consumer = APIConsumer.objects.create(
        name=name,
        email=email,
        description='Penn Labs API automatic authentication',
        token=token,
        permission_level=2)
    return consumer


class APIUser(models.Model):
    username = models.CharField(max_length=200, unique=True)
    token = models.CharField(max_length=200, unique=True, default=generate_user_key)
    token_last_updated = models.DateTimeField(auto_now_add=True)

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

    def regenerate(self, force=False):
        if self.expiration <= timezone.now() or force:
            self.token_last_updated = timezone.now()
            self.token = generate_user_key()
            self.save(update_fields=['token', 'token_last_updated'])

    @property
    def expiration(self):
        return self.token_last_updated + datetime.timedelta(days=1)

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
