from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('bixly_blog.blog.views',
    url(r'^$', 'list_all', name='blog.list_all'),
    url(r'^new$', 'new', name='blog.new'),
    url(r'^entry/(?P<entry_pk>\d+)$', 'single', name='blog.single'),
    url(r'^filter/(?P<year>\d+)/(?P<month>\d+)$', 'filter',
        name='blog.filter_year_month'),
    url(r'^filter/(?P<year>\d+)/$', 'filter', name='blog.filter_year'),
    url(r'^c_filter$', 'choose_filter', name='blog.choose_filter'),
    url(r'^tagged/(?P<tag_pk>\d+)$', 'tagged_entries', name='blog.tagged'),
    url(r'^search$', 'search', name='blog.search'),
)
