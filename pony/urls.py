from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template


admin.autodiscover()

### TEMP TEASER: These real urlpatterns are overwritten below!
urlpatterns = patterns('',
    # Flat URLs
    url(r'^$', 'pony.views.index'),
    url(r'^how-it-works/$', direct_to_template, {'template': 'flat/how_it_works.html'}, name='how_it_works'),
    url(r'^terms-of-use/$', direct_to_template, {'template': 'flat/terms_of_use.html'}, name='terms_of_use'),
    url(r'^privacy-policy/$', direct_to_template, {'template': 'flat/privacy_policy.html'}, name='privacy_policy'),

    # Our Apps
    url(r'^user/', include('pony.users.urls')),
    url(r'^gifts/', include('pony.gifts.urls')),
    url(r'^social/', include('pony.social.urls')),

    # Django Apps
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

### TEMP TEASER: This is the temp root urlconf for the teaser site
urlpatterns = patterns('',
    url(r'^', include('pony.teaser.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^favicon\.ico$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'path': 'favicon.ico'}),
        url(r'^404/$', direct_to_template, {'template': '404.html'}),
        url(r'^500/$', direct_to_template, {'template': '500.html'}),
    )
