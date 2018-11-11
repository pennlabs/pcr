from django.db import models
from random import choice
import string


def generate_key():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '_'
    return ''.join(choice(chars) for x in range(30))


def generate_api_consumer(token):
    name = "Labs API " + token
    email = "admin+" + token + "@pennlabs.org"
    consumer = APIConsumer.objects.create(
        name=name,
        email=email,
        description="Penn Labs API automatic authentication",
        token=token,
        permission_level=2)
    return consumer


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

    def __unicode__(self):
        return "%s (level %d)" % (self.name, self.permission_level)
