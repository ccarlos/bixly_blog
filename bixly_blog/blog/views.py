from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET

from bixly_blog.blog.models import BlogEntry
from bixly_blog.blog.utils import (smart_int, check_ranges, get_blog_info,
                                   paginate_objects)


def list_all(request):
    """List all blog entries stored in our database."""
    entries = BlogEntry.objects.all().order_by('-created')
    data = {'entries': paginate_objects(request, entries),
            'blog_info': get_blog_info()}

    return render_to_response('list_all.html', data)


@require_GET
def process_filter(request):
    """Determine which url to redirect user to, given GET variables."""

    year = request.GET.get('year', None)
    month = request.GET.get('month', None)

    # Convert year and month if applicable to ints.
    year = smart_int(year, None)
    month = smart_int(month, None)

    errors = []

    # Check valid ranges were provided for year and month.
    errors.extend(check_ranges(year, month))

    if month and not year:
        errors.append('A Year is required to make a filter search.')
    if not month and not year:
        errors.append('A Year or Year/Month combination is needed.')

    data = {'blog_info': get_blog_info(), 'errors': errors, 'mon_sel': month,
            'yr_sel': year}
    if errors:
        return render_to_response('list_all.html', data)

    kwargs = {}
    url_str = ''
    if month and year:
        kwargs = {'month': month, 'year': year}
        url_str = 'blog.filter_year_month'
    elif year:
        kwargs = {'year': year}
        url_str = 'blog.filter_year'

    return HttpResponseRedirect(reverse(url_str, kwargs=kwargs))


def filter(request, year=None, month=None):
    """Allow users to filter entries by year or year & month."""

    # Arguments used when searching for entries.
    kwargs = {}

    errors = []

    # Update kwargs with appropriate search kwargs.
    if year and month:
        kwargs.update({'created__year': year, 'created__month': month})
    elif year:
        kwargs.update({'created__year': year})
    elif month:
        errors.append('A Year is required to make a query search.')
    else:
        errors.append('A Year or Year/Month combination is needed.')

    data = {'blog_info': get_blog_info(), 'errors': errors, 'mon_sel': month,
            'yr_sel': year}

    if not errors:
        entries = BlogEntry.objects.filter(**kwargs).order_by('-created')
        data.update({'entries': paginate_objects(request, entries)})

    return render_to_response('list_all.html', data)
