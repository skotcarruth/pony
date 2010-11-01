from django.conf.urls.defaults import *


urlpatterns = patterns('pony.social.views',
    (r'^callback/(?P<service>\w+)/$', 'callback'),
)
