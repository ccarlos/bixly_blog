from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET

from bixly_blog.blog.models import BlogEntry
from bixly_blog.blog.utils import smart_int, check_ranges, get_blog_info


def list_all(request):
    """List all blog entries stored in our database."""
    entries = BlogEntry.objects.all().order_by('-created')
    data = {'entries': entries, 'blog_info': get_blog_info()}

    return render_to_response('list_all.html', data)


@require_GET
def filter(request):
    """Allow users to filter entries by year or year & month."""

    year = request.GET.get('year', None)
    month = request.GET.get('month', None)

    # Convert year and month if applicable to ints.
    year = smart_int(year, None)
    month = smart_int(month, None)

    errors = []

    # Check valid ranges were provided for year and month.
    errors.extend(check_ranges(year, month))

    # Arguments used when searching for entries.
    kwargs = {}

    # Update kwargs with appropriate search kwargs.
    if year and month:
        kwargs.update({'created__year': year, 'created__month': month})
    elif year:
        kwargs.update({'created__year': year})
    elif month:
        errors.append('A Year is required to make a query search.')
    else:
        errors.append('A Year or Year/Month combination is needed.')

    data = {'blog_info': get_blog_info(), 'errors': errors}

    if not errors:
        entries = BlogEntry.objects.filter(**kwargs).order_by('-created')
        data.update({'entries': entries})

    return render_to_response('list_all.html', data)
