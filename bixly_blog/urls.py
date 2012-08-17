from django.conf.urls import patterns, include, url
from django.contrib import admin

from bixly_blog import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Authentication urls.
    (r'^$', 'django.contrib.auth.views.login'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),

    # Our blog urls
    (r'^blog/', include('bixly_blog.blog.urls')),

    # Used to add comment functionality to BlogEntry's.
    (r'^comments/', include('django.contrib.comments.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^bixly_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root':     settings.MEDIA_ROOT}),
    )
