from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_http_methods

from bixly_blog.blog.models import BlogEntry, Tag, BlogComment, BlogCommentLike
from bixly_blog.blog.utils import (smart_int, check_ranges, get_blog_info,
                                   paginate_objects, get_rq)
from bixly_blog.blog.forms import BlogEntryForm, BlogCommentForm


def list_all(request):
    """List all blog entries stored in our database."""

    entries = BlogEntry.objects.all()
    data = {'entries': paginate_objects(request, entries),
            'blog_info': get_blog_info(), 'action_str': 'All Blogs Shown'}

    return render_to_response('blog/list_entries.html', data,
                              context_instance=get_rq(request))


@require_http_methods(['GET'])
def choose_filter(request):
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
        return render_to_response('blog/list_entries.html', data,
                                  context_instance=get_rq(request))

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

    search_str = 'You searched for Year: %s - Month: %s.' % (year, month)
    data = {'blog_info': get_blog_info(), 'errors': errors, 'mon_sel': month,
            'yr_sel': year, 'action_str': search_str}

    if not errors:
        entries = BlogEntry.objects.filter(**kwargs)
        data.update({'entries': paginate_objects(request, entries)})

    return render_to_response('blog/list_entries.html', data,
                              context_instance=get_rq(request))


@require_http_methods(['GET', 'POST'])
@login_required
def new(request):
    """Create a new BlogEntry for today."""

    if request.method == 'POST':
        data = request.POST
        form = BlogEntryForm(creator=request.user, data=data)
        if form.is_valid():
            form.save()
            # Should we redirect to single entry view or to all?
            return HttpResponseRedirect(reverse('blog.list_all'))
    else:
        form = BlogEntryForm(creator=request.user)

    data = {'form': form, 'blog_info': get_blog_info()}
    data.update(csrf(request))
    return render_to_response('blog/new_blog.html', data,
                              context_instance=get_rq(request))


def single(request, entry_pk=None, comment_form=None):
    """Display a single BlogEntry.

    Has tag links if any and a comment submission form.

    """

    entry = get_object_or_404(BlogEntry, pk=entry_pk)

    if not comment_form:
        comment_form = BlogCommentForm(creator=request.user, blog=entry)

    data = {'entry': entry, 'blog_info': get_blog_info(),
            'comment_form': comment_form}
    return render_to_response('blog/single.html', data,
                              context_instance=get_rq(request))


def tagged_entries(request, tag_pk=None):
    """Given a tag, return all BlogEntry's sharing that tag."""
    tag = get_object_or_404(Tag, pk=tag_pk)

    entries = tag.blogentry_set.all()
    search_str = 'Tag search results for: %s' % (tag.tag)
    data = {'entries': paginate_objects(request, entries),
            'action_str': search_str, 'blog_info': get_blog_info()}

    return render_to_response('blog/list_entries.html', data,
                              context_instance=get_rq(request))


def search(request):
    """Perform a query agaist a BlogEntry title and body.

    Supports Boolean Full-Text Searches. Refer to:
    http://dev.mysql.com/doc/refman/4.1/en/fulltext-boolean.html

    """

    query = request.GET.get('q', '')

    if query:
        q1 = Q(title__search=query)
        q2 = Q(body__search=query)

        results = BlogEntry.objects.filter(q1 | q2).order_by(
            '-created').distinct()
    else:
        results = []

    search_str = 'Search results for: %s' % (query)
    data = {'entries': paginate_objects(request, results),
            'action_str': search_str, 'blog_info': get_blog_info()}

    return render_to_response('blog/list_entries.html', data,
                              context_instance=get_rq(request))


@login_required
@require_http_methods(['POST'])
def add_comment(request, entry_pk):
    """Add a comment to a blog entry, given its id."""

    blog = get_object_or_404(BlogEntry, pk=entry_pk)

    if not request.user.is_authenticated():
        raise PermissionDenied

    form = BlogCommentForm(creator=request.user, blog=blog, data=request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(blog.get_absolute_url())

    return single(request, entry_pk=entry_pk, comment_form=form)


@login_required
@require_http_methods(['POST'])
def remove_comment(request, comm_pk):
    """Delete a comment. Only allow if user is creator of comment or blog."""

    comm = get_object_or_404(BlogComment, pk=comm_pk)

    blog = comm.blog

    # Check whether user is comment.creator or blog.creator
    if comm.creator != request.user and blog.creator != request.user:
        raise PermissionDenied

    comm.delete()

    return HttpResponseRedirect(reverse('blog.single',
                                        kwargs={'entry_pk': blog.pk}))


@require_http_methods(['GET', 'POST'])
@login_required
def edit_comment(request, comm_pk):
    """Edit a comment."""

    comm = get_object_or_404(BlogComment, pk=comm_pk)

    # Check whether request.user is comment.creator.
    if comm.creator != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        data = request.POST
        form = BlogCommentForm(creator=comm.creator, blog=comm.blog,
                               data=data, instance=comm)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(comm.blog.get_absolute_url())
    else:
        form = BlogCommentForm(creator=comm.creator, blog=comm.blog,
                               instance=comm)

    data = {'action_str': 'Edit Comment', 'blog_info': get_blog_info(),
            'comm': comm, 'comment_form': form}

    return render_to_response('blog/edit_comment.html', data,
                              context_instance=get_rq(request))


# TODO: rename to like_dislike_comment.
# TODO: Separate like and dislike. Dislike should subtract from a count.
@login_required
@require_http_methods(['POST'])
def like_comment(request, comm_pk):
    comm = get_object_or_404(BlogComment, pk=comm_pk)

    # Has the user liked the comment object?
    like = comm.likes.filter(creator=request.user)
    if not like:
        BlogCommentLike.objects.create(creator=request.user, comm=comm)
    else:
        like.delete()

    return HttpResponseRedirect(reverse('blog.single',
                                        kwargs={'entry_pk': comm.blog.pk}))
