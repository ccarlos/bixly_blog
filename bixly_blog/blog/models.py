import markdown2

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    tag = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s' % (self.tag)


class BlogEntry(models.Model):
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    is_markdown = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s wrote on %s' % (self.creator, self.created)

    def get_absolute_url(self):
        return reverse('blog.single', kwargs={'entry_pk': self.pk})

    def save(self, *args, **kwargs):
        if self.is_markdown:
            self.body = markdown2.markdown(self.body)
        super(BlogEntry, self).save(*args, **kwargs)

    class Meta(object):
        verbose_name = 'Blog entry'
        verbose_name_plural = 'Blog entries'
        ordering = ['-created']
