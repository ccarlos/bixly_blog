from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('bixly_blog.blog.views',
    url(r'^$', 'list_all', name='blog.list_all'),
    url(r'^new$', 'new', name='blog.new'),
    url(r'^filter/(?P<year>\d+)/(?P<month>\d+)$', 'filter',
        name='blog.filter_year_month'),
    url(r'^filter/(?P<year>\d+)/$', 'filter', name='blog.filter_year'),
    url(r'^p_filter$', 'process_filter', name='blog.process_filter'),
)
