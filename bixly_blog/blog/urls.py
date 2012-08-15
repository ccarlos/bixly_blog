from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('bixly_blog.blog.views',
    url(r'^filter$', 'filter', name='blog.filter'),
    url(r'^$', 'list_all', name='blog.list_all'),
)
