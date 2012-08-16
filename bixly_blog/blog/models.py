from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class BlogEntry(models.Model):
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s wrote on %s' % (self.creator, self.created)

    def get_absolute_url(self):
        return reverse('blog.single', kwargs={'entry_pk': self.pk})

    class Meta(object):
        verbose_name = 'Blog entry'
        verbose_name_plural = 'Blog entries'
        ordering = ['created']
