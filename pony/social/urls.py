from django.conf.urls.defaults import *


urlpatterns = patterns('pony.social.views',
    (r'^callback/(?P<service>\w+)/$', 'callback'),
    (r'^oauth/(?P<service>\w+)/authorize-url/$', 'authorize_url'),
    (r'^oauth/(?P<service>\w+)/(?P<method>\w+)/(?P<category>\w+)/(?P<resource>\w+)/$', 'access_resource'),
)
