from django import forms

from bixly_blog.blog.models import BlogEntry, BlogComment
from bixly_blog.blog.utils import process_tags


class BlogEntryForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your Blog\'s title'}))
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
        self.is_markdown = False
        if data:
            data = data.copy()
            data.update({'creator': creator.pk})
            self.tags = data.get('tags')
            self.is_markdown = True if 'is_markdown' in data else False
        super(BlogEntryForm, self).__init__(data=data, *args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        entry = super(BlogEntryForm, self).save(*args, commit=False, **kwargs)

        if not commit:
            return entry

        entry.creator = self.creator
        entry.is_markdown = self.is_markdown
        entry.save()

        # Tag processing. Associate tags with given BlogEntry.
        if self.tags:
            process_tags(entry.pk, self.tags)

        return entry


class BlogCommentForm(forms.ModelForm):
    body = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 20,
                                     'placeholder': 'Enter Comment...'}))

    class Meta:
        model = BlogComment
        fields = ('body',)

    def __init__(self, blog, creator, data=None, *args, **kwargs):
        self.blog = blog
        self.creator = creator
        if data:
            data = data.copy()
            data.update({'creator': creator.pk})
        super(BlogCommentForm, self).__init__(data=data, *args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        comm = super(BlogCommentForm, self).save(*args, commit=False, **kwargs)

        if commit:
            comm.blog = self.blog
            comm.creator = self.creator
            comm.save()

        return comm
