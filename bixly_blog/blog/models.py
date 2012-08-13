import datetime

from django.contrib.auth.models import User
from django.db import models


class BlogEntry(models.Model):
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return '%s wrote on %s' % (self.creator, self.created)

    class Meta(object):
        verbose_name = 'Blog entry'
        verbose_name_plural = 'Blog entries'
        ordering = ['created']
