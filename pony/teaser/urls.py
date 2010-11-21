from django.conf.urls.defaults import *


urlpatterns = patterns('pony.teaser.views',
    (r'^$', 'teaser_index'),
)
