from django import forms

from bixly_blog.blog.models import BlogEntry
from bixly_blog.blog.utils import process_tags


class BlogEntryForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    body = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 20,
                                     'placeholder': 'Write your blog...'}))

    class Meta:
        model = BlogEntry
        fields = ('title', 'body')

    def __init__(self, creator, data=None, *args, **kwargs):
        self.creator = creator
        self.tags = ''
        if data:
            data = data.copy()
            data.update({'creator': creator.pk})
            self.tags = data.get('tags')
        super(BlogEntryForm, self).__init__(data=data, *args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        entry = super(BlogEntryForm, self).save(*args, commit=False, **kwargs)

        if not commit:
            return entry

        entry.creator = self.creator
        entry.save()

        # TAGS processing. Associate tags with given BlogEntry.
        if self.tags:
            process_tags(entry.pk, self.tags)

        return entry
