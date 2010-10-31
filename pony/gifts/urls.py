from django.conf.urls.defaults import *


urlpatterns = patterns('pony.gifts.views',
    (r'^add/$', 'add'),
    (r'^(?P<gift_id>\d+)/$', 'detail'),
    (r'^(?P<gift_id>\d+)/give/$', 'give'),
)
