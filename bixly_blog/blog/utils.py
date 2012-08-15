import datetime

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bixly_blog.blog.models import BlogEntry

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']


def smart_int(string, fallback=0):
    """Convert a string to int, with fallback for invalid strings or types."""
    try:
        return int(string)
    except (OverflowError, TypeError, ValueError):
        return fallback


def check_ranges(year, month):
    """Return a [] of error messages if year and/or month are not in range."""
    errors = []
    if year and not (datetime.MINYEAR <= year <= datetime.MAXYEAR):
        errors.append('Invalid year used.')
    if month and not (1 <= month <= 12):
        errors.append('Invalid month used.')
    return errors


def get_blog_info():
    """Return a {} with months and year keys. Used for filter purposes"""
    dates = BlogEntry.objects.dates('created', 'year', order='DESC')
    years = [y.year for y in dates]
    return {'months': MONTHS, 'years': years}


def paginate_objects(request, objs):
    paginator = Paginator(objs, settings.ENTRIES_PER_PAGE)

    page = request.GET.get('page')
    try:
        ents = paginator.page(page)
    except PageNotAnInteger:
        # Deliver first page.
        ents = paginator.page(1)
    except EmptyPage:
        # Out of range, deliver last page.
        ents = paginator.page(paginator.num_pages)

    return ents
