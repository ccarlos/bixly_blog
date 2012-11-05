from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('bixly_blog.blog.views',
    url(r'^$', 'list_all', name='blog.list_all'),
    url(r'^entry/(?P<entry_pk>\d+)$', 'single', name='blog.single'),

    url(r'^new$', 'new', name='blog.new'),

    # Filter on Year and/or Month urls.
    url(r'^c_filter$', 'choose_filter', name='blog.choose_filter'),
    url(r'^filter/(?P<year>\d+)/(?P<month>\d+)$', 'filter',
        name='blog.filter_year_month'),
    url(r'^filter/(?P<year>\d+)/$', 'filter', name='blog.filter_year'),

    # Search urls.
    url(r'^tagged/(?P<tag_pk>\d+)$', 'tagged_entries', name='blog.tagged'),
    url(r'^search$', 'search', name='blog.search'),

    # Comment urls.
    url(r'^entry/(?P<entry_pk>\d+)/comment$', 'add_comment',
        name='blog.comment'),
    url(r'^remove_comment/(?P<comm_pk>\d+)$', 'remove_comment',
        name='blog.remove_comment'),
    url(r'^edit_comment/(?P<comm_pk>\d+)$', 'edit_comment',
        name='blog.edit_comment'),
    url(r'^like_comment/(?P<comm_pk>\d+)$', 'like_comment',
        name='blog.like_comment'),
)
