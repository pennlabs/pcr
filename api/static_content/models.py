from django.db import models


class Page(models.Model):
    """simple holder for Static content/raw HTML"""
    name = models.CharField(max_length=50)
    content = models.TextField()

    def __unicode__(self):
        return self.name
