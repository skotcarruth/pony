from django.conf.urls.defaults import *


urlpatterns = patterns('pony.users.views',
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^register/$', 'register'),
    (r'^dashboard/$', 'dashboard'),
)
