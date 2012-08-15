import datetime

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
