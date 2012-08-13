from django.shortcuts import render_to_response

from bixly_blog.blog.models import BlogEntry


def list_all(request):
    """List all blog entries stored in our database."""
    entries = BlogEntry.objects.all()
    data = {'entries': entries}
    return render_to_response('list_all.html', data)
