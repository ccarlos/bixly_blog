from django.conf.urls import patterns, include, url
from django.contrib import admin

from bixly_blog import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bixly_blog.views.home', name='home'),
    # url(r'^bixly_blog/', include('bixly_blog.foo.urls')),
    (r'^$', 'django.contrib.auth.views.login'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^blog/', include('bixly_blog.blog.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^bixly_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root':     settings.MEDIA_ROOT}),
    )
